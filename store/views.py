from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Customer,Order,Collection
from .serializers import ProductSerializer,OrderSerializer,CollectionSerializer




@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':   
        query_set = Product.objects.all()
        serializer = ProductSerializer(query_set, many = True)
        return Response(serializer.data)
    elif request.method =='POST':
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status= status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product = get_object_or_404(Product,pk = id)
    if request.method =='GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method =='DELETE':
        if product.orderitems.count() > 0:
            return Response({'error':"Product can't be deleted because it has being associated with an order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() 
        return Response({'status':'Product Successfully Deleted'},status= status.HTTP_204_NO_CONTENT)   



@api_view(['GET','POST'])
def order_list(request):
    if request.method == 'GET':   
        query_set = Order.objects.select_related('customer').all()
        serializer = OrderSerializer(query_set,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

'''
@api_view()
def order_detail(request,id):
    try:
        order = Order.objects.select_related('customer').get(pk = id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

'''    
@api_view()
def order_detail(request,id):
    order = get_object_or_404(Order,pk=id)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
 
@api_view(['GET','POST'])            
def collection_list(request):
    if request.method == 'GET':
        query_set = Collection.objects.annotate(products_count = Count('products')).all()
        serializer = CollectionSerializer(query_set,many = True)
        return Response(serializer.data)
    elif request.method =='POST':
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
   
@api_view(['GET','PUT','DELETE'])        
def collection_detail(request,id):
    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')).all(),pk=id)
    if request.method =='GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({"error":"Collection can't be deleted becuase there are items in this collection."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({"status":"Collection Successfully Deleted"},status=status.HTTP_204_NO_CONTENT)
        
