from django.urls import path

from . import views
urlpatterns=[
    path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('register/', views.registration_view, name='register'),
path('password-forget/', views.password_forget_view, name='password-forget'),
path('password-reset/', views.password_reset_view, name='password-reset'),
path('delete-account-request/', views.delete_account_request, name='delete-account-request'),
path('delete-account-confirm/<str:uidb>/<str:token>', views.delete_account_confirm, name='delete-account-confirm'),
path('password-reset-for-logged-in/', views.password_reset_for_logged_in, name='password-reset-for-logged-in'),

path('activate/<str:uidb>/<str:token>', views.activation_view, name='activate'),
path('reset/<str:uidb>/<str:token>', views.reset_password_view, name='password_reset_confirm'),
path('activate-later/', views.account_activation_later, name='account-activation-later'),
path('profile/', views.profile_view, name='edit-profile'),
]