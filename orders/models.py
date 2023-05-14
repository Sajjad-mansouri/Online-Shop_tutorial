from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse
from shop.models import Product

class Order(models.Model):
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	email=models.EmailField()
	address=models.CharField(max_length=300)
	city=models.CharField(max_length=50)
	postalcode=models.CharField(max_length=50)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	paid=models.BooleanField(default=False)

	def order_detail(self):
		url=reverse('admin-order',args=[self.id])
		return mark_safe(f'<a href="{url}">detail</a>')

	class Meta:
		ordering=['-created']

	def __str__(self):
		return f'order {self.id}'

	def get_total_cost(self):
		return sum(item.get_price() for item in self.order_items.all() )




class OrderItem(models.Model):
	order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
	product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
	price=models.DecimalField(max_digits=10,decimal_places=2)
	quantity=models.PositiveIntegerField()

	def __str__(self):
		return str(self.id)

	def get_price(self):
		return self.price*self.quantity



