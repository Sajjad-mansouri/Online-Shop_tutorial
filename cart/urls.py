from django.urls import path
from . import views

urlpatterns=[
path('',views.cart_detail,name='cart-detail'),
path('add/<int:product_id>/',views.add_cart,name='add-cart'),
path('remove/<int:product_id>/',views.remove_cart,name='remove-cart')
]