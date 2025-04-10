from django.shortcuts import render,redirect
from .models import*
import random
from django.core.mail import send_mail
from django.contrib import messages



def home(request):
    if 'email' in request.session:
        mc = Category.objects.all()
        pid = Product.objects.all().order_by("-id")

        uid=User.objects.get(email=request.session['email'])
        cart_count=Add_to_cart.objects.filter(user_id=uid,status=True).count()

        wish_count=Wishlist.objects.filter(user_id=uid).count()
        wishlist_products = Wishlist.objects.filter(user_id=uid)
        price_id=Price.objects.all()
        color_id=Color.objects.all()
        size_id=Size.objects.all()
        fabric_id=Fabric.objects.all()
        

        price_filter=Price.objects.all()
        price_filter2=request.GET.get("price_filter2")


        color_filter=Color.objects.all()
        color_filter2=request.GET.get("color_filter2")

        size_filter=Size.objects.all()
        size_filter2=request.GET.get("size_filter2")

        fabric_filter=Fabric.objects.all()
        fabric_filter2=request.GET.get("fabric_filter2")


        mc2 = request.GET.get("mc2")  # First subcategory (mc2)
        
        sc = Sub_category.objects.all()
        sc2 = request.GET.get("sc2")  # Second subcategory (sc2)
       

        nc = New_subcategory.objects.all()
        nc3 = request.GET.get("nc3")

        wish=[]
        for i in wishlist_products:
            wish.append(i.product_id.id)
      

      
        if mc2:
            pid = Product.objects.filter(sub_category=mc2)
        elif sc2:
            pid = Product.objects.filter(name=sc2)
        elif nc3:
            pid = Product.objects.filter(name=nc3) 
        elif price_filter2:
            pid=Product.objects.filter(pro_price=price_filter2)
        elif color_filter2:
            pid=Product.objects.filter(pro_Color=color_filter2)
        elif size_filter2:
            pid=Product.objects.filter(pro_size=size_filter2)  
        elif fabric_filter2:
            pid=Product.objects.filter(pro_size=fabric_filter2)
        else:
            pid = Product.objects.all().order_by("-id")

        print(wish_count)
        context = {
            "pid": pid,
            "mc": mc,
            "sc": sc,
            "sc2": sc2,
            "nc3": nc3,  
            "mc2": mc2,
            "nc":nc,
            "wish":wish,
            "cart_count":cart_count,
            "wish_count":wish_count,
            "price_id": price_id,
            "color_id": color_id,  
            "size_id": size_id,
            "fabric_id":fabric_id,
            "price_filter":price_filter,
            "price_filter2":price_filter2,
            "color_filter": color_filter,
            "color_filter2": color_filter2,  
            "size_filter": size_filter,
            "size_filter2":size_filter2,
            "fabric_filter": fabric_filter,
            "fabric_filter2": fabric_filter2,  
           
        }
        return render(request, "home.html", context)
    else:
        return render(request, "login.html")


# def cart(request):
    
#     if 'email' in request.session:
#         mc=Category.objects.all()
#         sc = Sub_category.objects.all()
#         nc = New_subcategory.objects.all()
#         cart_count=Add_to_cart.objects.all().count()
        

#         contaxt={"mc":mc,"sc":sc,"nc":nc}
#         return render(request,"cart.html",contaxt)
#     else:
#         return render(request,"login.html")

def contact(request):
    
    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"contact.html",contaxt)
    else:
        return render(request,"login.html")
def about(request):

    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"about.html",contaxt)
    else:
        return render(request,"login.html")
def card(request):
    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"cart.html",contaxt)
    else:
        return render(request,"login.html")
    
def payment(request):
    
    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"payment.html",contaxt)
    else:
        return render(request,"login.html")
    
def returnp(request):
    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"returnp.html",contaxt)
    else:
        return render(request,"login.html")
    
def faq(request):
    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"faq.html",contaxt)
    else:
        return render(request,"login.html")
    
def editaddress(request):
    
    if 'id' in request.GET:
        address_id = request.GET.get('id')
        edit=address.objects.get(id=int(address_id))
        edit.delete()
        return redirect("checkout")
    
    if request.method == "POST":
        name=User.objects.get(email=request.session['email'])
        id=request.POST['aid']
        fname=request.POST['fname']
        lname=request.POST['lname']  
        recident_address=request.POST['address']
        state=request.POST['state']
        pincode=request.POST['pincode']
        phone=request.POST['phone']
        
        edit=address.objects.get(id=int(id))
        edit.firstname=fname
        edit.lastname=lname
        edit.resident_address=recident_address
        edit.state=state
        edit.pincode=pincode
        edit.phone=phone
        edit.save()
        old_address=address.objects.filter(email=name)
        con={"mail":name.email,"existing_address":old_address}
        # return render(request,"checkout.html",con)
        return redirect("checkout")

    
import razorpay    
def checkout(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        mc=Category.objects.all()
        cart_count=Add_to_cart.objects.filter(user_id=uid,status=True).count()
        wish_count=Wishlist.objects.filter(user_id=uid).count()
        ch=address.objects.filter(email=uid)
        old_address=address.objects.filter(email=uid)
        ctya=0
        ship=shiping.objects.all()
        
        cart_sum=Add_to_cart.objects.filter(user_id=uid,status=True)
        subtotal=sum(i.price for i in cart_sum)
        dis=0
        disamount=0
        total_price=subtotal
      
        if apply_user.objects.filter(user_coupon=uid).count() >=1 :
            coup_count=apply_user.objects.filter(user_coupon=uid).order_by("-id")[0]
            print(coup_count.apply_coupon.c_dis)
            dis=coup_count.apply_coupon.c_dis
            disamount=(dis*subtotal)/100
            total_price=subtotal-disamount
        
        
    
        if request.GET.get("addrss"):
            abc=request.GET.get("addrss")
            cty=address.objects.get(id=int(abc))
            ctya=cty.city.shiping_charge
            print(abc)
    
        if 'edit' in request.GET:
            # Get the address to be edited
            address_id = request.GET.get('edit')
            existing =address.objects.get(id=address_id)
            con = {'existing': existing,  'mail': uid.email, "existing_address":old_address,"uid":uid,"ship":ship,"cty":ctya,"subtotal":subtotal,"dis":dis,"disamount":disamount,"total_price":total_price,"cart_sum":cart_sum}#"subtot":stot,"total":total,"dis":dis,"disamount":disamount}
            return render(request, 'checkout.html', con)
       
        if request.POST:
            fname=request.POST['fname']
            lname=request.POST['lname']  
            recident_address=request.POST['address']
            state=request.POST['state']
            pincode=request.POST['pincode']
            phone=request.POST['phone']
            ac=request.POST['city']
            city=shiping.objects.get(shiping_city=ac)
            
            print(fname,lname,recident_address,state,pincode,phone,city)
            address.objects.create(firstname=fname,lastname=lname,resident_address=recident_address,state=state,pincode=pincode,phone=phone,email=uid,city=city)
        
        if total_price == 0:    
            amount = 1*100 #100 here means 1 dollar,1 rupree if currency INR
            client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
            response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
            print(response,"**************")
            contaxt={"response":response,"mc":mc,"cart_count":cart_count,"wish_count":wish_count,"ch":ch,"uid":uid,"existing_address":old_address,"ship":ship,"cty":ctya,"subtotal":subtotal,"dis":dis,"disamount":disamount,"total_price":total_price,"cart_sum":cart_sum}
            return render(request,"checkout.html",contaxt)
        else:
            amount = total_price*100 #100 here means 1 dollar,1 rupree if currency INR
            client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
            response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
            print(response,"**************")
            contaxt={"response":response,"mc":mc,"cart_count":cart_count,"wish_count":wish_count,"ch":ch,"uid":uid,"existing_address":old_address,"ship":ship,"cty":ctya,"subtotal":subtotal,"dis":dis,"disamount":disamount,"total_price":total_price,"cart_sum":cart_sum}
            return render(request,"checkout.html",contaxt)
        
    else:
        return render(request,"login.html")
    
def shippinh(request):
    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"shippinh.html",contaxt)
    else:
        return render(request,"login.html")
    

def login(request):
    if 'email' in request.session:
        mc=Category.objects.all()
        contaxt={"mc":mc}
        return render(request,"login.html",contaxt)
    else:
        return render(request,"login.html") 

def cart(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        mc=Category.objects.all()
        cart_id=Add_to_cart.objects.filter(user_id=uid,status=True)
        cart_sum=Add_to_cart.objects.filter(user_id=uid,status=True)
        cart_count=Add_to_cart.objects.filter(user_id=uid,status=True).count()
        wish_count=Wishlist.objects.filter(user_id=uid).count()
        nc = New_subcategory.objects.all()
        price_id=Price.objects.all()
        color_id=Color.objects.all()
        size_id=Size.objects.all()
        fabric_id=Fabric.objects.all()

        
        l1=[]
        charge=20
        subtotal=sum(i.price for i in cart_sum)
        dis=0
        disamount=0
        total_price=subtotal
      
        if apply_user.objects.filter(user_coupon=uid).count() >=1 :
            coup_count=apply_user.objects.filter(user_coupon=uid).order_by("-id")[0]
            print(coup_count.apply_coupon.c_dis)
            dis=coup_count.apply_coupon.c_dis
            disamount=(dis*subtotal)/100
            total_price=subtotal-disamount
            
        else:
          dis=0 


        contaxt={"mc":mc,"cart_id":cart_id,"cart_sum":cart_sum,"charge":charge,"price_id":price_id,"color_id":color_id,"size_id":size_id,"fabric_id":fabric_id,
                 "total_price":total_price,"subtotal":subtotal,"cart_count":cart_count,"wish_count":wish_count,"nc":nc,"dis":dis,"disamount":disamount}
        return render(request,"cart.html",contaxt)
    else:
        return render(request,"login.html")
   
   
def imgdetail(request,id):
    if 'email' in request.session:
        mc=Category.objects.all()
        pid=Product.objects.get(id=id)
        contaxt={"mc":mc,"pid":pid}

        return render(request,"card.html",contaxt)
    else:
        return render(request,"login.html")

def reg(request):
    if request.POST:
        name=request.POST["name"]
        email=request.POST["email"]
        password=request.POST["password"]
        conp=request.POST["conp"]

        try:
            uid=User.objects.get(email=email)
            if uid.email==email:
                con={"msg":"this email is already exist use another email"}
                return render(request,"login.html",con)
        except:
            if(password==conp):
                User.objects.create(name=name,email=email,password=password)
                return render(request,"login.html")

        else:
            return render(request,"regi.html")
    else:
        return render(request,"regi.html")
    

def wishlist(request):
    uid=User.objects.get(email=request.session['email'])
    w_wish_id=Wishlist.objects.filter(user_id=uid) 
    mc = Category.objects.all()
    nc = New_subcategory.objects.all()
    cart_count=Add_to_cart.objects.all().count()
    wish_count=Wishlist.objects.filter(user_id=uid).count()
    price_id=Price.objects.all()
    color_id=Color.objects.all()
    size_id=Size.objects.all()
    fabric_id=Fabric.objects.all()
    
    con={"uid":uid,"w_wish_id":w_wish_id,"cart_count":cart_count,"wish_count":wish_count,"mc":mc,"nc":nc,"price_id":price_id,"color_id":color_id,"size_id":size_id,"fabric_id":fabric_id}
    
    return render(request,"wishlist.html",con)
    

def add_wishlist(request, id):
    uid = User.objects.get(email=request.session['email'])
    pid = Product.objects.get(id=id)
    wish_id = Wishlist.objects.filter(product_id=pid, user_id=uid).first()
    
    if wish_id:
        wish_id.delete()
        
    else:
        Wishlist.objects.create(
            user_id=uid,
            product_id=pid,
            price=pid.price,
            name=pid.name,
            image=pid.image,
        )
        

    return redirect('wishlist')

def wish_delete(request,id):
    wish_id=Wishlist.objects.get(id=id)
    wish_id.delete()
    return redirect("wishlist")



def log(request):
    if 'email' in request.session:
        return render(request,"home.html")
    else:
        if request.POST:
            email=request.POST["email"]
            password=request.POST["password"]
            try:

                uid=User.objects.get(email=email)
                print(uid)
                if uid.email==email:
                    if uid.password==password:   
                        request.session['email']=uid.email
                        return redirect("home")
                    else:
                        con={"msg":"password do not match or invalid email"}
                        return render(request,"login.html",con)
                else:
                    con={"msg":"invalid email"}
                    return render(request,"login.html",con)
        
                
            except:
                    con={"msg":"invalid email"}
                    return render(request,"login.html",con)
        else:  
            return render(request,"login.html")  

def reset(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        try:
            uid=User.objects.get(email=email)
        
            uid.otp=otp
            uid.save()
            send_mail("django",f"your otp is - {otp}",'gohiljayb10@gmail.com',[email])
            contaxt={
                "email":email
            }
            return render(request,"confirm.html",contaxt)
        except:
            con={"msg":"invalid email"}
            print("Invalid Email")       
            return render(request,"reset.html",con) 
    else:
        return render(request,"reset.html")


def confirm_password(request):
    if request.POST:
        email=request.POST.get('email')
        otp=request.POST.get('otp')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        
        try:
            uid=User.objects.get(email=email)
            if str(uid.otp)==otp:
                if new_password==confirm_password:
                    uid.password=new_password
                    uid.save()
                    con={'email':email}

                    return render(request,"login.html",con)
                else:
                    con={"msg":"password do not match"}
                    return render(request,"confirm.html",con)
                
            else:
                con={"msg":"invalid otp"}
                return render(request,"confirm.html",con)
        except User.DoesNotExist:
            con={"msg":"invalid email3"}
            return render(request,"confirm.html",con)

 
def logout(request):
    if 'email' in request.session:
        del request.session['email']

    return render(request,'login.html')

def add_cart(request,id):
    if "email" in request.session:
        cart_id=Category.objects.all()
        pid=Product.objects.get(id=id)
        uid=User.objects.get(email= request.session['email'])
     
        cart_item=Add_to_cart.objects.filter(product_id=pid, user_id=uid, status=True).exists()
        if cart_item :
            cart_item=Add_to_cart.objects.get(product_id=pid, user_id=uid, status=True)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.totalprice = cart_item.quantity * cart_item.price
            cart_item.save()
        else:
            Add_to_cart.objects.create(product_id=pid,user_id=uid, name=pid.name,
                                       image=pid.image, price=pid.price,totalprice=pid.price)
            
            contaxt={"pid":pid,"uid":uid,"cart_id":cart_id}
        return redirect("cart")
    else:
        return render(request,"login.html",contaxt)
    
def cart_increment(request,id):
    cart_inc=Add_to_cart.objects.get(id=id)
    if cart_inc :
        cart_inc.quantity = cart_inc.quantity + 1
        cart_inc.totalprice = cart_inc.quantity * cart_inc.price
        cart_inc.save()
        return redirect("cart")
    

def cart_decrement(request,id):
    cart_dec=Add_to_cart.objects.get(id=id)
    if cart_dec.quantity==1:
        cart_dec.delete()
        return redirect("cart")
    else:
        if cart_dec:
            cart_dec.quantity=cart_dec.quantity-1
            cart_dec.totalprice=cart_dec.quantity*cart_dec.price
            cart_dec.save()
            
            return redirect("cart")
        
def cart_delete(request,id):
    cart_item=Add_to_cart.objects.get(id=id)
    cart_item.delete()
    return redirect("cart")


def apply_coupon(request):
    uid=User.objects.get(email= request.session['email'])
    cart_get=Add_to_cart.objects.filter(user_id=uid,status=True)
    coup=Coupon.objects.all()
  

    if request.POST:
        coupon = request.POST["code"]
        print(coupon)

        try:
           
            coupon_id = Coupon.objects.get(code=coupon)
            print("Coupon exists:")
            aid=apply_user.objects.filter(user_coupon=uid, apply_coupon=coupon_id).exists()
            if aid:
                messages.success(request,"Coupon already applied.")
                return redirect("cart")
            else:
                apply_user.objects.create(user_coupon=uid, apply_coupon=coupon_id)
                messages.success(request,"Coupon applied successfully!.")
                return redirect("cart")
        
        except Coupon.DoesNotExist:
            messages.success(request,"Coupon does not exist.")
            return redirect("cart")

    else:
      
        context = {"uid": uid, "cart_get": cart_get, "coup": coup}
        return redirect("cart")


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



def single_order(request, order_id):
    order_instance = order.objects.get(order_id=order_id)
    return render(request, 'single_order.html', {'order': order_instance})

from django.http import JsonResponse

def toggle_refund(request, order_id):
    if request.method == "POST":
        try:
            order1 = order.objects.get(order_id=order_id)
            order1.is_refunded = True  # Toggle refund status
            order1.save()
            return render(request, 'all_orders.html')
        except order.DoesNotExist:
            return render(request, 'all_orders.html')
    return render(request, 'all_orders.html')


def rate_product(request):
    uid=User.objects.get(email= request.session['email'])
    if request.method == "POST":
        rating = request.POST.get('rating')  # Get rating value
        description = request.POST.get('description')  # Get description

        if rating and description:
            Rating.objects.create(user_data=uid, rating=rating, description=description)
            return redirect('rate_product')  # Redirect to refresh page

    ratings = Rating.objects.all().order_by('-created_at')  # Fetch stored ratings
    return render(request, "rating.html", {"ratings": ratings})


def get_shipping_charge(request, address_id):
    print(address_id,"okokok")
    try:
        address1 = address.objects.get(id=address_id)
        print(address1)
        shipping_charge = address1.city.shiping_charge  # Get shipping charge from related city
        return JsonResponse({'shipping_charge': shipping_charge})
    except address.DoesNotExist:
        return JsonResponse({'error': 'Address not found'}, status=404)