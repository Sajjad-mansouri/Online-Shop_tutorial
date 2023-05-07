from django.urls import path
from . import views

urlpatterns=[
path('',views.product_list,name='product-list'),
path('<slug:category_slug>',views.product_list,name='category-list'),
path('product/<int:id>/<slug:product_slug>/',views.product_detail,name='product-detail')
]