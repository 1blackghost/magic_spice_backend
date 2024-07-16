import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CartItem,Order
import json
from decouple import config
from .models import Cart, CartItem,ProductDB,User
import traceback


RAZOR_KEY_ID = config('RAZORPAY_KEY_ID')
RAZOR_CLIENT_SECRET = config('RAZORPAY_CLIENT_SECRET')


razorpay_client = razorpay.Client(
	auth=(RAZOR_KEY_ID, RAZOR_CLIENT_SECRET))


def getAmount(request):
    user=request.session.get("user_id")
    cart_items = CartItem.objects.filter(cart__user=user) 
    for item in cart_items:
        product = ProductDB.objects.get(id=item.product_id)
        index=0
        for i in product.quantity.split(":"):
            if str(item.quantity)==str(i):
                break
            index=index+1
        if not ((int(product.stock.split(":")[index])-int(item.number))>0):
            return JsonResponse({"message":"some of the items may have finished!"},status=400)
            

    total_amount = sum(item.price for item in cart_items)
    currency = 'INR'
    amount = total_amount*100

    request.session["amount"]=amount
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    data={}
    data['razorpay_order_id'] = razorpay_order_id
    data['razorpay_merchant_key'] = RAZOR_KEY_ID
    data['razorpay_amount'] = amount
    data['currency'] = currency
    data['callback_url'] = callback_url
    return JsonResponse(data)


def delete_all_items(user):
    try:
        cart_items = CartItem.objects.filter(cart__user=user)
        cart_items.delete()
        return JsonResponse({"status": "ok", "message": "All items deleted from cart."}, status=200)
    except Exception as e:
        return JsonResponse({"status": "bad", "error": str(e)}, status=500)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            signature = data.get('razorpay_signature')
            razorpay_order_id = data.get('razorpay_order_id')
            payment_id = data.get('razorpay_payment_id')
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result is not None:
                user_id = request.session.get("user_id")
                user = User.objects.get(pk=user_id)

                cart_items = CartItem.objects.filter(cart__user=user)
                if not cart_items.exists():
                    return JsonResponse({"message": "No items in the cart!"}, status=400)

                for item in cart_items:
                    # Prepare order details for each item
                    item_details = {
                        "name": item.item,
                        "price": item.price,
                        "image": item.img,
                        "quantity": item.quantity,
                        "number": item.number
                    }

                    # Update stock quantities
                    product = ProductDB.objects.get(id=item.product_id)
                    quantities = product.quantity.split(":")
                    stock_values = product.stock.split(":")

                    for i, qty in enumerate(quantities):
                        if str(item.quantity) == str(qty):
                            stock_value = int(stock_values[i])
                            stock_value -= int(item.number)
                            stock_values[i] = str(stock_value)
                            break
                    
                    product.stock = ":".join(stock_values)
                    product.save()

                    # Create a separate order for each cart item
                    order = Order.objects.create(
                        user=user,
                        total_amount=item.price,
                        items=item_details,
                        address=user.address,
                        payment_id=payment_id,
                        order_status="ordered"
                    )

                    order.save()

                # Delete all cart items after processing
                cart_items.delete()

                return JsonResponse({"message": "Payment completed and orders placed successfully!"}, status=200)
            else:
                return JsonResponse({"message": "Payment signature verification failed!"}, status=400)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)