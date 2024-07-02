from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User, Verify_Email, Cart,CartItem
from . import helper
import time
from django.views.decorators.csrf import csrf_protect
import json
from . import  custom_settings

url="127.0.0.1:8000/"

def dash(request):
    if request.session.get("user_id"):
        uid=request.session.get("user_id")
        user = User.objects.get(uid=uid)
        cart_items = CartItem.objects.filter(cart__user=user)
        cart_count = cart_items.count()
        context = {
            'user_name': user.name,
            'cart_count': cart_count
        }
        return JsonResponse(context)
    else:
        return JsonResponse({"message": "User not logged in"}, status=401)


def get_csrf(request):
    csrf_token = get_token(request)
    request.session["csrf"]=str(csrf_token)
    request.session.save()
    return JsonResponse({'csrf_token': csrf_token})


def verify(request, hash_value):
    try:
        verify_email = Verify_Email.objects.get(hash=hash_value)
        user = User.objects.get(email=verify_email.email)
        request.session.clear()
        request.session["user_id"] = user.uid
        user.email_verified = True
        user.save()
        verify_email.delete()
        Cart.objects.create(user=user)

        return JsonResponse({"message": "Verification completed!"}, status=200)
    except Verify_Email.DoesNotExist:
        return JsonResponse({"message": "Invalid verification link"}, status=400)

def resend(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"message": "You're not logged in."}, status=400)

    verification_started = request.session.get("verification_started")
    if verification_started:
        timer_duration = 10
        current_time = time.time()
        last_request_time = request.session.get("last_request_time", current_time)
        elapsed_time = current_time - last_request_time
        
        if elapsed_time >= timer_duration:
            request.session["last_request_time"] = current_time
            user = User.objects.get(uid=user_id)
            verify_email, created = Verify_Email.objects.get_or_create(email=user.email)
            
            verify_email.generate_unique_hash()
            send_verification_email(user.email, url+verify_email.hash)
            
            return JsonResponse({"message": "Verification email sent"}, status=200)
        else:
            return JsonResponse({"message": "Time has not elapsed yet"}, status=400)
    else:
        return JsonResponse({"message": "Verification not started"}, status=400)

def unverified(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"message": "You're not logged in."}, status=400)

    verification_started = request.session.get("verification_started")
    if verification_started:
        timer_duration = 10
        current_time = time.time()
        last_request_time = request.session.get("last_request_time", current_time)
        elapsed_time = current_time - last_request_time
        remaining_time = max(timer_duration - elapsed_time, 0)
        
        user = User.objects.get(uid=user_id)
        if not request.session.get("last_request_time"):
            verify_email, created = Verify_Email.objects.get_or_create(email=user.email)
            verify_email.generate_unique_hash()
            send_verification_email(user.email, url+verify_email.hash)
        
        request.session["last_request_time"] = current_time
        formatted_email = format_email(user.email)
        
        return JsonResponse({"email": formatted_email, "timer_duration": remaining_time})
    else:
        return JsonResponse({"message": "Verification not started"}, status=400)

def format_email(email):
    local_part, domain = email.split("@")
    obscured_local_part = local_part[0] + "*" * (len(local_part) - 1)
    return f"{obscured_local_part}@{domain}"

def send_verification_email(email, hash_value):
    url = f"http://127.0.0.1:8000/verify/{hash_value}"
    helper.send_verification_email(email, url)

def logout(request):
    if request.session.get("user_id"):
        request.session.clear()
        return JsonResponse({"message": "Logged out successfully"}, status=200)
    else:
        return JsonResponse({"message": "No account found"}, status=400)


@csrf_exempt
def login(request):
    if request.method == "POST":
        origin = request.META.get('HTTP_ORIGIN')
        csrf=request.META.get('HTTP_X_CSRFTOKEN')
        saved_csrf=request.session.get("csrf")
        print(saved_csrf)

        if origin in custom_settings.origins:

            data=json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    if user.email_verified:
                        request.session["user_id"] = user.uid
                        return JsonResponse({"message": "success"}, status=200)
                    else:
                        request.session["user_id"] = user.uid
                        request.session["verification_started"] = True
                        request.session["email"] = user.email
                        return JsonResponse({"message": "verify"}, status=200)
                else:
                    return JsonResponse({"message": "Incorrect password"}, status=401)
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist"}, status=404)
            except Exception as e:
                return JsonResponse({"message": "Something went wrong:("}, status=500)
        else:
            return JsonResponse({"message":"Forbidden"},status=403)

@csrf_exempt
def signup(request):
    if request.method == "POST":
        origin = request.META.get('HTTP_ORIGIN')
        csrf=request.META.get('HTTP_X_CSRFTOKEN')
        saved_csrf=request.session.get("csrf")

        print(saved_csrf)
        if origin in custom_settings.origins:
            
            data=json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            
            additional_params = request.POST.get('additional_params')
            try:
                new_user = User(name=name, email=email, password=make_password(password), additional_params=additional_params)
                new_user.save()
                print("Success account created!")
                return JsonResponse({'message': 'success'}, status=200)
            except Exception as e:
                print(str(e))
                return JsonResponse({"message": "Something went wrong:("}, status=500)
        else:
            return JsonResponse({"message":"Forbidden"},status=403)
