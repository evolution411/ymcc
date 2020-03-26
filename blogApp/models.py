from django.db import models
from django.urls import reverse
from django.utils import timezone
from phone_field import PhoneField
from django.utils.text import slugify
from django.contrib.auth.models import User


class Blog(models.Model):

	LOCATION_CHOICES = ( 
		   ('BK', 'BROOKLYN'), 
		   ('QS', 'QUEENS'), 
		   ('MT', 'MANHATTAN'), 
		   ('SI', 'STATE ISLAND'), 
		) 
	RENTAL_CHOICES=(
		('qz', 'Looking for Rent'),
		('cz', 'For Rent'),
		)

	title = models.CharField(max_length=100)
	poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	slug = models.SlugField(null=True, default='')
	# slug = models.SlugField(max_length=250, null=True, blank=True)
	description = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	date_updated = models.DateTimeField(default=timezone.now)
	#contact = PhoneField(blank=True, help_text='Contact phone number')
	contact = models.CharField(max_length=25)
	status = models.CharField(max_length = 10, choices=RENTAL_CHOICES, default='cz')
	location = models.CharField(max_length = 10, choices = LOCATION_CHOICES, default ='BK') 
	# image = models.FilePathField(path='/img')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		kwargs={
		'pk': self.id,
		'slug': self.slug
		}
		return reverse('blog-detail', kwargs=kwargs)
		# return reverse('post-detail', kwargs={'pk': self.pk})
	def save(self, *args, **kwargs):
		value = self.title
		self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)

# class videos(model.Model):
# 	poster = models.ForeignKey(User, on_delete=models.CASCADE)
# 	title = models.CharField(max_length=100)
# 	description = models.TextField()
# 	link = models.CharField(max_length=20)
# 	active = models.BooleanField(default=False)
# 	postdate = models.DateTimeFiled()