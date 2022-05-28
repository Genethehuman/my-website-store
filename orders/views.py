from cmath import e
import time
from django.template import context
from django.urls import reverse
from django.shortcuts import render, redirect
from.models import Order
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.
from cart.models import Cart
from .utils import id_generator
from accounts.forms import UserAddressForm
from accounts.models import UserAddress, UserAddressManager

try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
except Exception as e: 
    raise NotImplementedError(str(e))

def orders_view(request):

    context={}
    return render(request, 'orders/user.html', context=context)

#require user login **
@login_required
def checkout_view(request):
    
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
        print('OUR CART:', cart)
    except:
        the_id = None
        return redirect(reverse('cart'))

    try:
        new_order = Order.objects.get(id=the_id)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.sub_total = cart.total
        new_order.final_price = float(new_order.sub_total) + float(new_order.tax_total)
        new_order.order_id = id_generator()
        new_order.save()
    except:
        return redirect('cart')

    try:
        address_added = request.GET.get('address-added')

        
    except:
        address_added = None
    
    if address_added == None:
        address_form = UserAddressForm(request.POST or None)
    else:
        address_form = None

    current_addresses = UserAddress.objects.filter(user=request.user)
    current_billing_addresses = UserAddress.objects.filter(user=request.user, billing=True)
    print('REQUEST.USER:', request.user)
    #current_billing_addresses = UserAddress.objects.get_billing_address(user=request.user)
    
    if request.method == "POST":
        print(request.POST['stripeToken'])   


    #1 add shipping address
    #2 add billing address
    #3 add and run credit card

    
        

    # new_order, created = Order.objects.get_or_create(cart=cart)
    # if created:
    #     new_order.order_id = id_generator() #str(time.time()) 
    #     new_order.save()
    # new_order.user = request.user
    # new_order.save()
    # print('OUR USER:', new_order.user)
    # #run credit card
    if new_order.status == 'Finished':
        #cart.delete()
        del request.session['cart_id']
        del request.session['cart_items_count']
        return redirect(reverse('cart'))
    context = {
        'address_form': address_form,
        'current_addresses': current_addresses,
        'current_billing_addresses': current_billing_addresses,
        'stripe_pub': stripe_pub, 
    }
    return render(request, 'orders/checkout.html', context=context)
