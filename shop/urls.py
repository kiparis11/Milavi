from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('delivery/', views.delivery, name='delivery'),
    path('contacts/', views.contacts, name='contacts'),
    path('reviews/purchase/<int:order_item_id>/', views.create_purchase_review, name='create_purchase_review'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]