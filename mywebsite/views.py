from django.shortcuts import render, redirect
from django.http import request, response
from django.template import context
from django.utils.text import slugify
from marketing.models import MarketingMessage, Slider
from marketing.forms import EmailForm
from posts.models import Post
from store.models import Item, Category

def capital_word_view(request):
    context={}
    return render(request, 'capital-word.html', context=context)

def home_view(request):
    sliders = Slider.objects.all_featured()
    object_list = Post.objects.all()
    form = EmailForm(request.POST or None)
    context={
        'object_list': object_list,
        'sliders': sliders,
        'form': form,
    }
    # print('FORM CLEANED DATA:', form.cleaned_data['email'])
    return render(request, 'home.html', context=context)

def cart_item_create(request):
    context={}
    return render(request, 'cart-item-detail', context=context)

def cart_item_delete(request):
    context={}
    return render(request, 'cart-item-delete', context=context)


def test_view(request):
    context = {}
    all_names = []
    if request.method == "POST":
        title = request.POST.get('class-item-title')
        print('TITLE:', title)

        for i in Item.objects.all():
            all_names.append(i.name)

        if title in all_names:
            i.delete()
            print('FUCK YOU ASSHOLE')
            context['created'] = False

        else:
            new_obj = Item.objects.create(name=title)
            new_obj.slug = slugify(title)
            new_obj.save()
            context = {
                'created': True,
                'new_obj': new_obj,
            }

        if context['created']:
            return redirect('item-detail', anal=new_obj.slug)
    
        print('OBJ IS:', title)
    
    return render(request, 'test.html', context=context)

def capital_word_result_view(request):
    print(request.GET)
    query_set = request.GET
    word = str(query_set.get('q'))
    capital_word = word.upper()
    print('Slovo', capital_word)
    context={
        'word': word,
        'capital_word': capital_word,
    }
    return render(request, 'capital-word-result.html', context=context)




