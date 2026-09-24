from django.urls import path

from . import views


urlpatterns = [
    path(
        'cart/',
        views.cart_detail,
        name='cart_detail'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/change/<int:item_id>/<str:action>/',
        views.change_quantity,
        name='change_cart_quantity'
    ),

    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
]