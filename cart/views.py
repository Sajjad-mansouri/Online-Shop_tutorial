from django.shortcuts import redirect,render,get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product
from .forms import ProductCartForm
from django.conf import settings
from coupons.forms import CouponForm
from shop.recommender import Recommender


@require_POST
def add_cart(request,product_id):
	cart=Cart(request)
	product=get_object_or_404(Product,id=product_id)
	form=ProductCartForm(request.POST)
	if form.is_valid():
		cd=form.cleaned_data
		quantity=cd['quantity']
		override=cd['override']
		cart.add(product=product,quantity=quantity,override_quantity=override)
		return redirect('cart-detail')


@require_POST
def remove_cart(request,product_id):
	cart=Cart(request)
	product=get_object_or_404(Product,id=product_id)
	cart.remove(product)
	return redirect('cart-detail')

def cart_detail(request):

	coupon_form=CouponForm()
	carts=Cart(request)

	for cart in carts:
		cart['updated_cart']=ProductCartForm(initial={'quantity':cart['quantity'],'override':True})
	r=Recommender()
	cart_product=[item['product'] for item in carts]
	if cart_product:
		recommendation=r.suggest_product_for(cart_product,max_result=4)
		print(recommendation)
	else:
		recommendation=[]


	context={'carts':carts,'coupon_form':coupon_form,'recommended_products':recommendation}
	return render(request,'cart/cart_detail.html',context)
