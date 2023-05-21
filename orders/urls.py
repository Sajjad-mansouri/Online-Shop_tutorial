from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns=[

path('',views.create_order,name='create-order'),
path('admin/detail/<int:id>/',views.admin_order_detail,name='admin-order'),
path('admin/detail/pdf/<int:id>',views.admin_order_pdf,name='admin-pdf')

]