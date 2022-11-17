from django.urls import path
from . import views

urlpatterns = [
    
    path('hello/',views.Get_tags,name='Hello'),
   
   
]