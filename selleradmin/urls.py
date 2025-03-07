from django.urls import path
from selleradmin import views

app_name = 'selleradmin'

urlpatterns = [
    path('seller-dashboard/', views.dashboard, name='seller-dashboard'),
    path('products/', views.product, name='products'),
    path('add-product/', views.add_product, name='add-product'),
    path('edit-product/<id>/', views.edit_product, name='edit-product'),
    path('delete-product/<id>/', views.delete_product, name='delete-product'),
    path('orders/', views.orders, name='orders'),
    path('order-details/<int:id>/', views.orders_detail, name='order-detail'),
    path('change-status/<int:id>/', views.change_order_status, name='change-status'),
    path('shop-page/', views.shop_page, name='shop-page'),
    path('reviews/', views.reviews, name='reviews'),

   
]
