"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings 
from myapp import views
urlpatterns = [
    path('admin123/', admin.site.urls),
    path('', views.home, name='home'),
    path('cart', views.cart, name='cart'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('card', views.card, name='card'),
    path('payment', views.payment, name='payment'),
    path('shippinh', views.shippinh, name='shippinh'),
    path('returnp', views.returnp, name='return'),
    path('faq', views.faq, name='faq'),
    path('reg', views.reg, name='reg'),
    path('login', views.login, name='login'),
    path('log', views.log, name='log'),
    path('checkout', views.checkout, name='checkout'),
    path('confirm_password', views.confirm_password, name='confirm_password'),
    path('reset', views.reset, name='reset'),
    path('imgdetail/<int:id>', views.imgdetail, name='imgdetail'),
    path('add_cart/<int:id>', views.add_cart, name='add_cart'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_wishlist/<int:id>', views.add_wishlist, name='add_wishlist'),
    path('wish_delete/<int:id>', views.wish_delete, name='wish_delete'),
    path('logout', views.logout, name='logout'),
    path('cart_increment/<int:id>', views.cart_increment, name='cart_increment'),
    path('cart_decrement/<int:id>', views.cart_decrement, name='cart_decrement'),
    path('cart_delete/<int:id>', views.cart_delete, name='cart_delete'),
    path('apply_coupon', views.apply_coupon, name='apply_coupon'),
    path('editaddress',views.editaddress,name="editaddress"),
    path('order_create',views.order_create,name="order_create"),
    path('all_orders',views.all_orders,name="all_orders"),
    path('single_order/<str:order_id>', views.single_order, name='single_order'),
    path("toggle-refund/<str:order_id>/", views.toggle_refund, name="toggle_refund"),
    path('rate',views.rate_product, name='rate_product'),
    path('get_shipping_charge/<int:address_id>/', views.get_shipping_charge, name='get_shipping_charge'),
]





urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

