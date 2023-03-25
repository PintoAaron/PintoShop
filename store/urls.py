from django.urls import path,include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register(r'products',views.ProductViewset,basename='product')
router.register(r'collections',views.CollectionViewset)
router.register(r'carts',views.CartViewset)
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewSet,basename='orders')

product_router = routers.NestedDefaultRouter(router,r'products',lookup = 'product')
product_router.register(r'reviews',views.ReviewViewset,basename='product-reviews')
product_router.register('images',views.ProductImageViewSet,basename='product-images')
cart_router = routers.NestedDefaultRouter(router,r'carts',lookup ='cart')
cart_router.register(r'items',views.CartItemViewset,basename='cart-items')


urlpatterns = [
    path(r'',include(router.urls)),
    path(r'',include(product_router.urls)),
    path(r'',include(cart_router.urls))


] 