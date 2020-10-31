from django import forms
from product.models import Item, Category, Order, PaymentInfo, BankInfo


class ProductForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'new_price', 'old_price', 'in_stock', 'sell_count', 'category', 'feature_image')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'new_price': forms.TextInput(attrs={'class': 'form-control'}),
            'old_price': forms.TextInput(attrs={'class': 'form-control'}),
            'in_stock': forms.CheckboxInput(),
            'sell_count': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'feature_image': forms.FileInput(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('phone', 'tranx_id', 'notes', 'order_note', 'ordered')

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tranx_id': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'order_note': forms.TextInput(attrs={'class': 'form-control'}),
            'ordered': forms.CheckboxInput()
        }
       

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = '__all__'

        widgets = {
            'bkash': forms.TextInput(attrs={'class': 'form-control'}),
            'nogod': forms.TextInput(attrs={'class': 'form-control'}),
            'rocket': forms.TextInput(attrs={'class': 'form-control'}),

        }

class BankPaymetForm(forms.ModelForm):
    class Meta:
        model = BankInfo
        fields = '__all__'

        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),

        }