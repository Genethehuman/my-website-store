from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from tkinter import CASCADE
from django.db import models
from accounts.models import UserAddress
from cart.models import Cart

# Create your models here.

STATUS_CHOICES =(
    ('Started', 'Started'),
    ('Abandoned', 'Abandoned'),
    ('Finished', 'Finished'),
)

tax_rate = settings.DEFAULT_TAX_RATE

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    #assign address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    sub_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    final_price = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    user_shipping = models.ForeignKey(UserAddress, null=True, on_delete=models.CASCADE, related_name='user_shipping')
    user_billing = models.ForeignKey(UserAddress, max_length=350, null=True, on_delete=models.CASCADE, related_name='user_billing')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    stripe_payment_intent = models.CharField(max_length=120, null=True, blank=True)
    

    def __str__(self):
        return self.order_id

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        instance.tax_total = tax_rate * float(self.sub_total)
        print('TAX:', instance.tax_total)
        print('SELF.SUB_TOTAL:', self.sub_total)
        instance.final_price = float(self.sub_total) + instance.tax_total
        print('FINAL PRICE IN METHOD:', instance.final_price)
        instance.save()
        return instance.final_price



