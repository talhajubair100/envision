from django.contrib.auth.models import User
from django.db import models
import decimal
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    feature_image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    new_price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    sell_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def total_price(self):
        cart_items = self.cart_item.all()
        price = cart_items.aggregate(total=Sum('price'))
        return price["total"]
        
    def __str__(self):
        return str(self.pk)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')

    def save(self, *args, **kwargs):
        self.price = self.item.new_price * decimal.Decimal(self.quantity)
        super().save(*args, **kwargs)

#    @property
#    def price(self):
#        return self.quantity * self.item.new_price

    def __str__(self):
        return self.item.name

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14, default="+880")
    tranx_id = models.CharField(max_length=50, default="TrxID :", unique=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    order_note = models.TextField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    
    def __str__(self):
        return self.cart.user.username
    
class PaymentInfo(models.Model):
    bkash = models.CharField(max_length=14)
    nogod = models.CharField(max_length=14)
    rocket = models.CharField(max_length=14)
    

    def __str__(self):
        return self.bkash
    

class BankInfo(models.Model):
    bank_name = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=15)

    def __str__(self):
        return self.bank_name