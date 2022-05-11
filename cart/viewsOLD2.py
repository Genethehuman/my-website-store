from calendar import c
from django.http import HttpResponseRedirect
from django.template import context
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import Cart, CartItem
from store.models import Item, Variation




def cart_view(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
        

    if the_id:
        cart = Cart.objects.get(id=the_id)
        objects_in_cart = cart.cartitem_set.all()
        print('OBJECTS IN THE CART:', objects_in_cart)
        context={
            'cart': cart,
            'objects_in_cart': objects_in_cart,
        }
    else:
        empty_message = 'The Cart Is Empty! Shop More Scum!'
        context = {
            'empty': True,
            'empty_message': empty_message,        
        }

    return render(request, 'store/cart.html', context=context)

def add_to_cart_view(request, hueta):
    request.session.set_expiry(12000)

    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)
#до сюда вроде бы понятно все про то, как карзинку делаем
    try:
        item_you_add = Item.objects.get(slug=hueta)
        print('ITEM YOU ADD:', item_you_add)
    except Item.DoesNotExist:
        pass
    except:
        pass
    
    item_var = [] #item_variation
    if request.method == "POST":
        print(request.POST)
        qty = request.POST['qty']
        for i in request.POST:
            key = i
            value = request.POST[key]
            print(key, value)
            try:
                v = Variation.objects.get(item=item_you_add, category__iexact=key, title__iexact=value)
                print('V:', v)
                item_var.append(v)
            except:
                pass
        #print(item_var[0])

        #("cart item object", "True/False")
        cart_item, created = CartItem.objects.get_or_create(cart=cart, cart_item=item_you_add)
        #я требую объяснений!!! Вроде и понятно, а вроде и хотелось бы табличку эту представить
        #print('THIS IS ADD OR CREATE:', CartItem.objects.get_or_create(cart=cart, cart_item=item_you_add))
        print('GET OR CREATE JUST TRIGGERED:')
        if created:
            print("Yeah")
        if qty:
            if int(qty) <= 0:
                # cart_item.delete()
                print('CART ITEM IN MODELS:', CartItem.objects.get(id=cart_item.id))
                #CartItem.objects.get(id = cart_item.id).delete() #так тоже можно
                cart_item.delete()
                print('CART ITEM SET:', cart.cartitem_set.all())
                print('QTY:', qty)
                print('CART ITEM:', cart_item)
                print('CART ITEM QUANTITY:', cart_item.quantity)
                
            else:
                print('POSHLO V ELSE?:')
                if len(item_var) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*item_var)
                    # for i in item_var:
                    #     cart_item.variations.add(i)
                print('VARIATIONS:', cart_item.variations.all())
                cart_item.quantity = qty
                cart_item.save()
            
        else:
            print('WHY ELSE?')
            pass
            


        print('CART ITEM SET AGAIN:', cart.cartitem_set.all())
        

        # if cart_item not in cart.cart_items.all():
        #     cart.cart_items.add(cart_item)
        # else:
        #     cart.cart_items.remove(cart_item)
            
        #print('ITEM QUANTITY:', Item.objects.get(slug=hueta).quantity)
        
        new_total = 0.00
        for i in cart.cartitem_set.all():
            new_total += float(i.cart_item.price) * i.quantity
        cart.total = new_total
        cart.save()
        request.session['cart_items_count'] = cart.cartitem_set.count()
        #вот тут бы хотелось немного больше понимать конечно же
        print('ITEMCART OBJECTS ALL:', Cart.objects.all())
        print('CART ITEM SET:', cart.cartitem_set.all())
        print('COUNT OF ITEMS IN THE CART:', request.session['cart_items_count'])
        return redirect(reverse('cart'))
    else:
        return redirect(reverse('cart'))   






