from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='avatar', default='avatar/default.jpeg')


    def __str__(self):
    	return f'{self.user.username} Profile'

    def save(self):
    	super().save()
    	img = Image.open(self.image.path)

    	if img.height > 300 or img.width > 300:
    		output_size = (300,300)
    		img.thumbnail(output_size)
    		img.save(self.image.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()
# @receiver(post_save, sender=User)u
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#         instance.profile.save()


