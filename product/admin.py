from django.contrib import admin
from .models import Category, Item, Cart, CartItem, Order, PaymentInfo, BankInfo

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(PaymentInfo)
admin.site.register(BankInfo)



