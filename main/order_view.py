from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from .models import Order, CancellationRequest
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem,ProductDB,User,Order
import razorpay
from decouple import config
import json


RAZOR_KEY_ID = config('RAZORPAY_KEY_ID')
RAZOR_CLIENT_SECRET = config('RAZORPAY_CLIENT_SECRET')


razorpay_client = razorpay.Client(
	auth=(RAZOR_KEY_ID, RAZOR_CLIENT_SECRET))

@csrf_exempt
def update_order_status(request, order_id,status):
    if request.method == "GET":
        new_status = status
        if not new_status:
            return JsonResponse({'error': 'No status provided'}, status=400)
        
        try:
            user_id = request.session.get("admin")
            if not user_id:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

            order = get_object_or_404(Order, order_id=order_id)
            order.order_status = new_status
            order.save()
            
            return JsonResponse({'message': f'Order {order_id} status updated to {new_status}'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
def refund_payment(payment_id, amount_to_refund):
    try:
        refund_data = {
            "amount": amount_to_refund,
            "speed": "normal"  
        }
        refund = razorpay_client.payment.refund(payment_id, refund_data)
        print(refund)
        return True
    except razorpay.errors.BadRequestError as e:
        return {"error": str(e)}
@csrf_exempt
def user_orders(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
        
        try:
            user = User.objects.get(uid=user_id)
            orders = Order.objects.filter(user=user).order_by('-order_date')
            orders_data = []
            for order in orders:

                order_data = {
                    "order_id": order.order_id,
                    "user": order.user.name,
                    "order_date": order.order_date,
                    "total_amount": order.total_amount,
                    "items": order.items,
                    "address":order.address,
                    "order_status":order.order_status,

                }
                orders_data.append(order_data)


            return JsonResponse({"orders": orders_data}, safe=False, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def all_orders(request):
    if request.method == "GET":
        try:
            orders = Order.objects.all().order_by('-order_date')
            orders_data = []

            for order in orders:

                order_data = {
                    "order_id": order.order_id,
                    "user": order.user.name,
                    "order_date": order.order_date,
                    "total_amount": order.total_amount,
                    "items": order.items,
                    "address":order.address,
                    "order_status":order.order_status,
                }
                orders_data.append(order_data)

            return JsonResponse({"orders": orders_data}, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def cancel_order(request, order_id):
    user = request.session.get("user_id")
    order = Order.objects.get(order_id=order_id)
    
    if refund_payment(order.payment_id, float(order.total_amount * 100)):
        order.order_status = "canceled"
        order.items = order.items.replace("'", '"')

        try:
            item = json.loads(order.items)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"JSON decode error: {str(e)}"}, status=400)

        product = ProductDB.objects.get(name=item["name"])
        
        quantity_list = product.quantity.split(":")
        index = 0
        for i in quantity_list:
            if str(item["quantity"]) == str(i):
                break
            index += 1

        stock_list = product.stock.split(":")
        updated_stock = int(stock_list[index]) + int(item["number"])
        stock_list[index] = str(updated_stock)
        product.stock = ":".join(stock_list)
        product.save()

        order.save()
        try:
            return JsonResponse({"message": f"Order {order_id} cancelled successfully and refund initiated."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "refund failed"}, status=500)


        
