import stripe

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from .models import UserStripe, EmailConfirmed
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model

#User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

# if we decide to decide to change how we add stripe id, that's where we set it for a user_logged_in
# def get_or_create_stripe(sender, user, *args, **kwargs):
#     #print(sender)
#     print('I SNOVA SEDAYA NOCH:', user.email)
#     try:
#         my_user_id = user.userstripe.stripe_id
#         #print(my_user_id)
#     except UserStripe.DoesNotExist:           
#         customer = stripe.Customer.create(
#             email = user.email
#         )
#         new_user_stripe = UserStripe.objects.create(
#             user=user,
#             stripe_id=customer.id,
#         )
#     except:
#         pass

# user_logged_in.connect(get_or_create_stripe)

# def get_create_user_stripe(user):
#     try:
#         user.userstripe.stripe_id
#         #print(my_user_id)
#     except UserStripe.DoesNotExist:           
#         customer = stripe.Customer.create(
#             email = user.email
#         )
#         print('CUSTOMER:', customer)
#         new_user_stripe = UserStripe.objects.create(
#             user=user,
#             stripe_id=customer.id,
#         )
#         print('NEW_USER_STRIPE:', new_user_stripe)
#     except:
#         pass

def get_create_user_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
            email = user.email
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()





def user_created(sender, instance, created, *args, **kwargs): #Какого хера мы здесь использвуем инстанс а не Юзер, и кто вообще решает, какие аргументы мы можем вписывать и использовать в функции, а какие нет!?!?!?!
    user = instance                                            #Ответ: Да, потому что в сигнале типа КОННЕКТ, том что внизу, нету аргумента ЮЗЕР, который мог бы на него подаваться, а ИНСТАНС есть. Поэтому нам удобно сделать переменную ЮЗЕР, которая по сути будет инстансом.
    print('INSTANCE:', instance)
    if created:
        get_create_user_stripe(user)
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            line = (str(random.random())).encode('utf-8')
            short_hash = hashlib.sha1(line).hexdigest()[:5]
            username = 'Gennady'
            hash = hashlib.sha1((short_hash + username).encode('utf-8')).hexdigest()
            email_confirmed.activation_key = hash
            print('ACTIVATION_KEY:', email_confirmed.activation_key)
            email_confirmed.save()
            email_confirmed.activate_user_email()
            email_confirmed.save()
        # 


post_save.connect(user_created, sender=settings.AUTH_USER_MODEL)






import random, hashlib
line = (str(random.random())).encode('utf-8')
short_hash = hashlib.sha1(line).hexdigest()[:5]
username = 'Gennady'
hash = hashlib.sha1((short_hash + username).encode('utf-8')).hexdigest()
