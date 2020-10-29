from django import template
from product.models import Item, CartItem, Cart

register = template.Library()

@register.simple_tag
def my_cart_items(username):
    items = CartItem.objects.filter(cart__user__username=username, cart__is_active=True)
   
    return {'items': items, 'count': items.count()}

# @register.filter
# def my_cart_items_count(request):
#     cart = Cart.objects.get(user=request.user ,is_active=True)
#     items = CartItem.objects.filter(cart)
       
#     return items.count()



# @register.filter
# def cart_item_count(user):
#     if user.is_authenticated:
#         qs = Cart.objects.filter(user=user, is_active=True)
#         if qs.exists():
#             return qs[0].cart_item.item.count()

#     return 0
    