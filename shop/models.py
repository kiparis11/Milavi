from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL-адрес')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name = 'Категория'
    )
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')

    is_available = models.BooleanField(default=True, verbose_name='Доступен для заказа')
    is_featured = models.BooleanField(default=False, verbose_name='Особенное предложение')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')

    has_sizes = models.BooleanField(default=False, verbose_name='Выбор размера')
    has_temperature = models.BooleanField(default=False, verbose_name='Выбор температуры')
    has_addons = models.BooleanField(default=False, verbose_name='Возможность добавок')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sizes',
        verbose_name='Товар'
    )

    size = models.CharField(
        max_length=1,
        choices=SIZE_CHOICES,
        verbose_name='Размер'
    )

    extra_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Наценка'
    )

    class Meta:
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товаров'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'],
                name='unique_product_size'
            )
        ]

    def __str__(self):
        return f'{self.product.name} — {self.size}'


class ProductAddon(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='addons',
        verbose_name='Товар'
    )

    name = models.CharField(max_length=100, verbose_name='Название добавки')

    extra_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Наценка'
    )

    is_available = models.BooleanField(default=True, verbose_name='Доступна')

    class Meta:
        verbose_name = 'Добавка'
        verbose_name_plural = 'Добавки'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'name'],
                name='unique_product_addon'
            )
        ]

    def __str__(self):
        return f'{self.product.name} — {self.name}'


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )

    order_item = models.OneToOneField(
        'orders.OrderItem',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='review',
        verbose_name='Позиция заказа'
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name='Оценка'
    )

    text = models.TextField(
        verbose_name='Текст отзыва'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.product.name}'