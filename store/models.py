from distutils.text_file import TextFile
from itertools import product
from tkinter import CASCADE, TRUE
from tokenize import blank_re
from turtle import color
from unicodedata import category
from django.db import models
from django.forms import CharField
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=80, blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', kwargs={"vagina": self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        all_slugs = []
        if self.slug is None:
            self.slug = slugify(self.name)
        #print('OBJECTS:', Item.objects.all())
        all_slugs += self.slug
        for i in Item.objects.all():
            all_slugs.append(i.slug)
        # print(all_slugs)
        # print('SKOLKO RAZ:', all_slugs.count(self.slug))
        
        super().save(*args, **kwargs)
        print('ID:', self.id)
        if all_slugs.count(self.slug) >= 1:
            self.slug = self.slug + str(self.id)
            super().save(*args, **kwargs)



                

    # print(sender)
    # print(instance)
    # print(created)
    # print(args, kwargs)


class Item(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(Category, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    update_defaults = models.BooleanField(default=False)
    # SMALL = 'SM'
    # MEDIUM = 'MD'
    # LARGE = 'LG'
    # SIZE_CHOICES = [
    #     (SMALL, 'Small'),
    #     (MEDIUM, 'Medium'),
    #     (LARGE, 'Large'),
    # ]
    # size = models.CharField(
    #     max_length=2,
    #     choices=SIZE_CHOICES,
    #     default=MEDIUM,
    # )

    # def is_upperclass(self):
    #     return self.size in {self.MEDIUM, self.LARGE}

    
    def get_absolute_url(self):
        return reverse('item-detail', kwargs={"anal": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        all_slugs = []
        if self.slug is None:
            self.slug = slugify(self.name)
       
        all_slugs += self.slug
        for i in Item.objects.all():
            all_slugs.append(i.slug)
   
        
        super().save(*args, **kwargs)
        # print('ID:', self.id)
        # if all_slugs.count(self.slug) >= 1:
        #     self.slug = self.slug + str(self.id)
        #     super().save(*args, **kwargs)




class VariationManager(models.Manager):

    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')
    
    def colors(self):
        return super(VariationManager, self).filter(active=True).filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package'),
)



class Variation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self):
        return self.title


def item_defaults(sender, instance, created, *args, **kwargs):
    print('YA VOOBSHE TO BLYAD V SIGNALAH?', instance)
    if instance.update_defaults:
        print('Shya Zaapdeitim Eti Defaults')
        categories = instance.category.all()
        print('CATEGORII GOVNA:', categories)
        for cat in categories:
            print('CATEGORY.ID:', cat.id)
            if cat.id == 5:
                print('MANDA GLUPAYA')
                small_size = Variation.objects.get_or_create(item=instance, category='size', title='Small')
                print('PIZDA')
                medium_size = Variation.objects.get_or_create(item=instance, category='size', title='Medium')
                large_size = Variation.objects.get_or_create(item=instance, category='size', title='Large')
                black_color = Variation.objects.get_or_create(item=instance, category='color', title='Black')
                white_color = Variation.objects.get_or_create(item=instance, category='color', title='White')
        instance.update_defaults = False
        instance.save()


post_save.connect(item_defaults, sender=Item)

    




