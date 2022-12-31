from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline


class TagInline(GenericTabularInline):
    model = TaggedItem 
    autocomplete_fields = ['tag']
    extra = 0
    min_num = 1
    max_num = 10

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]
    
admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)
