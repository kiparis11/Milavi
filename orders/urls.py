from django.urls import path

from . import views


urlpatterns = [
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'payment/demo/<int:order_id>/',
        views.demo_payment,
        name='demo_payment'
    ),

    path(
        'payment/demo/<int:order_id>/process/',
        views.process_demo_payment,
        name='process_demo_payment'
    ),

    path(
        'orders/success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'orders/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    path(
        'orders/<int:order_id>/cancel/',
        views.cancel_order,
        name='cancel_order'
    ),
]