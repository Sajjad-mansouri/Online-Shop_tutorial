from django.shortcuts import render
import time
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from cart.cart import Cart
from .models import OrderItem,Order
from .forms import OrderForm
from .tasks import order_created



def create_order(request):
	cart=Cart(request)
	if request.method=="POST":
		form=OrderForm(request.POST)
		if form.is_valid():
			order=form.save()
			for item in cart:
				OrderItem.objects.create(order=order,product=item['product'],quantity=item['quantity'],price=item['price'])


			cart.clear()
			# time.sleep(60)
			order_created.delay(order.id)
			return render(request,'orders/create_order_done.html',{'order':order})

	else:
		form=OrderForm()

	return render(request,'orders/create_order.html',{'form':form,'cart':cart})


@staff_member_required
def admin_order_detail(request,id):
	order=get_object_or_404(Order,id=id)
	return render(request,'orders/admin_order.html',{'order':order})