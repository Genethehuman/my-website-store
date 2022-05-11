from tkinter import CASCADE
from django.db import models
from store.models import Item, Category, Variation




class Cart(models.Model):
    #cart_items = models.ManyToManyField(CartItem, blank=True)
    # items = models.ManyToManyField(Item, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Cart id: %s" %(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(max_digits=100, decimal_places=2, default=20.00)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)

    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.cart_item.name




    

