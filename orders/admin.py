from django.contrib import admin
from .models import Order,OrderItem

class OrderItemInline(admin.TabularInline):
	model=OrderItem
	raw_id_fields = ['product']
	extra=2

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display=['first_name','last_name','email','address','city','postalcode','paid','created','updated']
	list_filter=['paid','created','updated']
	inlines=[OrderItemInline]




