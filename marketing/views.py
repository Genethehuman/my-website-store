from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse
import json
from django.utils import timezone
import datetime
from django.conf import settings

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




