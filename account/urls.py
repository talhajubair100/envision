from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
   # path('create-profile', create_profile, name='create_profile'),
    path('profile', profile, name='profile'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('login', log_in_view, name='log-in'),
    path('logout', log_out_view, name='log-out'),
    path('signup', sign_up_view, name='sign-up'),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),
    path('password-reset-sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'), name='password_reset_confirm'),
    path('password-reset-done', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'), name='password_reset_complete'),

]