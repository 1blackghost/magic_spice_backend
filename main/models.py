from django.db import models
import hashlib
import random
import string
class ProductDB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.CharField(max_length=10, default=None)
    category = models.CharField(max_length=10, default=None)
    img1 = models.CharField(max_length=100, default=None)
    img2 = models.CharField(max_length=100, default=None)
    img3 = models.CharField(max_length=100, default=None)
    percentage = models.CharField(max_length=100, default=None)
    delivery_fees = models.CharField(max_length=100, default=None)
    tax = models.CharField(max_length=100, default=None)
    other_fees = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=1000, default="No Description")
    shelf_life = models.CharField(max_length=1000, default=None, null=True)
    fssai_info = models.CharField(max_length=1000, default=None, null=True)
    key_features = models.CharField(max_length=1000, default=None, null=True)
    return_policy = models.CharField(max_length=1000, default=None, null=True)
    customer_care = models.CharField(max_length=1000, default=None, null=True)
    seller_details = models.CharField(max_length=1000, default=None, null=True)
    disclaimer = models.CharField(max_length=1000, default=None, null=True)
    si_unit = models.CharField(max_length=100, default=None, null=True)
    stock = models.CharField(max_length=100,default=None,null=True)

    def __str__(self):
        return self.name


class User(models.Model):
    uid = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100,unique=False)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128)  
    email_verified = models.BooleanField(default=False) 
    address=models.TextField(default=None,null=True)
    additional_params = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
    

class Verify_Email(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    def generate_unique_hash(self):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        unique_hash = hashlib.sha256((self.email + random_string).encode()).hexdigest()
        self.hash = unique_hash
        self.save()

    def __str__(self):
        return self.email
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def add_item(self, item_name, quantity,price,img,product_id,number,tax,other_fees,discount,delivery_fees):

        CartItem.objects.create(cart=self, item=item_name, quantity=quantity, price=price,img=img,product_id=product_id,number=number,tax=tax,other_fees=other_fees,discount=discount,delivery_fees=delivery_fees)

    def remove_item(self, item,price):
        self.cartitem_set.filter(item=item,price=price).delete()

    def get_quantity(self, item_name):
        item = self.cartitem_set.filter(item=item_name).first()
        return item.quantity if item else 0



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    img=models.CharField(max_length=100,null=True)
    product_id=models.CharField(max_length=100,null=True)
    number=models.CharField(max_length=100,null=True)
    tax=models.CharField(max_length=100,null=True)
    delivery_fees=models.CharField(max_length=100,null=True)
    discount=models.CharField(max_length=100,null=True)
    other_fees=models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"{self.quantity} x {self.item} in cart for {self.cart.user.username}"
    def update_price(self):
        product = ProductDB.objects.get(id=self.product_id)
        index = 0
        for i in product.quantity.split(":"):
            if str(self.quantity) == str(i):
                break
            index += 1

        price = int(product.price.split(":")[index])
        o_price = int(product.price.split(":")[index])
        discount = price * (int(product.percentage) / 100)
        price -= discount
        tax =  int(o_price) * (int(product.tax) / 100)
        delivery_fees = int(product.delivery_fees)
        other_fees = int(product.other_fees)
        self.price = (price + tax + delivery_fees + other_fees) * int(self.number)
        self.save()
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    items=models.CharField(max_length=1000)
    address=models.CharField(max_length=100)
    payment_id=models.CharField(max_length=100)
    order_status=models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.name}"

class CancellationRequest(models.Model):
    request_id = models.CharField(max_length=20, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancellation Request for Order {self.order.order_id}"

