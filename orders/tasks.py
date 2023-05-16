from celery import shared_task
import time
import io
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from .models import Order


@shared_task
def order_created(order_id):
	time.sleep(60)
	order=Order.objects.get(id=order_id)
	subject=f'order number is {order_id}'
	message = f'Dear {order.first_name},\n\n' \
				f'You have successfully placed an order.' \
				f'Your order ID is {order.id}.'

	mail_sent=send_mail(subject,message,'example@company.com',[order.email])
	return mail_sent

@shared_task
def email_pdf(order_id):
	order=Order.objects.get(id=order_id)
	subject=f'My shop -invoice no. {order_id}'
	message = f'Dear {order.first_name},\n\n' \
				f' please find your attached invoice.' 
			

	email=EmailMessage(subject,message,'example@company.com',[order.email])

	html_string=render_to_string('orders/order_pdf.html',{'order':order})
	out=io.BytesIO()
	html=HTML(string=html_string)
	stylesheets=[settings.STATICFILES_DIRS[0]/'css/pdf.css']
	html.write_pdf(stylesheets=stylesheets)
	email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
	email.send()


	
