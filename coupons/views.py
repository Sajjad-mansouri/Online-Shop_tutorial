from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Coupon
from .forms import CouponForm



def apply_coupon(request):
	coupon_form=CouponForm(request.POST)
	if coupon_form.is_valid():
		code=coupon_form.cleaned_data['code']
		time=timezone.now()
		try:
			print('before')
			
			coupon=Coupon.objects.get(code__iexact=code,
										valid_from__lte=time,
										valid_to__gte=time,
										active=True)

			
			request.session['coupon_id']=coupon.id
		except Coupon.DoesNotExist as e:
			request.session['coupon_id']=None

	coupon_form=CouponForm()
	return redirect('cart-detail')

