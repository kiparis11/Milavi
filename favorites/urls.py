from django.urls import path

from . import views


urlpatterns = [
    path(
        'favorites/',
        views.favorite_list,
        name='favorite_list'
    ),

    path(
        'favorites/toggle/<int:product_id>/',
        views.toggle_favorite,
        name='toggle_favorite'
    ),
]