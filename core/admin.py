from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin,ProductImageInline
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","email","first_name","last_name"),
            },
        ),
    )
    
    



class TagInline(GenericTabularInline):
    model = TaggedItem 
    autocomplete_fields = ['tag']
    extra = 0
    min_num = 1
    max_num = 10

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline,ProductImageInline]
    
admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)
