from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from .models import Order, CancellationRequest
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem,ProductDB,User,Order


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
                }
                orders_data.append(order_data)

            return JsonResponse({"orders": orders_data}, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def cancel_order(request, order_id):
    if request.method == "POST":
        user = request.session.get("user")
        order = get_object_or_404(Order, order_id=order_id, user=user)

        try:
            cancellation_request = CancellationRequest(order=order, reason="Customer requested cancellation")
            cancellation_request.save()

            order.delete()

            return JsonResponse({"message": f"Order {order_id} cancelled successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)