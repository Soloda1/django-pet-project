import profile
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('email-verification-sent/', email_verification_sent, name='email-verification-sent'),

    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('dashboard/', dashboard_user, name='dashboard'),
    path('profile-management/', profile_user, name='profile-management'),
    path('delete-user/', delete_user, name='delete-user'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password_reset.html',
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')),
        name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password_reset_done.html'),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')),
        name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password_reset_complete.html'),
        name='password_reset_complete'),


]