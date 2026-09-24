from django.contrib import admin

from .models import Category, Product, ProductSize, ProductAddon, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 0

class ProductAddonInline(admin.TabularInline):
    model = ProductAddon
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'is_available',
        'is_featured',
        'is_new',
        'has_sizes',
        'has_temperature',
        'has_addons',
        'created_at',
    )

    list_filter = (
        'category',
        'is_available',
        'is_featured',
        'is_new',
        'has_sizes',
        'has_temperature',
        'has_addons',
    )

    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    inlines = [
        ProductSizeInline,
        ProductAddonInline,
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'rating',
        'created_at',
        'order_item',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'product__name',
        'user__username',
        'text',
    )
