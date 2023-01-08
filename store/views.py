from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Customer,Order
from .serializers import ProductSerializer,OrderSerializer




@api_view()
def product_list(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set, many = True)
    result = serializer.data
    return Response(result)


@api_view()
def product_detail(request,id):
    #catch 404 or object not found errors
    product = get_object_or_404(Product,pk = id)
    #product = Product.objects.get(pk=id)
    serializer = ProductSerializer(product)
    result = serializer.data
    return Response(result)



@api_view()
def order_list(request):
    query_set = Order.objects.select_related('customer').all()
    serializer = OrderSerializer(query_set,many=True)
    return Response(serializer.data)

@api_view()
def order_detail(request,id):
    try:
        order = Order.objects.select_related('customer').get(pk = id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        

