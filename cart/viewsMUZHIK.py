from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

from store.models import Item
from.models import Cart

def cart_view(request):
    cart = Cart.objects.all()[0]
    context={
        'cart': cart,
        }
    return render(request, 'store/cart.html', context)

def update_cart(request, slug):
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
        print('something')
    
    cart = Cart.objects.get(id=the_id)


    print('CART ID FROM SESSION:', request.session['cart_id'])
    
    try:
        item = Item.objects.get(slug=slug)
    except Item.DoesNotExist:
        pass
    except:
        pass
    if not item in cart.items.all():
        cart.items.add(item)
        print(cart.items.all())
    else:
        for i in cart.items.all():
            print(i.name, i.quantity)
        cart.items.remove(item)
    
    new_total = 0.00
    for item in cart.items.all():
        new_total += float(item.price) * float(item.quantity)
    print('ETO SUKA BLYA PRICE:', new_total)
        
    context = {
        'new_total': new_total,
    }
    cart.total = new_total
    cart.save()
    return redirect (reverse('cart'), context=context)






