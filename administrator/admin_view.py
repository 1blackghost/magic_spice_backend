from django.shortcuts import render
from django.http import JsonResponse
from .models import Admin
from main.models import ProductDB,CartItem
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.db import transaction

def update_cart_item_prices(product):
    cart_items = CartItem.objects.filter(product_id=product.id)
    for item in cart_items:
        item.update_price()
        
@csrf_exempt      
def submit_data(request):
    if request.method == 'POST':
        if request.session.has_key("admin"):
            name = request.POST.get('name')
            quantity = request.POST.get('quantity')
            category = request.POST.get('category')
            price = request.POST.get('price')
            img1 = request.POST.get('img1')
            img2 = request.POST.get('img2')
            img3 = request.POST.get('img3')
            percentage = request.POST.get('percentage')
            delivery_fees = request.POST.get('delivery_fees')
            tax = request.POST.get('tax')
            other_fees = request.POST.get('other_fees')
            description = request.POST.get('description')
            shelf_life = request.POST.get('shelf_life')
            fssai_info = request.POST.get('fssai_info')
            key_features = request.POST.get('key_features')
            return_policy = request.POST.get('return_policy')
            customer_care = request.POST.get('customer_care')
            seller_details = request.POST.get('seller_details')
            disclaimer = request.POST.get('disclaimer')
            si_unit = request.POST.get('si_unit')
            stock = request.POST.get("stock")
            
            try:
                existing_product = ProductDB.objects.get(name=name)
                existing_product.name = name if name else existing_product.name
                existing_product.quantity = quantity if quantity else existing_product.quantity
                existing_product.category = category if category else existing_product.category
                existing_product.price = price if price else existing_product.price
                existing_product.img1 = img1 if img1 else existing_product.img1
                existing_product.img2 = img2 if img2 else existing_product.img2
                existing_product.img3 = img3 if img3 else existing_product.img3
                existing_product.percentage = percentage if percentage else existing_product.percentage
                existing_product.delivery_fees = delivery_fees if delivery_fees else existing_product.delivery_fees
                existing_product.tax = tax if tax else existing_product.tax
                existing_product.other_fees = other_fees if other_fees else existing_product.other_fees
                existing_product.description = description if description else existing_product.description
                existing_product.shelf_life = shelf_life if shelf_life else existing_product.shelf_life
                existing_product.fssai_info = fssai_info if fssai_info else existing_product.fssai_info
                existing_product.key_features = key_features if key_features else existing_product.key_features
                existing_product.return_policy = return_policy if return_policy else existing_product.return_policy
                existing_product.customer_care = customer_care if customer_care else existing_product.customer_care
                existing_product.seller_details = seller_details if seller_details else existing_product.seller_details
                existing_product.disclaimer = disclaimer if disclaimer else existing_product.disclaimer
                existing_product.si_unit = si_unit if si_unit else existing_product.si_unit
                existing_product.stock = stock if stock else existing_product.stock
                existing_product.save()

                update_cart_item_prices(existing_product)

                return JsonResponse({'success': True})
            except ProductDB.DoesNotExist:
                new_product = ProductDB(
                    name=name, 
                    quantity=quantity, 
                    category=category, 
                    price=price, 
                    img1=img1, 
                    img2=img2, 
                    img3=img3, 
                    percentage=percentage, 
                    delivery_fees=delivery_fees, 
                    tax=tax, 
                    other_fees=other_fees, 
                    description=description,
                    shelf_life=shelf_life,
                    fssai_info=fssai_info,
                    key_features=key_features,
                    return_policy=return_policy,
                    customer_care=customer_care,
                    seller_details=seller_details,
                    disclaimer=disclaimer,
                    si_unit=si_unit,
                    stock=stock
                )

                new_product.save()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def adminLogin(request):
    return render(request, 'admin_login.html')

def adminPanel(request):
    if "admin" in request.session:
        return render(request, 'admin_panel.html')

@csrf_exempt
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
