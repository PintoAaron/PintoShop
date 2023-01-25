from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views


router  = SimpleRouter()
router.register('products',views.ProductViewset)
router.register('collections',views.CollectionViewset)

urlpatterns = [
    path('',include(router.urls)),
    path('orders/',views.OrderList.as_view()),
    path('orders/<int:pk>/',views.OrderDetail.as_view()),
    
]