from django.shortcuts import render,get_object_or_404
from .models import Product,Category




def product_list(request,category_slug=None):
	category=None
	categories=Category.objects.all()
	products=Product.objects.filter(available=True)
	if category_slug:
		category=get_object_or_404(Category,slug=category_slug)
		products=category.products.filter(available=True)

	
	return render(request,'shop/product/list.html',{'products':products,'categories':categories,'category':category})


def product_detail(request,id,product_slug):
	product=get_object_or_404(Product,id=id,slug=product_slug,available=True)
	return render(request,'shop/product/detail.html',{'product':product})

