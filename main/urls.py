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

from . import auth,cart_view,payment_view,order_view

urlpatterns = [
    path('get_csrf', auth.get_csrf, name='get_csrf'),
    path('verify/<str:hash_value>', auth.verify, name='verify'),
    path('resend', auth.resend, name='resend'),
    path('unverified', auth.unverified, name='unverified'),
    path('logout', auth.logout, name='logout'),
    path('dash', auth.dash, name='dash'),
    path('login', auth.login, name='login'),
    path('signup', auth.signup, name='signup'),
    path('get_cart', cart_view.get_cart, name='get_cart'),
    path('cart/<str:value>/<int:number>/<int:qu>', cart_view.cart, name='cart'),
    path('delete/<str:value>/<str:price>', cart_view.delete, name='delete'),
    path("getaddr",cart_view.get_addr,name="getaddr"),
    path("setaddr",cart_view.set_addr,name="setaddr"),
    path("products",cart_view.get_all_products,name="products"),
    path('getAmount', payment_view.getAmount, name='get_amount'),
    path('paymenthandler', payment_view.paymenthandler, name='payment_handler'),
    path('user_orders', order_view.user_orders, name='user_orders'),
    path('all_orders', order_view.all_orders, name='all_orders'),
    path('cancel/<int:order_id>', order_view.cancel_order, name='cancel_order'),
    path('product/<int:product_id>', cart_view.get_product, name='get_product'),
    path('update_order_status/<int:order_id>/<str:status>', order_view.update_order_status, name='update_order_status'),

]