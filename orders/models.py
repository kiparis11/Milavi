from django.conf import settings
from django.db import models

from shop.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('preparing', 'Готовится'),
        ('delivering', 'Доставляется'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('demo_card', 'Картой онлайн'),
        ('cash', 'При получении'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('failed', 'Ошибка оплаты'),
        ('cancelled', 'Оплата отменена'),
        ('refunded', 'Возврат совершен'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Покупатель'
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name='Имя получателя'
    )

    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона'
    )

    address = models.TextField(
        verbose_name='Адрес доставки'
    )

    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий к заказу'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        verbose_name='Способ оплаты'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='Статус оплаты'
    )

    cart_snapshot = models.JSONField(
        default=list,
        blank=True,
        editable=False,
        verbose_name='Содержимое корзины при оформлении'
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Итоговая стоимость'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оформления'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id} — {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Товар'
    )

    product_name = models.CharField(
        max_length=200,
        verbose_name='Название товара'
    )

    size = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Размер'
    )

    temperature = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Температура'
    )

    addons = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Добавки'
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена за единицу'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return self.product_name
