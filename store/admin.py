from django.contrib import admin
from .models import Item, Category, Variation

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'id']
    ordered = ['id']

    search_fields = ['name', 'description']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'id']
    ordered = ['id']
    search_fields = ['name', 'description']

admin.site.register(Variation)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)