from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from .models import Order, CancellationRequest
from django.shortcuts import get_object_or_404



@csrf_exempt
def user_orders(request):
    if request.method == "GET":
        user = request.session.get("user_id")
        orders = Order.objects.filter(user=user)
        orders_data = list(orders.values()) 
        return JsonResponse(orders_data, safe=False) 
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def all_orders(request):
    if request.method == "GET":
        orders = Order.objects.all()
        orders_data = list(orders.values())  
        return JsonResponse(orders_data, safe=False) 
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