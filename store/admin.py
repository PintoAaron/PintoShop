from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse 
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10','Low'),
            ('>10','Ok')
        ]
        
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)
        return queryset.filter(inventory__gte = 10)

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['id','placed_at','payment_status','customer_name','number_of_items']
    list_editable = ['payment_status']
    list_per_page = 10
    ordering = ['placed_at']
    list_select_related = ['customer']
    list_filter = ['payment_status']
    
    @admin.display(ordering= 'customer')
    def customer_name(self,order):
       f_name = order.customer.user.first_name
       l_name = order.customer.user.last_name
       name = f'{f_name} {l_name}'
       url = ( reverse('admin:store_address_changelist') + '?' + urlencode({'customer__id':str(order.customer.id)}) )
       return format_html('<a href="{}">{}</a>', url, name)
   
    @admin.display(ordering='order_items')
    def number_of_items(self,order):
        url = (reverse('admin:store_orderitem_changelist') + '?' + urlencode({'order__id':str(order.id)}))
        return format_html('<a href="{}">{}</a>',url,order.order_items)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_items = Count('orderitems'))
       

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']
    
    def thumbnail(self,instance):
        if instance.image.name != '':
            return format_html(f'<img src ="{instance.image.url}" class = "thumbnail" />')
        return ''


    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = { 'slug': ['title'] }
    inlines = [ProductImageInline]
    actions = ['clear_inventory']
    list_display = ['title','unit_price','inventory_status','collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection',InventoryFilter]
    search_fields = ['title__istartswith']
    
    #def collection_title(self,product):
    #    return product.collection.title
    
    @admin.display(ordering = 'inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    
    @admin.action(description = 'clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.'
        )
        
    class Media:
        css = {'all':['store/styles.css']}


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','membership','birth_date','orders_count',]
    ordering = ['user__first_name','user__last_name']
    list_editable = ['membership']
    list_per_page = 10
    list_filter = ['membership']
    search_fields = ['first_name__istartswith','last_name__istartswith']
    list_select_related = ['user']
    
    @admin.display(ordering = 'orders_count')
    def orders_count(self,customer):
        #return customer.orders_count
        url = (reverse('admin:store_order_changelist') + '?' + urlencode({'customer__id':str(customer.id)}))
        return format_html('<a href="{}">{}</a>',url,customer.orders_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count = Count('order'))
    

    
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['id','title','products_count']
    list_per_page = 10
    search_fields = ['title']
   
    
    
    @admin.display(ordering='products_count')
    def products_count(self,collection):
       url = ( reverse('admin:store_product_changelist')  + '?' + urlencode({'collection__id':str(collection.id)}) )
       return format_html('<a href="{}">{}</a>',url,collection.products_count)
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count = Count('products'))



@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_select_related = ['order','product']
    list_display = ['product_name','order_id','order_status','order_date']
    list_per_page = 10
    
    
    
    def order_date(self,orderitem):
        return orderitem.order.placed_at
    

    def order_id(self,orderitem):
        url = ( reverse('admin:store_orderitem_changelist')  + '?' + urlencode({'order__id':str(orderitem.order.id)}) )
        return format_html('<a href="{}">{}</a>',url,orderitem.order.id)
    
    
    def order_status(self,orderitem):
        state =  orderitem.order.payment_status
        state_dict = {
            'F':'Failed',
            'P':'Pending',
            'C':'Complete'
        }
        
        return state_dict.get(state)
    
    def product_name(self,orderitem):
        return orderitem.product.title
    
    
    
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['zip','city','street','customer']
    list_select_related = ['customer']
    list_editable = ['city','street']
    list_per_page = 10
    ordering = ['city']
    
    
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','created_at','cart_items']
    list_per_page = 10
    
    @admin.display(ordering='cart_items')
    def cart_items(self,cart):
        url = (reverse('admin:store_cartitem_changelist') + '?' + urlencode({'cart__id':str(cart.id)}))
        return format_html('<a href="{}">{}</a>',url,cart.cart_items)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(cart_items= Count('items'))
    
@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','cartId']
    list_select_related = ['cart','product']
    list_per_page = 10
    
    def cartId(self,cart_item):
        return cart_item.cart.id

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ['product']
    list_display = ['id','name','product_name','description','date']
    list_per_page = 10
    list_select_related = ['product']
    search_fields = ['name__istartswith','description']
    #list_filter = ['lastupdate']
    
    
    def product_name(self,review):
        url = (reverse('admin:store_product_changelist') + '?' + urlencode({'product__id':str(review.product.id)}))
        return format_html('<a href="{}">{}</a>',url,review.product.title)
        