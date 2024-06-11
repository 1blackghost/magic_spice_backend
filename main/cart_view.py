from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartItem,ProductDB,User

def find_valid_part(s):
    n = len(s)
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            substring = s[:i]
            if substring * (n // i) == s:
                return substring
    return s


def get_cart(request):
    user = request.session.get("user")
    try:
        uid=request.session.get("user_id")
        user = User.objects.get(uid=uid)
        cart_items = CartItem.objects.filter(cart__user=user)
        cart_data = [{'item': item.item, 'quantity': item.quantity, 'price': item.price} for item in cart_items]
        return JsonResponse({'cart': cart_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def cart(request, value, qu):
    uid=request.session.get("user_id")
    user = User.objects.get(uid=uid)
    value=find_valid_part(str(value))
    print(value)
    try:
        cart, created = Cart.objects.get_or_create(user=user)
        value = value.lower()
        qu = int(qu)
        
        if qu > 0:
            product = ProductDB.objects.get(code=str(value))
            p = qu * int(product.price)  
            cart.add_item(item_name=product.name, quantity=qu, price=p)
            cart.save()
            if (int(product.quantity)-qu)>-1:
                product.quantity = int(product.quantity) - qu
            
                product.save()
            else:
                return JsonResponse({"status":"bad","message":"item finished!"},status=400)
            
            if created:
                return JsonResponse({"status": "ok", "message": "Item added to cart."}, status=200)
            else:
                return JsonResponse({"status": "ok", "message": "Item quantity updated in cart."}, status=200)
        else:
            return JsonResponse({"status": "bad", "error": "Invalid quantity. Quantity must be greater than 0."}, status=400)
    except ValueError:
        return JsonResponse({"status": "bad", "error": "Invalid quantity format. Please provide a valid integer."}, status=400)
    except ProductDB.DoesNotExist:
        return JsonResponse({"status": "bad", "error": "Product not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "bad", "error": str(e)}, status=500)

def delete(request, value):
    try:
        uid=request.session.get("user_id")
        user = User.objects.get(uid=uid)
        cart, created = Cart.objects.get_or_create(user=user)
        cart.remove_item(item_name=value)
        cart.save()
        return JsonResponse({"status": "ok"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "bad"}, status=500)
