from django.conf import settings
from shop.models import Product
class Cart:
	 def __init__(self,request):
	 	self.request=request
	 	self.session=request.session
	 	self.cart=request.session.get(settings.CART_SESSION_ID,{})

	def __add__(self,product,quantity=1,override_quantity=False):
		product_id=str(product_id)
		if product.id not in  self.cart.keys():
			self.cart['product_id']={
				'quantity':0,
				'price':str(product.price)
			}
		if override_quantity:
				self.cart['product_id']['quantity']=quantity

		else:
				self.cart['product_id']['quantity']+=quantity

		self.save()

	def remove(self,product):
		product_id=str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		product_id=self.cart.keys()
		products=Product.objects.filter(id__in=product_id)
		cart=self.cart.copy()
		for product in products:
			cart['product']=product
		for item in self.cart.values():
			item['price']=Decimal(item['price'])
			irem['total_price']=item['price']*item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity']) for item in self.cart.values()	

	def get_total_price(self):
		return sum(Decima(item['price'])*item['quantity'] for item in self.cart.values()	)

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.save() 

	def save(self):
		self.session.modified=True
		