from django.urls import path
from . import views

urlpatterns = [
    
    path('hello/',views.Hello,name='Hello'),
    path('shopping/',views.shopping,name='shopping'),
    path('raw/',views.raw_query,name = 'raw_query')
   
   
]