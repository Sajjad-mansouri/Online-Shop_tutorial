from django.urls import path
from . import views

urlpatterns=[
	path('apply_coupon/',views.apply_coupon,name='apply-coupon')
]