from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from cart.models import CartItem

from .forms import OrderForm
from .models import Order, OrderItem


def clear_ordered_cart_items(order):

    for entry in order.cart_snapshot:
        cart_item = (
            CartItem.objects
            .select_for_update()
            .filter(
                id=entry['id'],
                user=order.user
            )
            .first()
        )

        if cart_item is None:
            continue

        ordered_quantity = entry['quantity']

        if cart_item.quantity > ordered_quantity:
            cart_item.quantity -= ordered_quantity
            cart_item.save(update_fields=['quantity'])
        else:
            cart_item.delete()


@login_required
def checkout(request):
    cart_items = list(
        CartItem.objects
        .filter(user=request.user)
        .select_related('product', 'size')
        .prefetch_related('addons')
    )

    if not cart_items:
        return redirect('cart_detail')

    error = None


    for item in cart_items:
        product = item.product

        if not product.is_available:
            error = (
                f'Товар «{product.name}» больше недоступен. '
                'Удалите его из корзины.'
            )
            break

        if product.has_sizes and not item.size:
            error = (
                f'Для товара «{product.name}» '
                'необходимо выбрать размер.'
            )
            break

        if item.size and item.size.product_id != product.id:
            error = 'Обнаружен некорректный размер товара.'
            break

        if product.has_temperature and item.temperature not in (
            'hot', 'cold'
        ):
            error = 'Обнаружена некорректная температура товара.'
            break

        for addon in item.addons.all():
            if (
                addon.product_id != product.id
                or not addon.is_available
            ):
                error = (
                    f'Одна из добавок для товара '
                    f'«{product.name}» больше недоступна.'
                )
                break

        if error:
            break

    cart_total = sum(
        (item.total_price for item in cart_items),
        Decimal('0.00')
    )

    form = OrderForm(request.POST or None)

    if request.method == 'POST' and form.is_valid() and not error:

        snapshot = [
            {
                'id': item.id,
                'quantity': item.quantity
            }
            for item in cart_items
        ]

        with transaction.atomic():

            # Если неоплаченный заказ с такой же корзиной
            # уже существует, не создаём его повторно.
            if form.cleaned_data['payment_method'] == 'demo_card':
                existing_order = Order.objects.filter(
                    user=request.user,
                    status='new',
                    payment_method='demo_card',
                    payment_status__in=['pending', 'failed'],
                    cart_snapshot=snapshot
                ).order_by('-id').first()

                if existing_order:
                    return redirect(
                        'demo_payment',
                        order_id=existing_order.id
                    )

            order = form.save(commit=False)

            order.user = request.user
            order.total_price = cart_total
            order.payment_status = 'pending'
            order.cart_snapshot = snapshot

            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    size=item.size.size if item.size else '',
                    temperature=(
                        item.get_temperature_display()
                        if item.temperature else ''
                    ),
                    addons=[
                        addon.name
                        for addon in item.addons.all()
                    ],
                    unit_price=item.unit_price,
                    quantity=item.quantity
                )

            # При оплате при получении заказ уже подтверждён.
            if order.payment_method == 'cash':
                clear_ordered_cart_items(order)

        if order.payment_method == 'demo_card':
            return redirect(
                'demo_payment',
                order_id=order.id
            )

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'error': error,
        }
    )


@login_required
def demo_payment(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
        payment_method='demo_card'
    )

    if order.payment_status == 'paid':
        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'orders/demo_payment.html',
        {'order': order}
    )


@login_required
@require_POST
def process_demo_payment(request, order_id):
    result = request.POST.get('result')

    if result not in ('success', 'failed'):
        return HttpResponseBadRequest(
            'Некорректный результат оплаты.'
        )

    with transaction.atomic():
        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            user=request.user,
            payment_method='demo_card'
        )


        if order.payment_status == 'paid':
            return redirect(
                'order_success',
                order_id=order.id
            )

        if order.status == 'cancelled':
            return HttpResponseBadRequest(
                'Отменённый заказ нельзя оплатить.'
            )

        if result == 'success':
            order.payment_status = 'paid'
            order.save(
                update_fields=['payment_status', 'updated_at']
            )

            clear_ordered_cart_items(order)

        else:
            order.payment_status = 'failed'
            order.save(
                update_fields=['payment_status', 'updated_at']
            )

    if result == 'success':
        return redirect(
            'order_success',
            order_id=order.id
        )

    return redirect(
        'demo_payment',
        order_id=order.id
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        id=order_id,
        user=request.user
    )

    # Если заказ отменён, показываем его подробности
    if order.status == 'cancelled':
        return redirect(
            'order_detail',
            order_id=order.id
        )

    if (
        order.payment_method == 'demo_card'
        and order.payment_status != 'paid'
    ):
        return redirect(
            'demo_payment',
            order_id=order.id
        )

    return render(
        request,
        'orders/order_success.html',
        {'order': order}
    )

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
        }
    )


@login_required
@require_POST
def cancel_order(request, order_id):
    with transaction.atomic():
        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            user=request.user
        )

        if order.status != 'new':
            messages.error(
                request,
                'Этот заказ уже нельзя отменить.'
            )

            return redirect(
                'order_detail',
                order_id=order.id
            )

        order.status = 'cancelled'

        if order.payment_status == 'paid':
            order.payment_status = 'refunded'
        else:
            order.payment_status = 'cancelled'

        order.save(
            update_fields=[
                'status',
                'payment_status',
                'updated_at'
            ]
        )

    messages.success(
        request,
        'Ваш заказ успешно отменён.'
    )

    return redirect(
        'order_detail',
        order_id=order.id
    )