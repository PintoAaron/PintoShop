import re
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail,mail_admins,BadHeaderError, EmailMessage
from django.db.models import Q,F,Count,Value
from django.db.models.aggregates import Count,Max,Min,Avg
from django.db.models.functions import Concat
from django.db import transaction,connection
from templated_mail.mail import BaseEmailMessage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product,Customer,Collection,Order,OrderItem,Cart,CartItem
from tags.models  import TaggedItem
from store.serializers import ProductSerializer





def Hello(request):
    #orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:10]
    #most_expensive_item = Order.objects.aaggregate(max_price = Max('unit_price'))
    query_set = OrderItem.objects.values('product_id').distinct()
    products = Product.objects.filter(id__in = query_set).order_by('title')
    #products = query_set.order_by('-unit_price','inventory')[:10]
    #query_set =  Product.objects.only('title','inventory','unit_price')
    #products = query_set.filter(inventory__lt = 10,unit_price__gt = 20).order_by('unit_price')[:10]
    #products = query_set.filter(Q(inventory__lt = 10) | Q(unit_price__lt = 20))
    #products = query_set.filter(inventory = F('unit_price'))
    #products = Product.objects.filter(Q(title__istartswith= 'Bar') | Q(title__iendswith='ers')).annotate(new_id = F('id')+1).order_by('title')[:10]
    #orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
  
    context = {'products':list(products)}
    return render(request,'products.html',context)


def Get_tags(request):
    query_set = TaggedItem.objects.get_tags_for(Product,2)
    
    context = {'tag':list(query_set)}
    
    return render(request,'hello.html',context)

@transaction.atomic
def shopping(request):
    new_cart = Cart()
    new_cart.save()
    
    new_cartItem = CartItem()
    new_cartItem.cart = new_cart
    new_cartItem.product = Product(pk = 2)
    new_cartItem.quantity = 8
    new_cartItem.save()
    
    
    return render(request,'shopingCart.html')


@api_view()
def raw_query(request):
   with connection.cursor() as cursor:
       a = cursor.execute("SELECT id,title,unit_price,inventory FROM store_product WHERE inventory >= 10 and unit_price < 20")
       #cursor.callproc('summarize_orderitems')
       items = ProductSerializer(a)
    
   return Response(items.data)


def mails(request):
    try:
        #send_mail('Activate Your Account','Please you have to activate your account to conti9nue shopping with us.',settings.DEFAULT_FROM_EMAIL,['aaron@gmail.com'])
        message = EmailMessage('Requested Image','Please you have to activate your account to conti9nue shopping with us.','from@admin.com',['aaron@gmail.com'])
        message.attach_file('playground/static/images/category.png')
        message.send()
    except BadHeaderError:
        pass
    return HttpResponse('mail Successfully Sent')


def template_mail(request):
    try:
        message = BaseEmailMessage(
        template_name= 'emails/mail.html',
        context= {'name': 'Macquena'}
        )
        message.attach_file('playground/static/images/category.png')
        message.send(['Bod@gmail.com'])
    except BadHeaderError:
        pass 
    return HttpResponse('Mail Successfully Delivered')
    

       
    








