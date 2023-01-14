from decimal import Decimal
from rest_framework import serializers
from .models import Product,Customer,Order,Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #collection = CollectionSerializer()
    
    
    def calculate_tax(self , product:Product):
        return product.unit_price * Decimal(1.1)
    
    
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','first_name','last_name','email','phone','birth_date','membership']
   # id = serializers.IntegerField()
   #first_name = serializers.CharField(max_length = 255)
   #last_name = serializers.CharField(max_length = 255)



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','placed_at','customer']
    
    customer = serializers.StringRelatedField()    
    
    #id = serializers.IntegerField()
    #placed_at = serializers.DateTimeField()
    #customer = serializers.StringRelatedField()        
    