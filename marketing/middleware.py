from django.views import View
from .models import MarketingMessage
from django.utils.deprecation import MiddlewareMixin

class DisplayMarketing(MiddlewareMixin):
    def process_request(self, request):
        print('ZHOPKA')
        try:
            request.session['marketing_message'] = MarketingMessage.objects.all()[0].message
            print(request.session['marketing_message'])
        except:
            request.session['marketing_message'] = False