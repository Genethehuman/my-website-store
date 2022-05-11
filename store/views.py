from django.shortcuts import render
from .models import Category, Item
from cart.models import Cart
from django.utils.text import slugify
from marketing.models import MarketingMessage
# Create your views here.


def store_main_view(request):
    all_categories = Category.objects.all()
    # marketing_message = MarketingMessage.objects.all()[0]
    #marketing_message = request.session['marketing_message']
    print('MARKETING MESSAGE FROM SESSION:', request.session['marketing_message'])
    context={
        'all_categories': all_categories,
        # 'marketing_message': marketing_message,
    }
    return render(request, 'store/main.html', context=context)

def category_view(request, vagina):
    print('ARGUMENTS:', vagina)
    all_items = Item.objects.all()
    items_in_category = []
    for i in all_items:
        if slugify(i.category) == vagina:
            items_in_category.append(i)
    context={
        'all_items': all_items,
        'items_in_category': items_in_category,
    }
    print('Items In Category', items_in_category)
    return render(request, 'store/category.html', context=context)




def item_detail_view(request, anal):
    print('VOT ETO PRINT:', anal)
    item_object = Item.objects.get(slug=anal)
    context={
        'obj': item_object,
    }
    return render(request, 'store/item-detail.html', context=context)

# def _cart_id(request):
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
#     return cart

# def add_to_cart(request, item_id):
#     item_in_cart = Item.objects.get(id=item_id)


    

# def cart_view(request):
#     all_items = Item.objects.all()
#     context={
#         'all_items': all_items,
#     }
#     return render(request, 'store/cart.html', context=context)


