from django.contrib.auth.models import User
from tkinter import CASCADE
from django.db import models
from cart.models import Cart

# Create your models here.

STATUS_CHOICES =(
    ('Started', 'Started'),
    ('Abandoned', 'Abandoned'),
    ('Finished', 'Finished'),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    #assign address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    sub_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    final_price = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='started')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.order_id



