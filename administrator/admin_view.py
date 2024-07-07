from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from .models import Admin
from main.models import ProductDB
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.middleware.csrf import get_token
from .models import Admin
from django.contrib.auth.hashers import make_password, check_password
import time


        

def submit_data(request):
    if request.method == 'POST':
        if request.session.has_key("admin"):
            name = request.POST.get('name')
            quantity = request.POST.get('quantity')
            category = request.POST.get('category')
            price = request.POST.get('price')
            img = request.POST.get('img')
            description=request.POST.get("description")
            
            try:
                existing_product = ProductDB.objects.get(name=name)
                existing_product.name = name
                existing_product.quantity = quantity
                existing_product.category = category
                existing_product.price = price
                existing_product.img=img
                existing_product.description=description
                existing_product.save()
                return JsonResponse({'success': True})
            except ProductDB.DoesNotExist:
                new_product = ProductDB(name=name, quantity=quantity, category=category, price=price, img=img,description=description)
                new_product.save()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def adminPanel(request):
    if request.session.has_key("admin"):
        return  JsonResponse({"success":True,"message":"admin logged in"},status=200)  
    else:
        return JsonResponse({"success":True,"message":"admin not logged in"},status=403)  


def adminL(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Admin.objects.get(email=email)
            if check_password(password, user.password):
                request.session["admin"] = user
                return JsonResponse({"message": "success"}, status=200)
    
            else:
                return JsonResponse({"message": "Incorrect password"}, status=401)
        except Admin.DoesNotExist:
            return JsonResponse({"message": "Admin does not exist"}, status=404)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Something went wrong:("}, status=500)
