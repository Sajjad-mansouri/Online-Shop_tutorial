from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator,MaxValueValidator
from django.urls import reverse
from decimal import Decimal
from shop.models import Product
from coupons.models import Coupon

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
	coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,related_name='order',null=True,blank=True)
	discount=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],default=0)

	def order_detail(self):
		url=reverse('admin-order',args=[self.id])
		return mark_safe(f'<a href="{url}">detail</a>')

	class Meta:
		ordering=['-created']

	def __str__(self):
		return f'order {self.id}'

	def price_before_discount(self):
		return  sum([item.price*item.quantity for item in self.order_items.all()])

	def get_discount(self):
		total_price=self.price_before_discount()
		if self.discount:
			return total_price*(self.discount/Decimal(100))
		return Decimal(0)
	def get_total_price(self):
		total_price=self.price_before_discount()
		return total_price-self.get_discount()




class OrderItem(models.Model):
	order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
	product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
	price=models.DecimalField(max_digits=10,decimal_places=2)
	quantity=models.PositiveIntegerField()

	def __str__(self):
		return str(self.id)

	def get_price(self):
		return self.price*self.quantity



