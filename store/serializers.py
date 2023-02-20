from decimal import Decimal
from rest_framework import serializers
from .models import Product,Customer,Order,Collection,Review,Cart,CartItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    
    products_count = serializers.IntegerField(read_only = True)
    
   
 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #collection = CollectionSerializer()
    
    
    def calculate_tax(self , product:Product):
        return product.unit_price * Decimal(1.1)
    
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','placed_at','customer','order_items']
        
    order_items = serializers.IntegerField(read_only = True)
    customer = serializers.StringRelatedField()    
    
    #id = serializers.IntegerField()
    #placed_at = serializers.DateTimeField()
    #customer = serializers.StringRelatedField()        
    
    
class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id','name','description','date','product']
        


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']      
      
        

 
    
    
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','quantity','product','total_price']
        
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price
        
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','items','total_price']
        
        
    items = CartItemSerializer(many= True,read_only = True)    
    id = serializers.UUIDField(read_only = True)
    
    total_price = serializers.SerializerMethodField(method_name="get_total_price")
    
    def get_total_price(self,cart):
       return  sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']
        
    product_id = serializers.IntegerField()
    
    def validate_product_id(self,value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('No Product with this Id exits')
        return value
    
    
   
    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id,product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
            
        return self.instance
 
 
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
         model  = CartItem
         fields = ['quantity']
         
    
    
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Customer 
        fields = ['id','user_id','phone','birth_date','membership']
        
    
        
        