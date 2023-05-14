import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Order,OrderItem



def export_to_csv(modeladmin,request,queryset):
	opts=modeladmin.model._meta
	content_disposition=f'attachment;filename={opts.verbose_name}.csv'
	response=HttpResponse(content_type='text/csv')
	# response=HttpResponse() in this case show in page not downloadable
	response['Content_Disposition']=content_disposition
	fields=[field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many ]
	writer=csv.writer(response)
	writer.writerow([field.verbose_name for field in fields])

	
	for obj in queryset:
		data_row=[]
		for field in fields:
			value=getattr(obj,field.name)
			if isinstance(value,datetime.datetime):
				value=value.strftime('%Y%m%d')
			data_row.append(value)
		writer.writerow(data_row)
	return response

export_to_csv.short_description='export to csv'

class OrderItemInline(admin.TabularInline):
	model=OrderItem
	raw_id_fields = ['product']
	extra=2

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display=['first_name','last_name','email',
	'address','city','postalcode','paid','created','updated','order_detail']
	list_filter=['paid','created','updated']
	inlines=[OrderItemInline]
	actions=[export_to_csv]




