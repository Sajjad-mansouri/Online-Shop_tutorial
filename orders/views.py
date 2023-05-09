from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderForm


def create_order(request):
	cart=Cart(request)
	if request.method=="POST":
		form=OrderForm(request.POST)
		if form.is_valid():
			order=form.save()
			for item in cart:
				OrderItem.objects.create(order=order,product=item['product'],quantity=item['quantity'],price=item['price'])


			cart.clear()
			return render(request,'orders/create_order_done.html',{'order':order})

	else:
		form=OrderForm()

	return render(request,'orders/create_order.html',{'form':form,'cart':cart})