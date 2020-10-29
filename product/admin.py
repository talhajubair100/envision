from django.contrib import admin
from .models import Category, Item, Cart, CartItem, Order

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)

