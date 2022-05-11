from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib import messages
from django.template.loader import render_to_string
import hashlib, random

from mywebsite.settings import SITE_URL

# Create your models here.


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.stripe_id)



class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.confirmed)

    # def create_hash(self):



    def activate_user_email(self):
        # activation_url = 'http://localhost:8000/accounts/activate/%s' %(self.activation_key) #эта хуета поменялась в УРОКЕ 52. По-моему было намного проще
        activation_url = '%s%s' %(settings.SITE_URL, (reverse('activation', args=[self.activation_key])))#эта хуета поменялась в УРОКЕ 52. По-моему было намного проще. Да еще и не робит в новой версии Джанго
        subject = 'Email Confirmation'
        context = {
            'activation_key': self.activation_key,
            'activation_url': activation_url,
            'user': self.user.username,
        }
        message = render_to_string('accounts/activation-message.txt', context)
        print('MESSAGE:', message)
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL, context)


    def email_user(self, subject, message, from_email=None, *kwargs):

        send_mail(subject, message, from_email, [self.user.email])





