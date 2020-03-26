from django.db import models
from django.utils import timezone

class Headline(models.Model):
	title =  models.CharField(max_length=200)
	image = models.URLField(null=True, blank=True)
	newsdate = models.DateTimeField(default=timezone.now)
	url = models.TextField()

	def __str__(self):
		return self.title