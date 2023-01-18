from django.urls import path
from . import views

urlpatterns = [
    
    path('products/',views.Productlist.as_view()),
    path('products/<int:id>/',views.ProductDetail.as_view()),
    path('orders/', views.order_list),
    path('orders/<int:id>',views.order_detail),
    path('collections/',views.CollectionList.as_view()),
    path('collections/<int:id>/',views.CollectionDetail.as_view())
   
   
]