from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from favorites.models import Favorite
from orders.models import OrderItem
from .forms import ReviewForm
from .models import Category, Product, Review


def get_favorite_product_ids(request):
    if request.user.is_authenticated:
        return set(
            Favorite.objects
            .filter(user=request.user)
            .values_list('product_id', flat=True)
        )

    return set()


def home(request):
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    )[:4]

    context = {
        'featured_products': featured_products,
        'favorite_product_ids': get_favorite_product_ids(request),
    }

    return render(
        request,
        'shop/home.html',
        context
    )


def catalog(request):
    categories = Category.objects.all()

    products = Product.objects.filter(
        is_available=True
    )

    category_slug = request.GET.get('category')

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    sort = request.GET.get(
        'sort',
        ''
    )

    show_new = request.GET.get('new') == '1'


    if category_slug:
        products = products.filter(
            category__slug=category_slug
        )

    if show_new:
        products = products.filter(
            is_new=True
        ).order_by('-id')

    if search_query:
        normalized_query = search_query.casefold()

        products = [
            product
            for product in products
            if normalized_query in product.name.casefold()
        ]


    if sort == 'price_asc':
        products = sorted(
            products,
            key=lambda product: product.price
        )

    elif sort == 'price_desc':
        products = sorted(
            products,
            key=lambda product: product.price,
            reverse=True
        )

    elif sort == 'name':
        products = sorted(
            products,
            key=lambda product: product.name.casefold()
        )


    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
        'search_query': search_query,
        'selected_sort': sort,
        'show_new': show_new,
        'favorite_product_ids': get_favorite_product_ids(request),
    }

    return render(
        request,
        'shop/catalog.html',
        context
    )



def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    reviews = (
        product.reviews
        .select_related('user')
        .all()
    )

    context = {
        'product': product,
        'reviews': reviews,
        'favorite_product_ids': get_favorite_product_ids(request),
    }

    return render(
        request,
        'shop/product_detail.html',
        context
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    if request.method == 'POST':
        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():
            form.save()

            return redirect(
                'product_detail',
                slug=review.product.slug
            )

    else:
        form = ReviewForm(
            instance=review
        )


    context = {
        'review': review,
        'form': form,
    }

    return render(
        request,
        'shop/edit_review.html',
        context
    )


@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    product_slug = review.product.slug

    review.delete()

    return redirect(
        'product_detail',
        slug=product_slug
    )

@login_required
def create_purchase_review(request, order_item_id):
    item = get_object_or_404(
        OrderItem.objects.select_related('order', 'product'),
        id=order_item_id,
        order__user=request.user,
        order__status='delivered',
        order__payment_status='paid',
        product__isnull=False,
    )

    if Review.objects.filter(order_item=item).exists():
        messages.info(
            request,
            'Вы уже оставили отзыв на эту покупку.'
        )
        return redirect('order_detail', order_id=item.order_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review, created = Review.objects.get_or_create(
                order_item=item,
                defaults={
                    'user': request.user,
                    'product': item.product,
                    'rating': form.cleaned_data['rating'],
                    'text': form.cleaned_data['text'],
                }
            )

            if created:
                messages.success(
                    request,
                    'Спасибо! Ваш отзыв опубликован.'
                )
            else:
                messages.info(
                    request,
                    'Отзыв на эту покупку уже существует.'
                )

            product_url = reverse(
                'product_detail',
                kwargs={'slug': item.product.slug}
            )

            return redirect(f'{product_url}#review-{review.id}')

    else:
        form = ReviewForm()

    return render(
        request,
        'shop/purchase_review.html',
        {
            'form': form,
            'item': item,
        }
    )


def about(request):
    return render(request, 'shop/about.html')


def delivery(request):
    return render(request, 'shop/delivery.html')


def contacts(request):
    return render(request, 'shop/contacts.html')