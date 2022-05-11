from tkinter import CASCADE
from django.db import models
from store.models import Item, Category

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']
        db_table = 'Cart'

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        sub_total = self.item.price * self.quantity
        return sub_total

    def __str__(self):
        return self.item
