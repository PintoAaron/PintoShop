from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin,UpdateModelMixin
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .models import Product,Customer,Order,Collection,OrderItem,Review,Cart,CartItem,ProductImage
from .serializers import ProductSerializer,ProductImageSerializer,OrderSerializer,UpdateOrderSerializer,CustomerSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,CreateOrderSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly,ViewCustomerHistoryPermission


'''    
class Productlist(APIView):
    def get(self,request):
        query_set = Product.objects.all()
        serializer  = ProductSerializer(query_set,many = True)
        return Response(serializer.data)
     
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED) 

'''
'''
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
'''


'''
class ProductDetail(APIView):
    def get(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,id):
        product = get_object_or_404(Product,pk =id)
        if product.orderitems.count() > 0:
            return Response({"error":"Producrt cant be deleted because it has being associated with an order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({"status":"Product is successfully deleted"},status=status.HTTP_204_NO_CONTENT)
'''


'''
class ProductList(ListCreateAPIView):
        queryset = Product.objects.select_related('collection').all()
        serializer_class = ProductSerializer
        
        def get_serializer_context(self):
            return {'request':self.request}
'''
   
'''                
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def delete(self,request,pk):
        product = get_object_or_404(Product,pk = pk)
        if product.orderitems.count() > 0:
            return Response({"error":"Product cant be deleted because it is associated with an order"},status= status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({"Status":"Product successfully deleted"},status=status.HTTP_204_NO_CONTENT)
'''
    
class ProductViewset(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title','description']
    ordering_fields = ['unit_price']
    
        
    def get_serializer_context(self):
        return {'request':self.request}
    
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({"error":"Product cant be deleted because it is associated with an order"},status= status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

'''
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
'''

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
''' 
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
'''    

'''
class CollectionList(APIView):
    def get(self,request):
        query_set = Collection.objects.annotate(products_count = Count('products')).all()
        serializer = CollectionSerializer(query_set,many =True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CollectionSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''          
   
'''

class CollectionDetail(APIView):
    def get(self,request,id):
        collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')),pk =id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    def put(self,request,id):
        collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')),pk =id)
        serializer = CollectionSerializer(collection,data =request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,id):
        collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')),pk =id)
        if collection.products.count() > 0:
            return Response({"error":"Cant delete collection because there are products in this collection"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({"status":"Collection Successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
        
 '''
 
  
'''
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
'''

   
'''           
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset =  Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    
    def delete(self,request,pk):
        collection = get_object_or_404(Collection,pk = pk)
        if collection.products.count() > 0:
            return Response({"error":"collection cannot be deleted because there are items in this collection "},status= status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({"status":"collection successfully deleted"},status=status.HTTP_204_NO_CONTENT)

'''

class CollectionViewset(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
            return Response({"error":"collection cannot be deleted because there are items in this collection "},status= status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

'''
@api_view(['GET','PUT','DELETE'])        
def collection_detail(request,id):
    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')),pk=id)
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
        
'''

'''

class OrderList(APIView):
    def get(self,request):
        query_set = Order.objects.select_related('customer').annotate(order_items= Count('orderitems')).all()
        serializer = OrderSerializer(query_set,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = OrderSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''


'''    
    
class OrderDetail(APIView):
    def get(self,request,pk):
        order = get_object_or_404(Order.objects.select_related('customer').annotate(order_items= Count('orderitems')),pk = pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def put(self,request,pk):
        order = get_object_or_404(Order.objects.select_related('customer').annotate(order_items= Count('orderitems')),pk = pk)
        serializer = OrderSerializer(order,data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(serializer.data)
    
    
    def delete(self,request,pk):
        order = get_object_or_404(Order,pk = pk)
        if order.orderitems.count()> 0:
            return Response({"error":"Order cant be deleted because there are order items in this order "},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        order.delete()
        return Response({"status":"Order Successfully deleted"},status=status.HTTP_204_NO_CONTENT)
'''        
        
        

class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
class CartViewset(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
class CartItemViewset(ModelViewSet):
    http_method_names = ['get','post','delete','patch']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).select_related('product')
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    
    
    #def get_permissions(self):
    #    if self.request.method == 'GET':
    #        return [AllowAny()]
    #    return [IsAuthenticated()]
    
    
    @action(detail=True,permission_classes = [ViewCustomerHistoryPermission])
    def history(self,request,pk):
        return Response(request.user.id)
    
    @action(detail=False,methods=['GET','PUT'],permission_classes = [IsAuthenticated])
    def me(self,request):
        customer = Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete','head','options']
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    
    def create(self, request, *args, **kwargs):
        seriaizer = CreateOrderSerializer(data = request.data,context = {'user_id':self.request.user.id})
        seriaizer.is_valid(raise_exception=True)
        order = seriaizer.save()
        seriaizer = OrderSerializer(order)
        return Response(seriaizer.data)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        customer = Customer.objects.only('id').get(user_id = self.request.user.id)
        return Order.objects.filter(customer_id = customer)
    


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    
    
    def get_queryset(self):
         return ProductImage.objects.filter(product_id = self.kwargs['product_pk'])
    
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    

        
