from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart', views.CartView.as_view(), name='summary'),
    path('remove-from-cart/<pk>', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
]