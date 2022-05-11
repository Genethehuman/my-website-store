from itertools import count
from django.shortcuts import render, redirect
from django.template import context
from .models import Post
from .forms import PostForm
from django.utils.text import slugify
from store.models import Item


# Create your views here.

def home_view(request):
    render(request, 'home')

def capital_word_result_view(request):
    word = request.GET
    print('Slovo', word)
    word_capital = word.upper()
    context = {
        'word_capital': word_capital
    }
    return render(request, 'capital-word.html', context=context)

def post_details_view(request, pizda):
    post_object = Post.objects.get(slug=pizda)
    context = {
        'obj': post_object
    }
    return render(request, 'posts/post-details.html', context=context)

# def post_create_view_new(request):
#     form = PostForm(request.POST or None)
#     context={
#         'form': form,
#     }
#     print('Vot On context[form]', context['form'])
#     post_object = form.save()
#     context['form'] = PostForm()
    
#     print('A vot teper vot tak:', context['form']) 
#     return render(request, 'posts/post-create.html', context=context)
    

def post_create_view(request):
    print('Request.POST:', request.POST.get('govnotitle'))
    context = {}
    if request.method == "POST":
        counter = 0
        title = request.POST.get('govnotitle')
        text = request.POST.get('sukatext')
        all_slugs = []
        obj = Post.objects.create(title=title, text=text)
        obj.slug = slugify(obj.title)
        obj.save()
        # print('VSE TITLES:', Post.objects.all().get(title)) - как обратиться ко всем без цикла

        for i in Post.objects.all():
            #print(i.slug)
            #print(obj.slug)
            all_slugs.append(i.slug)
        print('OBJ SLUG IS:', obj.slug)
        print('ALL SLUGS:', all_slugs)
        print('SKOLKO SLUGOV:', all_slugs.count(obj.slug))
        if all_slugs.count(obj.slug) >= 2:
            obj.slug = obj.slug + str(obj.id)
            obj.save()
        context={
            'obj': obj ,
            'created': True,
        }
        print('Context of created is:', context['created'])
        print('object slug before redirectiong:', obj.slug)
        if context['created'] == True:
            return redirect('post-details', pizda=obj.slug)   
    return render(request, 'posts/post-create.html', context=context)

def search_view(request):
    print(request.GET)
    key_word = request.GET.get('q')
    search_list = []
    context={}
    for object in Post.objects.all():
        if key_word.lower() in object.title.lower():
            search_list.append(object)
            context['it_is_post'] = True
    for object in Item.objects.all():
        if key_word.lower() in object.name.lower():
            search_list.append(object)
            context['it_is_item'] = True
    print(search_list)
    context['search_list'] = search_list
    return render(request, 'posts/search-results.html', context=context)

