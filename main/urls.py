"""
URL configuration for miniproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from . import auth,cart_view

urlpatterns = [
    path('get_csrf', auth.get_csrf, name='get_csrf'),
    path('get_cart', auth.get_cart, name='get_cart'),
    path('verify/<str:hash_value>', auth.verify, name='verify'),
    path('resend', auth.resend, name='resend'),
    path('unverified', auth.unverified, name='unverified'),
    path('logout', auth.logout, name='logout'),
    path('dash', auth.dash, name='dash'),
    path('login', auth.login, name='login'),
    path('signup', auth.signup, name='signup'),
]
