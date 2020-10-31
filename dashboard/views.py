from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from product.models import *
from account.models import Profile
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import ProductForm, CategoryForm, OrderUpdateForm, PaymentForm, BankPaymetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_users, admin_only
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import csv
from django.http import HttpResponse



@login_required
@admin_only
def dashboard(request):
    orders = Order.objects.filter(is_delete=False)
    orders_list = Order.objects.filter(is_delete=False).order_by('-date_created')[0:10]
    customer = Profile.objects.all()

    order_done = Order.objects.filter(ordered=True, is_delete=False).count()
    order_pending = Order.objects.filter(ordered=False, is_delete=False).count()

    context = {
        'orders': orders_list, 'customer': customer, 'order_done': order_done, 
        'order_pending': order_pending, 'customer_count': customer.count(), 'total_order': orders.count(),

    }


    return render(request, 'dashboard/dashboard.html', context)


@login_required
@admin_only
def all_order(request):
    orders = Order.objects.filter(ordered=True, is_delete=False).order_by('-date_created')
    
    context = {
        'all_order': orders
    }
    return render(request, 'dashboard/all_order.html', context)



@login_required
@admin_only
def download_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment ; filename="all_order.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'TranxID', 'Date', 'Item', 'Quantity', 'Total'])


    order_list = Order.objects.filter(ordered=True, is_delete=False).order_by('-date_created').values_list('cart__user__username', 'cart__user__email', 'phone', 'tranx_id', 'date_created', 'cart__cart_item__item__name', 'cart__cart_item__quantity', 'cart__cart_item__price')

    for mah_order in order_list:
        writer.writerow(mah_order)

    return response


@login_required
@admin_only
def customer(request, id):
    customer_profile = Profile.objects.get(id=id)
    
    customer_order = Order.objects.filter(cart__user__id = customer_profile.user.id, is_delete=False)
    
    context = {'customer_profile': customer_profile, 'customer_order_count': customer_order.count(),
             'customer_order': customer_order
    }
    return render(request, 'dashboard/customer.html', context)


@login_required
@admin_only
def order_view(request, id):

    order_obj = Order.objects.get(id=id)
    
    form = OrderUpdateForm(instance=order_obj)
    
    if request.method == 'POST':
	    form = OrderUpdateForm(request.POST, instance=order_obj)
	    if form.is_valid():
                form.save()
                order_note = form.cleaned_data['order_note']
                if order_obj.ordered  == True:
                        user_mail = order_obj.cart.user.email
                        subject = "Welcome to Y-Gaming BD"
                        message = f"Hi {order_obj},\nThanks for your order. Your order is done,\n{order_note}"
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [user_mail, ]
                        send_mail(subject, message, email_from, recipient_list)
                return redirect('dashboard')
                

    context = {
        'order_obj': order_obj,
        'form': form
    }
    return render(request, 'dashboard/order_view.html', context)


@login_required
@admin_only
def delete_order(request, id):
    del_order = Order.objects.get(id=id)
    del_order.is_delete = True
    del_order.save()
    return redirect('dashboard')


@login_required
@admin_only
def delete_order_undo(request, id):
    del_order_undo = Order.objects.get(id=id)
    del_order_undo.is_delete = False
    del_order_undo.save()
    return redirect('dashboard')


@login_required
@admin_only
def delete_order_view(request):
    del_orders = Order.objects.filter(is_delete=True)
    context = {
        'del_orders' : del_orders
    }
    return render(request, 'dashboard/order_del_view.html', context)
    

@method_decorator(admin_only, name='dispatch')
class ProductListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'dashboard/product_list.html'
    context_object_name = 'products'


@method_decorator(admin_only, name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'dashboard/product_detail.html'
    context_object_name = 'product'


@login_required
@allowed_users(allowed_roles=['admin'])
def product_create(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product-list')
    context = {
        'form': form,
        'error': "Form is invalid",
    }
    return render(request, 'dashboard/product_form.html', context)


@method_decorator(admin_only, name='dispatch')
class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'dashboard/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('dashboard-product-list')


@method_decorator(admin_only, name='dispatch')
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'dashboard/product_delete.html'
    success_url = reverse_lazy('dashboard-product-list')
    context_object_name = 'product'


@method_decorator(admin_only, name='dispatch')
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    fields = '__all__'
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'


@login_required
@admin_only
def category_create(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard-category-list')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/category_form.html', context)


@method_decorator(admin_only, name='dispatch')
class CategoryEditView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'dashboard/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard-category-list')


@method_decorator(admin_only, name='dispatch')
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/category_delete.html'
    success_url = reverse_lazy('dashboard-category-list')
    context_object_name = 'categorie'


@login_required
@admin_only
def payment_info_create(request):
    form = PaymentForm()
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/payment_info.html', context)

@method_decorator(admin_only, name='dispatch')
class PaymentInfoListView(LoginRequiredMixin, ListView):
    model = PaymentInfo
    fields = '__all__'
    template_name = 'dashboard/payment_list.html'
    context_object_name = 'payments_info'


@method_decorator(admin_only, name='dispatch')
class PaymentInfoEditView(LoginRequiredMixin, UpdateView):
    model = PaymentInfo
    template_name = 'dashboard/payment_info.html'
    form_class = PaymentForm
    success_url = reverse_lazy('payment_info_list')


@login_required
@admin_only
def bank_info_create(request):
    form = BankPaymetForm()
    if request.method == "POST":
        form = BankPaymetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_info_list')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/bank_info.html', context)

@method_decorator(admin_only, name='dispatch')
class BankInfoListView(LoginRequiredMixin, ListView):
    model = BankInfo
    fields = '__all__'
    template_name = 'dashboard/bank_info_list.html'
    context_object_name = 'bank_info'


@method_decorator(admin_only, name='dispatch')
class BankInfoEditView(LoginRequiredMixin, UpdateView):
    model = BankInfo
    template_name = 'dashboard/bank_info.html'
    form_class = BankPaymetForm
    success_url = reverse_lazy('bank_info_list')
