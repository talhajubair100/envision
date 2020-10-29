from django.urls import path
from .views import *

urlpatterns = [
    path('', product_home, name='home'),
    path('search', serach_product, name='search'),
    path('category/<ctg_nam>', category_list, name='category_list'),
    path('product/detail/<int:pk>', product_detail, name='product-detail'),
    path('add-to-cart', AddToCartView.as_view(), name='add_to_cart'),
    path('cart-view', CartView.as_view(), name='cart_view'),
    #path('checkout', Checkout.as_view(), name='checkout'),
    path('checkout', checkout, name='checkout'),
    path('remove-cart-item/<int:cart_item_id>', RemoveFromCartView.as_view(), name='remove_cart_item'),



]