from django.urls import path
from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('all-orders', all_order, name='all_orders'),
    path('download-data', download_data, name='download_data'),
    path('customer/<int:id>', customer, name='customer'),
    path('order/view/<int:id>', order_view, name='order_view'),
    path('order/delete/<int:id>', delete_order, name='delete_order'),
    path('order/delete/cancel/<int:id>', delete_order_undo, name='delete_order_undo'),
    path('order/delete/item', delete_order_view, name='delete_order_view'),
    path('product/list', ProductListView.as_view(), name='dashboard-product-list'),
    path('product/detail/<int:pk>', ProductDetailView.as_view(), name='dashboard-product-detail'),
    path('product/create', product_create, name='dashboard-product-create'),
    path('product/edit/<int:pk>', ProductEditView.as_view(), name='dashboard-product-edit'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='dashboard-product-delete'),
    path('category/list', CategoryListView.as_view(), name='dashboard-category-list'),
    path('category/create', category_create, name='dashboard-category-create'),
    path('category/edit/<int:pk>', CategoryEditView.as_view(), name='dashboard-category-edit'),
    path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='dashboard-category-delete'),
]
