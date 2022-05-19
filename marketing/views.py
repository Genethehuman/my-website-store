from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse
import json
from django.utils import timezone
import datetime
from django.conf import settings
from .forms import EmailForm


# def email_signup(request):
#     if request.method == "POST":
#         print(request.POST)
#         form = EmailForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data('email')

def dismiss_marketing_message(request):
    if request.is_ajax():
        data = {"success": True}
        print('TIME NOW', timezone.localtime(timezone.localtime(timezone.now())))
        print(data)
        json_data = json.dumps(data)
        request.session['dismiss_message_for'] = str(timezone.localtime(timezone.now()) + datetime.timedelta(settings.MARKETING_DISMISS_OFFSET))
        print(json_data)
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def email_signup(request):

    form = EmailForm(request.POST)
    if form.is_valid():
        # print(form.cleaned_data['email'])
        email = form.cleaned_data['email']
        return HttpResponse('Success' + email)
    else:
        raise Http404




