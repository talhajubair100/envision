from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserCreateForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get_or_create(user=user)
    context = {'profile': profile, 'user': user}

    return render(request, 'account/profile.html', context)

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'account/edit_profile.html', context)


# @login_required    
# def create_profile(request):
#     form = ProfileForm()
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             return redirect('/')
#     context = {'form': form}
#     return render(request, 'account/create_profile.html', context)


@unauthenticated_user
def log_in_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            context = {
                'form': form,
                'error': "Invalid Email or Password!!",
            }
            return render(request, 'account/log_in.html', context)

    context = {

    }
    return render(request, 'account/log_in.html', context)


@unauthenticated_user
def sign_up_view(request):
    form = UserCreateForm()

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            user_profile = Profile.objects.get_or_create(user=user)
            
            subject = "Welcome to Y-Gaming BD"
            message = f"hi {user.username}, thanks for register this website"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            
            return redirect('log-in')

            messages.success(request, "Account was created for" + username)

            return redirect('log-in')
        messages.warning(request, "This Username or email already exist plz try again")
        
    context = {
        'form': form,
        'error': "This Username is already taken",
    }
    return render(request, 'account/sign_up.html', context)


def log_out_view(request):
    logout(request)
    return redirect('log-in')