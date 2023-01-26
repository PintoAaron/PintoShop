from django.urls import path,include
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter()
router.register(r'products',views.ProductViewset)
router.register(r'collections',views.CollectionViewset)

product_router = routers.NestedSimpleRouter(router,r'products',lookup = 'product')
product_router.register(r'reviews',views.ReviewViewset,basename='product-reviews')


urlpatterns = [
    path(r'',include(router.urls)),
    path(r'',include(product_router.urls)),
    path('orders/',views.OrderList.as_view()),
    path('orders/<int:pk>/',views.OrderDetail.as_view()),

    
    
]