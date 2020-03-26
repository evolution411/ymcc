from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import Profile


class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='Required')
	# image = forms.ImageField()
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
	
	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
			raise ValidationError("Username already exist")
		return username

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email=email)
		if r.count():
			raise ValidationError("Email already exist")
		return email

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise ValidationError("Password don't match")

		return password2

	def clean_image(self):
		avatar = self.cleaned_data['image']
		try:
			w, h = get_image_dimensions(avatar)
			max_width = max_height = 800
			if w > max_width or h > max_height:
				raise ValidationError("please use a smaller pictures")
			main, sub = avatar.content_type.spli('/')
			if not(main == 'image' and sub in['jpeg','jpg','png']):
				raise ValidationError("Please use a JPEG, JPG or PNG image.")

			if len(avatar) > (800*1024):
				raise ValidationError("Image file size may not exceed 8mb.")

		except AttributeError:
			pass

		return avatar

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

# class CustomUserCreationForm(forms.Form):
# 	username = forms.CharField(label='Username', min_length=4, max_length=50)
# 	email = forms.EmailField(label='Email')
# 	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
# 	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

# 	def clean_username(self):
# 		username = self.cleaned_data['username'].lower()
# 		r = User.objects.filter(username=username)
# 		if r.count():
# 			raise ValidationError("Username already exist")
# 		return username

# 	def clean_email(self):
# 		email = self.cleaned_data['email'].lower()
# 		r = User.objects.filter(email=email)
# 		if r.count():
# 			raise ValidationError("Email already exist")
# 		return email

# 	def clean_password2(self):
# 		password1 = self.cleaned_data.get('password1')
# 		password2 = self.cleaned_data.get('password2')

# 		if password1 and password2 and password1 != password2:
# 			raise ValidationError("Password don't match")

# 		return password2

# 	def save(self, commit=True):
# 		user = User.objects.create_user(
# 			self.cleaned_data['username'],
# 			self.cleaned_data['email'],
# 			self.cleaned_data['password1']
# 			)
# 		return user
