from django.conf import settings
from shop.models import Product
from coupons.models import Coupon
from decimal import Decimal
class Cart:
	def __init__(self,request):
	 	
	 	self.session=request.session
	 	cart=request.session.get(settings.CART_SESSION_ID)
	 	if not cart:
	 		cart=self.session[settings.CART_SESSION_ID]={}
	 	self.cart=cart
	 	self.coupon_id=request.session['coupon_id']



	def add(self,product,quantity=1,override_quantity=False):
		product_id=str(product.id)
		if product_id not in  self.cart.keys():
			self.cart[product_id]={
				'quantity':0,
				'price':str(product.price)
			}
		if override_quantity:
				self.cart[product_id]['quantity']=quantity

		else:
				self.cart[product_id]['quantity']+=quantity

		self.save()


	def remove(self,product):
		product_id=str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	@property
	def coupon(self):
		if self.coupon_id:
			try:
				coupon_obj=Coupon.objects.get(id=self.coupon_id)
				return coupon_obj
			except Coupon.DoesNotExist :		
				pass
		return None
		
	@property
	def discount(self):
		if self.coupon:
			return (self.coupon.discount/Decimal(100))*self.get_total_price()
		return Decimal(0)

	def __iter__(self):
		product_id=self.cart.keys()
		products=Product.objects.filter(id__in=product_id)
		cart=self.cart.copy()
		for product in products:
			cart[str(product.id)]['product']=product
		for item in self.cart.values():
			item['price']=Decimal(item['price'])
			item['total_price']=item['price']*item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values()	) 

	def get_total_price(self):
		return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

	def get_total_price_with_discount(self):
		price=self.get_total_price()-self.discount
		del self.coupon_id
		return price

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.save() 

	def save(self):
		self.session.modified = True

		