from enum import unique
from random import choices
from turtle import title
from django.db import models
from django.forms import CharField


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete = models.SET_NULL,null=True, related_name = '+')


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places = 2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now = True)
    collection = models.ForeignKey(Collection,on_delete = models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null = True)
    
    
class Order(models.Model):
    PENDING_STATUS = 'P'
    COMPLETE_STATUS = 'C'
    FAILED_STATUS = 'F'
    
    PAYMENT_STATUS = [
        
        (PENDING_STATUS,'Pending'),
        (COMPLETE_STATUS,'Complete'),
        (FAILED_STATUS,'Failed')
    ]
    
    placed_at  = models.DateTimeField(auto_now_add = True)
    payment_status = models.CharField(max_length=1,choices = PAYMENT_STATUS,default = PENDING_STATUS)
    customer = models.ForeignKey(Customer,on_delete = models.PROTECT)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unitprice = models.DecimalField(max_digits=4, decimal_places = 2)
    
       
    
class Address(models.Model):
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key = True)
    
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField()