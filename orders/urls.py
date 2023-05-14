from django.urls import path
from . import views

urlpatterns=[

path('',views.create_order,name='create-order'),
path('admin/detail/<int:id>/',views.admin_order_detail,name='admin-order'),

]