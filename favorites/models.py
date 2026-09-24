from django.conf import settings
from django.db import models

from shop.models import Product


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name = 'Пользователь'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Товар'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата добавления')

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} — {self.product.name}'