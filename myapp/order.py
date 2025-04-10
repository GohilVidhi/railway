



class order(models.Model):
    user_data=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    address_data=models.ForeignKey(address,on_delete=models.CASCADE,blank=True,null=True)
    cart_data=models.ManyToManyField(Add_to_cart,blank=True,null=True)
    order_id=models.CharField(max_length=100)
    sub_total=models.IntegerField()
    shipping=models.CharField(max_length=100)
    coupon=models.IntegerField()
    total=models.IntegerField()
    is_refunded = models.BooleanField(default=False)

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

# ===================================
    

import uuid

def order_create(request):
    uid=User.objects.get(email= request.session['email'])
    cid=Add_to_cart.objects.filter(user_id=uid,status=True)
    address1=request.POST["selected_address"]
    aid=address.objects.get(id=address1)
    print("ok",aid.city.shiping_charge)
    subtotal=sum(i.price for i in cid)
    dis=0
    disamount=0
    total_price=subtotal
    shipping=aid.city.shiping_charge
    order_id = str(uuid.uuid4().hex[:10]).upper()
    if apply_user.objects.filter(user_coupon=uid).count() >=1 :
        coup_count=apply_user.objects.filter(user_coupon=uid).order_by("-id")[0]
        print(coup_count.apply_coupon.c_dis)
        dis=coup_count.apply_coupon.c_dis
        disamount=(dis*subtotal)/100
        total_price=subtotal-disamount+shipping
    delivery_boy = DeliveryBoy.objects.filter(assigned_city=aid.city).first()    
    print(delivery_boy)
    oid=order.objects.create(user_data=uid,address_data=aid,order_id=order_id,sub_total=subtotal,shipping=shipping,coupon=disamount,total=total_price,delivery_boy=delivery_boy)
    oid.cart_data.set(cid)
    cid.update(status=False)
    return redirect("checkout")
    # return render(request,"checkout.html")


def all_orders(request):
    uid=User.objects.get(email= request.session['email'])
    orders = order.objects.filter(user_data=uid)
    return render(request, 'all_orders.html', {'orders': orders})    

# =============

path('order_create',views.order_create,name="order_create"),
    path('all_orders',views.all_orders,name="all_orders"),


# ====================


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Orders</title>
    <style>
        /* Global Styles */
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }

        .container {
            width: 80%;
            max-width: 900px;
            margin: 50px auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }

        /* Table Styles */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background: #fff;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #007bff;
            color: white;
            text-transform: uppercase;
        }

        tr:nth-child(even) {
            background: #f2f2f2;
        }

        tr:hover {
            background: #e0e0e0;
        }

        /* Link Button */
        .view-link {
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
            transition: 0.3s;
        }

        .view-link:hover {
            color: #0056b3;
            text-decoration: underline;
        }

        /* No Orders Message */
        .no-orders {
            text-align: center;
            color: #888;
            margin-top: 20px;
        }

        /* Responsive Design */
        @media (max-width: 600px) {
            .container {
                width: 95%;
            }

            table {
                font-size: 14px;
            }

            th, td {
                padding: 10px;
            }
        }
    </style>
</head>
<body>

<div class="container">
    <h2>All Orders</h2>

    {% if orders %}
        <table>
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>User</th>
                    <th>Subtotal</th>
                    <th>Shipping</th>
                    <th>Coupon</th>
                    <th>Total</th>
                    <th>Status</th>
                    <th>Refund Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for order in orders %}
                    <tr>
                        <td>{{ order.order_id }}</td>
                        <td>{{ order.user_data.name }}</td>
                        <td>₹{{ order.sub_total }}</td>
                        <td>₹{{ order.shipping }}</td>
                        <td>₹{{ order.coupon }}</td>
                        <td><strong>₹{{ order.total }}</strong></td>
                        <td>
                            <span style=" 
                                padding: 5px 10px;
                                border-radius: 5px;
                                font-weight: bold;
                                color: white;
                                background:
                                    {% if order.status == 'pending' %}orange
                                    {% elif order.status == 'accepted' %}blue
                                    {% elif order.status == 'out_for_delivery' %}purple
                                    {% elif order.status == 'delivered' %}green
                                    {% elif order.status == 'cancelled' %}red
                                    {% else %}gray{% endif %}
                                ">
                                {{ order.get_status_display }}
                            </span>
                        </td>
                        <td>
                            <form method="post" action="{% url 'toggle_refund' order.order_id %}">
                                {% csrf_token %}
                                <button type="submit" 
                                    style="background: {% if order.is_refunded %}green{% else %}red{% endif %};
                                        color: white;
                                        border: none;
                                        padding: 5px 10px;
                                        cursor: {% if order.is_refunded %}not-allowed{% else %}pointer{% endif %};
                                        border-radius: 5px;" 
                                    {% if order.is_refunded %}disabled{% endif %}>
                                {% if order.is_refunded %}ON{% else %}OFF{% endif %}
                            </button>
                            </form>
                        </td>
                        <td>
                            <a href="{% url 'single_order' order.order_id %}" class="view-link">View Details →</a>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p class="no-orders">No orders found.</p>
    {% endif %}
</div>

</body>
</html>
