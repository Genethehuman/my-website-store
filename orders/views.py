from decimal import Decimal
from ast import Or
from cmath import e
from pipes import Template
import time
from django import template
from django.http import request, HttpResponseNotFound, JsonResponse
from django.template import context
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from.models import Order
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.
from cart.models import Cart
from .utils import id_generator
from accounts.forms import UserAddressForm
from accounts.models import UserAddress, UserAddressManager
import stripe
import json

try:
    stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY
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
        new_order.id = cart.id
        new_order.cart = cart
        new_order.user = request.user
        new_order.sub_total = cart.total
        new_order.order_id = id_generator()
        new_order.save()
    except:
        return redirect('cart')

    final_amount = 0
    if new_order is not None:
        new_order.sub_total = cart.total
        print('FINAL_AMOUNT:', new_order.get_final_amount)
        new_order.final_price = new_order.get_final_amount()
        print('FINAL PRICE:', new_order.final_price)
        new_order.save()

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
        print('STRIPE TOKEN:', request.POST['stripeToken'])   


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
        #del request.session['cart_id']   ТУТ НАДО ПОМЕНЯТЬ ОБРАТНО КАК ДОДЕЛАЮ ОПЛАТУ
        #del request.session['cart_items_count']
        return redirect(reverse('cart'))
    context = {
        'address_form': address_form,
        'current_addresses': current_addresses,
        'current_billing_addresses': current_billing_addresses,
        # 'stripe_pub': stripe_pub, 
    }
    print('ORDER.ID:', new_order.id)
    return render(request, 'orders/checkout.html', context=context)

class payment_successful_view2(TemplateView):

    template_name = 'orders/payment-successful.html'

    def get(self, request, *args, **kwargs):
        try:
            print('TRY')
            session_id = request.GET.get('session_id')
            print('SESSION_ID:', session_id) #session_id сессии берется из ебучей стандартной функции Джаваскрипта в создании чекаут сессии для stripe'а
        except:
            session_id = None
            return HttpResponseNotFound

        if session_id is not None:

            stripe.api_key = settings.STRIPE_SECRET_KEY
            print('BEFORE SESSION.RETRIEVE')
            session = stripe.checkout.Session.retrieve(session_id)
            print('SESSION:', session)
            card_name = session.customer_details.name
            
            order = Order.objects.get(stripe_payment_intent=session.payment_intent)
            
            order.status = 'Finished'
            order.save()

            # stripe.Token.create(
            # card={
            #     "number": "4242424242424242",
            #     "exp_month": 6,
            #     "exp_year": 2023,
            #     "cvc": "314",
            # },
            # )
            context = {
                'card_name': card_name,
            }
            

            print('Request Session Cart_ID:', request.session['cart_id'])
            del request.session['cart_id']
            del request.session['cart_items_count']

            # request.session.modified = True
            print('CART ID ESHE TUT?:', request.session['cart_id'])
            print('CART ITEM COUNT ESHE TUT?:', request.session['cart_items_count'])
            
            return render(request, self.template_name, context=context)



def payment_successful_view(request):

    template_name = 'orders/payment-successful.html'

    try:
        print('TRY')
        session_id = request.GET.get('session_id')
        print('SESSION_ID:', session_id) #session_id сессии берется из ебучей стандартной функции Джаваскрипта в создании чекаут сессии для stripe'а
    except:
        session_id = None
        return HttpResponseNotFound

    if session_id is not None:

        stripe.api_key = settings.STRIPE_SECRET_KEY
        print('BEFORE SESSION.RETRIEVE')
        session = stripe.checkout.Session.retrieve(session_id)
        print('SESSION:', session)
        customer = session.customer
        card_name = session.customer_details.name
        print('CUSTOMER:', customer)
        print('POST:', request.POST)
        
        order = Order.objects.get(stripe_payment_intent=session.payment_intent)
        
        order.status = 'Finished'
        order.save()
        context = {
            'card_name': card_name,
        }
        

        
        try:
            del request.session['cart_id']
            del request.session['cart_items_count']
        except:
            print('NE UDALILOS NIHOYA')

        # request.session.modified = True
        
        
        return render(request, template_name, context=context)

class payment_failed_view(TemplateView):

    template_name = 'orders/payment-failed.html'

    def get(self, request, *args, **kwargs):
        
        context={}

        return render(request, self.template_name, context=context)


def payment_page_view(request):
    if request.method == 'POST':
        print('REQUEST.POST:', request.POST)
        try:
            the_id = request.session['cart_id']
        except:
            pass
        
        address_s = request.POST.get('shipping_address')
        address_b = request.POST.get('billing_address')
        print('ADDRESS:', address_s)
        print('BILLING_ADDRESS:', address_b)
        user = request.user
        key = settings.STRIPE_PUBLISHABLE_KEY
        this_order = Order.objects.get(id=the_id)
        this_order.user_shipping = UserAddress.objects.get(id=address_s)
        this_order.user_billing = UserAddress.objects.get(id=address_b)
        this_order.save()
        

        context = {
            'user': user,
            'order': this_order,
            'stripe_publishable_key': key,
        }
        print('THIS_ORDER:', this_order, this_order.id, this_order.cart)
        
        return render(request, 'orders/payment-page.html', context=context) 
    
    else:
        return redirect(reverse('checkout'))

@csrf_exempt
def checkout_final_view(request, id):
    print('IDI NAHOI:', request.GET)

    request_data = json.loads(request.body)
    
    order = Order.objects.get(id=id) #возможно здесь надо будет изменить как у них
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_stripe = request.user.userstripe.stripe_id
    customer = stripe.Customer.retrieve(user_stripe)
    print('CUSTOMER:', customer)
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
        payment_method_types=['card'],
        # shipping_address_collection={
        #     'allowed_countries': ['US', 'CA'],
        # },
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': order.id,
                    },
                    'unit_amount': int(order.final_price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment-successful')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment-failed')),
    )
    
    order.stripe_payment_intent = checkout_session['payment_intent']

    order.save()
    print(checkout_session['payment_intent'])
    print('TI PIZDA EBANAYA')
    
    context={
        'order': order,
    }
    return JsonResponse({'sessionId': checkout_session.id})





