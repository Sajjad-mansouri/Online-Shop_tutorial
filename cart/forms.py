from django import forms

class ProductCartForm(forms.Form):
	PRODUCT_QUANTITY_CHOICES=[(i,str(i)) for i in range(1,11)]
	quantity=forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
	override=forms.BooleanField(widget=forms.HiddenInput,required=False,initial=False)