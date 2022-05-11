import time
from django.template import context
from django.urls import reverse
from django.shortcuts import render, redirect
from.models import Order
from django.contrib.auth.decorators import login_required

# Create your views here.
from cart.models import Cart
from .utils import id_generator


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
        new_order.user = request.User
        new_order.order_id = id_generator()
        new_order.save()

    
        

    new_order, created = Order.objects.get_or_create(cart=cart)
    if created:
        new_order.order_id = id_generator() #str(time.time()) 
        new_order.save()
    new_order.user = request.user
    new_order.save()
    print('OUR USER:', new_order.user)
    #run credit card
    if new_order.status == 'Finished':
        #cart.delete()
        del request.session['cart_id']
        del request.session['cart_items_count']
        return redirect(reverse('cart'))
    context = {}
    return render(request, 'orders/checkout.html', context=context)
