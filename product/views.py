from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from .models import Item, Category, Cart, CartItem, Order
from django.http import HttpResponse
from .forms import OrderFrom
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

def product_home(request):
    items = Item.objects.all()
    featured_products = Item.objects.all().order_by('-sell_count')[:4]
    context = {
        'items': items,
        'featured_products': featured_products,
    }
    return render(request, 'home.html', context)


def serach_product(request):
    if request.method == 'POST':
        search_keyword = request.POST['search_keyword']
        serach_items = Item.objects.filter(name__contains=search_keyword)
        return render(request, 'product/product_search.html', {'serach_items': serach_items, 'serch_key': search_keyword})
    return render(request, 'product/product_search.html')


def category_list(request, ctg_nam):
    ctg_obj = Category.objects.get(name=ctg_nam)
    item_list = Item.objects.filter(category=ctg_obj)
    context = {'ctg_items': item_list, 'category_name': ctg_nam}
    return render(request, 'product/product_by_category.html', context)



def product_detail(request, pk):
    try:
        product_detail = Item.objects.get(pk=pk)
        r_product = Item.objects.filter(category=product_detail.category).order_by('-sell_count')[:4]
        context = {
            'product': product_detail,
            'r_product': r_product,
        }
        return render(request, 'product/product_detail.html', context)
    except:
        return render(request, '404.html')


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request):
        qty = request.GET.get('quantity', 1)
        item_id = request.GET.get('item_id')
        item = Item.objects.get(pk=item_id)

        cart_obj, created = Cart.objects.get_or_create(user=request.user, is_active=True)

        item, created = CartItem.objects.get_or_create(item=item, cart=cart_obj, defaults={'quantity':qty})
        if not created:
            item.quantity = item.quantity + int(qty)
            item.save()

        

        #CartItem.objects.create(item=item, quantity=qty, cart=cart_obj)
        messages.success(request, 'Item Add to cart')

        return redirect('cart_view')

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            #cart = Cart.objects.get(user=request.user, is_active=True)
            cart_item = get_object_or_404(Cart, user=request.user, is_active=True)
            items = CartItem.objects.filter(cart=cart_item)
            context = {'cart': cart_item, 'items': items}
            return render(request, 'product/add_to_cart.html', context)
        except:
            return redirect('home')

class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, cart_item_id):
        item = get_object_or_404(CartItem, pk=cart_item_id)
        item.delete()
        messages.warning(request, "Your cartitem has been removed") 
        return redirect('/')

# class Checkout(LoginRequiredMixin, View):
#     def get(self, request):
#         cart = Cart.objects.get(user=request.user, is_active=True)
#         items = CartItem.objects.filter(cart=cart)
#         form = OrderFrom()
        
#         context = {
#             'cart': cart,
#             'items': items,
#             'form': form
#         }
#         return render(request, 'product/checkout.html', context)
    
        
    # def post(self, request):
    #     forms = OrderFrom()
    #     if forms.is_valid():


# class Order(LoginRequiredMixin, View):
#     def get(self, request):
#         cart = Cart.objects.get(user=request.user, is_active=True)

#         phone = request.GET.get('phone')
#         tranx_id = request.GET.get('tranx_id')
#         order_note = request.GET.get('notes')

#         print(phone, tranx_id, order_note, cart)
#         order = Order.objects.create(cart=cart, phone=phone, tranx_id=tranx_id, notes=order_note, ordered=False)
#         if order:
#             cart.is_active = False
#             cart.save()

#         messages.success(request, 'Thanks For Order')
#         return redirect('/')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user, is_active=True)
    items = CartItem.objects.filter(cart=cart)
    total_amount = cart.total_price
    print("total price is", total_amount())
    print("cart id is", cart)
    
    

    form = OrderFrom()
    if request.method == "POST":
        form = OrderFrom(request.POST)
        if form.is_valid():
            order_form = form.save(commit=False)
            order_form.cart = cart
            cart.is_active = False
            
            cart.save()
            order_form.save()

            for qty_item in items:
                item_qty = qty_item.quantity
                print("item qty", item_qty)
                item_sell = Item.objects.get(name=qty_item.item.name)
                print(item_sell)
                item_sell_count = item_sell.sell_count
                item, created = Item.objects.get_or_create(name=item_sell, defaults={'sell_count':item_qty})
                if not created:
                    item.sell_count = item.sell_count + int(item_qty)
                    item.save()

            
            subject = "Welcome to Y-Gaming BD"
            message = f"Hi {request.user.username}, Thanks for order \n Your total bill amount {total_amount()} TK. We will confirm your order as soon as possible"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email, ]
            send_mail(subject, message, email_from, recipient_list)    
            
       
            return redirect('/')
    
    

    context = {
             'cart': cart,
             'items': items,
             'form': form
         }
       
    return render(request, 'product/checkout.html', context)


# item_sell, created = Item.objects.get_or_create(sell_count=qty)
#         if not created:
#             item_sell.sell_count = item_sell.sell_count + int(qty)
#             item_sell.save()

# print("items qunatity is", item_qty)
#         print("items name is", qty_item.item.name)
#         print("items id is", qty_item.item.id)
#         print('name : ', item_sell)
#         print('id : ', item_sell.id)
#         print('sell count : ', item_sell.sell_count)


#  