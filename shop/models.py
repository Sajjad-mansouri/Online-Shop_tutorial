from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel,TranslatedFields

class Category(TranslatableModel):
	translations=TranslatedFields(
		name=models.CharField(max_length=100),
		slug=models.SlugField(max_length=100),
			)


 
	def get_absolute_url(self):
		return reverse('category-list',args=[self.slug])
	def __str__(self):
		return self.name


class Product(models.Model):
	category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
	name=models.CharField(max_length=100)
	slug=models.SlugField(max_length=100)
	image=models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
	description=models.TextField()
	price=models.DecimalField(max_digits=10,decimal_places=2)
	available=models.BooleanField(default=False)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	class Meta:
		indexes=[
		models.Index(fields=['id','slug'])]
	def get_absolute_url(self):
		return reverse('product-detail',args=[self.id,self.slug])
	def __str__(self):
		return self.name
