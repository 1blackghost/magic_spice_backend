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
from . import server_admin,admin_view


urlpatterns = [
    path("adminA/<str:server_password>/<str:username>/<str:password>",server_admin.add,name="add_admin"),
    path("admin",admin_view.adminPanel,name="admin"),
    path('submit_data', admin_view.submit_data, name='submit_data'),
    path("adminL",admin_view.adminL,name="adminL"),
    
    
]