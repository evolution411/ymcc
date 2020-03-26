"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userApp import views as user_views
from django.contrib.auth import views as auth_views
# from userapp import views as user_views
# from userapp.views import register,activate_account
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blogApp.urls')),
    path('',include('videos.urls')),
    path('', include("news.urls")),
    #    path('activate/account/', user_views.activate_account, name='activate'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='user/password_management/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password_management/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/password_management/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_management/password_reset_complete.html'),
         name='password_reset_complete'),
	path('register/', user_views.SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
	# path('accounts/', include('django.contrib.auth.urls')),
	path('activate/<uidb64>/<token>/', user_views.ActivateAccount.as_view(), name='activate'),
    path('activated/', user_views.success_activate, name='success_registered'),
    path('actmessage/', user_views.activate_message, name='activation_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)