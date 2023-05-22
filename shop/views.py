from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from cart.forms import ProductCartForm
from .recommender import Recommender
import redis
from django.conf import settings
from cart.cart import Cart



def product_list(request,category_slug=None):

	for key in request.session.keys():
		value=request.session[key]
		print('key:',key,', value:',value)
	category=None
	categories=Category.objects.all()
	products=Product.objects.filter(available=True)

	if category_slug:
		category=get_object_or_404(Category,slug=category_slug)
		products=category.products.filter(available=True)

	
	return render(request,'shop/product/list.html',{'products':products,'categories':categories,'category':category})


def product_detail(request,id,product_slug):
	re=redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
	product_form=ProductCartForm()
	product=get_object_or_404(Product,id=id,slug=product_slug,available=True)
	r=Recommender()
	recommended_products=r.suggest_product_for([product],3)
	context={'product':product,'product_form':product_form,'recommended_products':recommended_products}
	return render(request,'shop/product/detail.html',context)

