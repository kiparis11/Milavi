from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from shop.models import Product

from .models import Favorite


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'product',
        'product__category'
    )

    context = {
        'favorites': favorites,
    }

    return render(request, 'favorites/favorite_list.html', context)


@login_required
@require_POST
def toggle_favorite(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        product=product
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            product=product
        )

    next_url = request.POST.get('next')

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()}
    ):
        return redirect(next_url)

    return redirect('catalog')
