from django.db import models


# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(unique=True,blank=True,null=True)
    password=models.CharField(max_length=20,blank=True,null=True)
    otp=models.IntegerField(default=0)


    def __str__(self):
        return self.name
    
class Category(models.Model):
    name=models.CharField(max_length=25,blank=True,null=True)

    def __str__(self):
        return self.name

class Sub_category(models.Model):
    main_category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class New_subcategory(models.Model):
    main_category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    secondsub_category=models.ForeignKey(Sub_category,on_delete=models.CASCADE,blank=True,null=True)

    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Price(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name

class Fabric(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    cate_id=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    sub_category=models.ForeignKey(Sub_category,on_delete=models.CASCADE,blank=True,null=True)
    secondsub_category=models.ForeignKey(New_subcategory,on_delete=models.CASCADE,blank=True,null=True)
    pro_price=models.ForeignKey(Price,on_delete=models.CASCADE,blank=True,null=True)
    pro_Color=models.ForeignKey(Color,on_delete=models.CASCADE,blank=True,null=True)
    pro_size=models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
    pro_fabric=models.ForeignKey(Fabric,on_delete=models.CASCADE,blank=True,null=True)

    name=models.CharField(max_length=100,blank=True,null=True)
    price=models.IntegerField()
    del_price=models.IntegerField()
    des=models.TextField()
    image=models.ImageField(upload_to="media",blank=True,null=True)
    quantity=models.IntegerField(default=0)


    def __str__(self):
        return self.name    

class Add_to_cart(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=25,blank=True,null=True)
    price=models.IntegerField(default=0)
    totalprice=models.IntegerField(blank=True,null=True)
    image=models.ImageField(upload_to="media",blank=True,null=True)
    quantity=models.IntegerField(default=1,blank=True,null=True)
    status=models.BooleanField(default=True)
    def __str__(self):
        return self.name
    

class Wishlist(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=25,blank=True,null=True)
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to="media",blank=True,null=True)

    def __str__(self):
        return self.name
    
class Coupon(models.Model):
    code=models.CharField(max_length=25,blank=True,null=True)
    c_dis=models.IntegerField()

    def __str__(self):
        return self.code
    
class apply_user(models.Model):
    user_coupon=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    apply_coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,blank=True,null=True)


class shiping(models.Model):
    shiping_city=models.CharField(max_length=50)
    shiping_charge=models.IntegerField()
    
    def __str__(self):
        return self.shiping_city

class DeliveryBoy(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    assigned_city = models.ForeignKey(shiping, on_delete=models.CASCADE)  # Assign to city
    
    def __str__(self):
        return f"{self.name} {self.assigned_city.shiping_city}"



class address(models.Model):
    email=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    resident_address=models.CharField(max_length=50)
    state=models.CharField(max_length=20)
    pincode=models.IntegerField()
    phone=models.IntegerField()
    city=models.ForeignKey(shiping,on_delete=models.CASCADE,blank=True,null=True)
    

    def __str__(self):
        return self.email.email




class order(models.Model):
    user_data=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    address_data=models.ForeignKey(address,on_delete=models.CASCADE,blank=True,null=True)
    cart_data=models.ManyToManyField(Add_to_cart)
    order_id=models.CharField(max_length=100)
    sub_total=models.IntegerField()
    shipping=models.CharField(max_length=100)
    coupon=models.IntegerField()
    total=models.IntegerField()
    is_refunded = models.BooleanField(default=False)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_orders")

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')




class Rating(models.Model):
    user_data=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_data.name} - {self.rating}"
