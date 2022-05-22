import re
import string
from django.contrib import messages
from cmath import log
import this
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template import context
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate, get_user_model
from  .forms import UserAddressForm
from accounts.models import EmailConfirmed
from .forms import LoginForm, RegistrationForm

# Create your views here.


def logout_view(request):
    logout(request)
    request.session['user_logged_in'] = False
    messages.success(request, 'You logged out. Please <a href="%s">login</a>' %reverse('login'), extra_tags='safe')
    # messages.warning(request, 'You logged out. Warning')
    # messages.error(request, 'You logged out. Error')

    return redirect(reverse('login'))

def login_view(request):
    btn = 'Login'
    form = LoginForm(request.POST or None)
    
    if form.is_valid():
        print('VECHERINKA')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        #user.emailconfirmed.activate_user_email()
        messages.success(request, 'You are now logged in!')
    context = {
        'form': form,
        'btn': btn,
    }

    return render(request, 'form.html', context=context)



def registration_view(request):
    btn = 'Join'
    form = RegistrationForm(request.POST or None)
    
    if form.is_valid():
        print('VECHERINKA')
        new_user = form.save(commit=False)
        #this is where the form was submitted but wasn't saved yet!
        # new_user.first_name = 'Genochka' that's where we are going to change fields of our model
        new_user.save()
        messages.success(request, 'You are registered now! Please confirm your email!')
        return redirect ('/')
    context = {
        'form': form,
        'btn': btn,
    }

    return render(request, 'form.html', context=context)




def activation_view(request, activation_key):

    try:
        this_user = EmailConfirmed.objects.get(activation_key=activation_key)
        print('this_user:', this_user.user)
        if this_user.confirmed == True:
            context = {
                'this_user': this_user,
                'msg': 'Your Accaunt Was Previously Activated. No Activation Needed. Would you like to'
            }
        else:                 
            this_user.confirmed = True
            this_user.activation_key = 'Confirmed'
            this_user.save()
            context = {
                'this_user': this_user,
                'msg': 'Activation Complete! Thank You For Joining Gennady Team! Please ',
                
            }       
    except:
        print('WRONG ACTIVATION KEY')
        context = {
            'msg': 'Something Went Wrong :('
        }
    #if re.search(r'{this_user.activation_key}', activation_key):

    #     print('YES IT IS HERE')
    #     try:
    #         this_user = EmailConfirmed.objects.get(activation_key=activation_key)
    #         context={'this_user': this_user}
    #         this_user.confirmed = True
    #         this_user.save()
    #     except:
    #         context={'msg': 'Something went wrong :('}
    #         print('TY GOVNO I ZVAT TEBYA NIKAK')
    # else:
    #     print('Activation Key Is Not Valid')    
    #     context={'msg': 'Something went wrong ;('}

    return render(request, 'accounts/activation-complete.html', context=context)



def add_user_address(request):
    try:
        next_page = request.GET.get("next")
        print('GET REQUEST', request.GET)
    except:
        next_page = None
    if request.method == "POST":
        form = UserAddressForm(request.POST)
        if form.is_valid:
            new_address = form.save(commit=False) #что это за залупа такая и что мы вообще здесь присваиваем, пустую форму? Нихуя же не понятно!
            new_address.user = request.user
            new_address.save()
            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page)) + "?address-added=True")
    else:
        raise Http404

