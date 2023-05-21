from django import forms
from django.utils.translation import gettext_lazy as _

class ProductCartForm(forms.Form):
	PRODUCT_QUANTITY_CHOICES=[(i,str(i)) for i in range(1,11)]
	quantity=forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int,label=_('quantity'))
	override=forms.BooleanField(widget=forms.HiddenInput,required=False,initial=False)