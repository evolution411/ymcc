from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from embed_video.fields import EmbedVideoField

# @python_2_unicode_compatible
class Video(models.Model):
	
	title = models.CharField(max_length=100)
	description = models.TextField()
	slug = models.SlugField(null=True, default='')
	link = EmbedVideoField()
	poster = models.ForeignKey(User, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		kwargs={
		'pk': self.id,
		'slug': self.slug
		}
		return reverse('video-detail', kwargs=kwargs)

	def save(self, *args, **kwargs):
		value = self.title
		self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)

class VideoComment(models.Model):
	video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_comments')
	commentPoster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_comment_posters')
	commentText = models.TextField()
	commentDate = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)

	class Meta:
		ordering = ['commentDate']

	def __str__(self):
		return 'Comment {} by {}'.format(self.commentText, self.commentPoster)

