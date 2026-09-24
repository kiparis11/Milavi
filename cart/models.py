from django.conf import settings
from django.db import models

from shop.models import Product, ProductSize, ProductAddon


class CartItem(models.Model):
    TEMPERATURE_CHOICES = [
        ('hot', 'Горячий'),
        ('cold', 'Холодный'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Пользователь'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар'
    )

    size = models.ForeignKey(
        ProductSize,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Размер'
    )

    temperature = models.CharField(
        max_length=10,
        choices=TEMPERATURE_CHOICES,
        blank=True,
        verbose_name='Температура'
    )

    addons = models.ManyToManyField(
        ProductAddon,
        blank=True,
        verbose_name='Добавки'
    )

    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')


    @property
    def unit_price(self):
        price = self.product.price

        if self.size:
            price += self.size.extra_price

        for addon in self.addons.all():
            price += addon.extra_price

        return price


    @property
    def total_price(self):
        return self.unit_price * self.quantity


    def __str__(self):
        return f'{self.user.username} — {self.product.name}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
