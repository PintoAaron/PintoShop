from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,Customer,Order
from .serializers import ProductSerializer




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

