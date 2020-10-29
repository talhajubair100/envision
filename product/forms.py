from django import forms
from .models import Order

class OrderFrom(forms.ModelForm):
     class Meta:
         model = Order
         fields = ('phone', 'tranx_id', 'notes') 

         widgets = {
             'phone': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Mobile Number'}),
             'tranx_id': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bkash/Rocket Transaction ID'}),  
             'notes': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Order Notes'}),  
        }