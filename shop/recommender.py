import redis
from django.conf import settings
from .models import Product

r=redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


class Recommender:

	def get_product_key(self,id):
		return f'product:{id}:purchased_with'

	def product_bought(self,products):
		products_id=[p.id for p in products]
		for product_id in products_id:
			for with_id in products_id:
				if product_id != with_id:
					r.zincrby(self.get_product_key(product_id),1,with_id)


	def suggest_product_for(self,products,max_result=6):
		products_id=[p.id for p in products]
		if len(products_id)==1:
			suggestions=r.zrange(self.get_product_key(products_id[0]),0,-1,desc=True)[:max_result]

		else:
			flat_ids=''.join([str(id) for id in products_id])
			tmp_key=f'tmp_{flat_ids}'
			keys=[self.get_product_key(id) for id in products_id]
			r.zunionstore(tmp_key,keys)
			r.zrem(tmp_key,*products_id)
			suggestions=r.zrange(tmp_key,0,-1,desc=True)[:max_result]
			r.delete(tmp_key)

		suggested_products_id=[int(id) for id in suggestions]
		suggested_products=list(Product.objects.filter(id__in=suggested_products_id))
		suggested_products.sort(key=lambda x: suggested_products_id.index(x.id))
		return suggested_products


	def clear_purchase(self):
		for id in Product.objects.values_list(id,flat=True):
			r.delete(self.get_product_key(id))


