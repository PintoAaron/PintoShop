from django.contrib import admin
from django.db.models import Count
from . import models

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at','payment_status','customer']
    list_editable = ['payment_status']
    list_per_page = 10
    ordering = ['placed_at']
    list_select_related = ['customer']
    

    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','inventory_status','collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    
    #def collection_title(self,product):
    #    return product.collection.title
    
    @admin.display(ordering = 'inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    ordering = ['first_name','last_name']
    list_editable = ['membership']
    list_per_page = 10
    

    
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    list_per_page = 10
    
    
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        return collection.products_count
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count = Count('product'))



@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_select_related = ['order','product']
    list_display = ['product_name','order_status','order_date']
    list_per_page = 10
    
    
    
    def order_date(self,orderitem):
        return orderitem.order.placed_at
    
    def order_status(self,orderitem):
        return orderitem.order.payment_status
    
    def product_name(self,orderitem):
        return orderitem.product.title
    