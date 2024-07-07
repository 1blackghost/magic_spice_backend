from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartItem,ProductDB,User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.shortcuts import get_object_or_404


def get_product(request, product_id):
    try:
        product = get_object_or_404(ProductDB, id=product_id)
        
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "category": product.category,
            "img": product.img,
            "description": product.description,
        }
        
        return JsonResponse(product_data)
    except:
        return JsonResponse({"status":"ok","message":"Item maynot be found"},status=200)


def get_all_products(request):
    products = ProductDB.objects.all().values()  
    products_list = list(products)  
    return JsonResponse(products_list, safe=False)

@csrf_exempt
@require_POST
def set_addr(request):
    try:
        data = json.loads(request.body)
        addr = data.get("address")
        if not addr:
            return JsonResponse({"error": "Address not provided"}, status=400)
        
        uid = request.session.get("user_id")
        if not uid:
            return JsonResponse({"error": "User not authenticated"}, status=401)
        
        user = User.objects.get(id=uid)
        user.address = addr
        user.save()
        
        return JsonResponse({"message": "Save successful"}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_addr(request):
    uid=request.session.get("user_id")
    user=User.objects.get(uid=uid)
    address=user.address
    return JsonResponse({"address":str(address)},status=200)
    
def find_valid_part(s):
    n = len(s)
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            substring = s[:i]
            if substring * (n // i) == s:
                return substring
    return s
def checkItemQuantity(request, value, qu):
    uid=request.session.get("user_id")
    user = User.objects.get(uid=uid)
    value=find_valid_part(str(value))
    print(value)
    try:
        product = ProductDB.objects.get(name=str(value))
        value = value.lower()
        qu = int(qu)
        
        if product.quantity > qu:
            return JsonResponse({"status":"true","message":"true"},status=200)
        else:
            return JsonResponse({"status":"false","message":"false"},status=200)
    except:
        return JsonResponse({"status":"Error!","message":"Something went wrong!"},status=500)
def get_cart(request):
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
            product = ProductDB.objects.get(name=str(value))
            p = qu * int(product.price)  
            cart.add_item(item_name=product.name, quantity=qu, price=p)
            cart.save()
            if (int(product.quantity)-qu)>-1:
            
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
