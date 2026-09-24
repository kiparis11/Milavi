from django.contrib import admin
from django.contrib import messages

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = (
        'product',
        'product_name',
        'size',
        'temperature',
        'addons',
        'unit_price',
        'quantity',
    )

    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'status',
        'payment_method',
        'payment_status',
        'total_price',
        'created_at',
    )

    list_filter = (
        'status',
        'payment_method',
        'payment_status',
        'created_at',
    )

    search_fields = (
        'id',
        'user__username',
        'full_name',
        'phone',
        'address',
    )

    readonly_fields = (
        'user',
        'full_name',
        'phone',
        'address',
        'comment',
        'payment_method',
        'payment_status',
        'total_price',
        'cart_snapshot',
        'created_at',
        'updated_at',
    )

    inlines = [
        OrderItemInline,
    ]

    actions = [
        'confirm_cash_payment',
    ]

    @admin.action(description='Подтвердить оплату при получении')
    def confirm_cash_payment(self, request, queryset):
        updated = 0

        for order in queryset:
            if (
                order.payment_method == 'cash'
                and order.payment_status != 'paid'
                and order.status != 'cancelled'
            ):
                order.payment_status = 'paid'
                order.save(
                    update_fields=[
                        'payment_status',
                        'updated_at',
                    ]
                )
                updated += 1

        if updated:
            self.message_user(
                request,
                f'Оплата подтверждена для заказов: {updated}.',
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                'Подходящих заказов для подтверждения оплаты нет.',
                level=messages.WARNING,
            )