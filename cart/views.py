from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product, ProductSize, ProductAddon

from .models import CartItem


@login_required
def cart_detail(request):
    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related(
            'product',
            'product__category',
            'size'
        )
        .prefetch_related('addons')
    )

    cart_total = sum(
        item.total_price
        for item in cart_items
    )

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }

    return render(
        request,
        'cart/cart_detail.html',
        context
    )


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    # Размер
    size = None

    if product.has_sizes:
        size_id = request.POST.get('size')

        if size_id:
            size = ProductSize.objects.filter(
                id=size_id,
                product=product
            ).first()

        if size is None:
            size = product.sizes.first()


    # Температура
    temperature = ''

    if product.has_temperature:
        temperature = request.POST.get(
            'temperature',
            'hot'
        )

        if temperature not in ('hot', 'cold'):
            temperature = 'hot'


    # Добавки
    addon_ids = request.POST.getlist('addons')

    addons = ProductAddon.objects.filter(
        product=product,
        id__in=addon_ids,
        is_available=True
    )

    selected_addon_ids = set(
        addons.values_list('id', flat=True)
    )

    same_items = (
        CartItem.objects
        .filter(
            user=request.user,
            product=product,
            size=size,
            temperature=temperature
        )
        .prefetch_related('addons')
    )

    cart_item = None

    for item in same_items:
        item_addon_ids = set(
            item.addons.values_list('id', flat=True)
        )

        if item_addon_ids == selected_addon_ids:
            cart_item = item
            break

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()

    else:
        cart_item = CartItem.objects.create(
            user=request.user,
            product=product,
            size=size,
            temperature=temperature
        )

        cart_item.addons.set(addons)


    return redirect('cart_detail')


@login_required
@require_POST
def change_quantity(request, item_id, action):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()

    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart_detail')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart_detail')
