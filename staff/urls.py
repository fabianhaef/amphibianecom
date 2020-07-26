from . import views
from django.urls import path


app_name = 'staff'

urlpatterns = [
    path('', views.StaffView.as_view(), name='staff'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
    path('products/<pk>/update', views.ProductUpdateView.as_view(), name='product-update')
]