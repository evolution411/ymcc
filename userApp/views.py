from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from videos.models import Video

# Create your views here.
class SignUpView(View):
	form_class = SignUpForm
	template_name = 'user/register.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()

			current_site = get_current_site(request)
			subject = "Activate your account"
			message = render_to_string('user/account_activation_email.html',
				{
				'user':user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
				}
				)
			user.email_user(subject,message)
			# messages.success(request, ('Please Confirm your email to complete registration.'))
			return redirect('activation_message')
			# return HttpResponse('Please Confirm your email to complete registration.')
		return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

	def get(self, request, uidb64, token, *args, **kwargs):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except(TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.profile.email_confirmed = True
			user.save()
			# login(request, user)
			messages.success(request, ('Your account has been activated, please login'))
			return redirect('success_registered')
		else:
			messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
			return redirect('/')

def success_activate(request, **kwargs):
	return render(request, 'user/success_activate.html')

	# template_name = 'user/success_activate.html'
def activate_message(request, **kwargs):
	return render(request, 'user/activation_message.html')

@login_required
def profile(request):
	
	if request.method=="POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
	'u_form': u_form,
	'p_form': p_form,
	# 'videos': myvideos
	}
	return render(request, 'user/profile.html', context)