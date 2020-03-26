from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, FormView
from .models import Video, VideoComment
from .forms import CommentForm

class VideoListView(ListView):
	model = Video
	template_name = 'videos/video_list.html'
	context_object_name = 'videos'
	ordering = ['-date_posted']

class VideoDetailView(LoginRequiredMixin, DetailView, FormView):
	model = Video
	template_name='videos/video_detail.html'
	query_pk_and_slug = True
	form_class = CommentForm

	new_comment = None

	# def get_success_url(self):
	# 	return reverse('video_detail', kwargs={'pk': kwargs['pk'], 'slug':kwargs['slug']})

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comments'] = VideoComment.objects.filter(video = self.get_object(), active=True).order_by('-commentDate')

		return context

	def post(self, request, *args, **kwargs):
		video  = get_object_or_404(Video, pk=kwargs['pk'])
		if request.method == 'POST':
			if request.user.is_authenticated:
				poster = request.user
			else:
				poster = "Guest"
			comment_form = CommentForm(data=request.POST)
			if comment_form.is_valid():
				new_comment = comment_form.save(commit=False)
				new_comment.commentPoster = poster
				new_comment.video = video
				new_comment.active = True
				
				new_comment.save()

		return HttpResponseRedirect(request.get_full_path())

class VideoCreateView(LoginRequiredMixin,CreateView):
	model = Video
	fields = ['title','description', 'link']
	
	def form_valid(self, form):
		form.instance.poster = self.request.user
		return super().form_valid(form)

class UserVideosView(LoginRequiredMixin,ListView):
	model = Video
	template_name = "videos/user_videos.html"
	context_object_name = 'videos'
	ordering = ['-date_posted']

	def get_queryset(self,**kwargs):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Video.objects.filter(poster=user)


class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Video
	fields = ['title','description', 'link']

	def test_func(self):
		video = self.get_object()
		if self.request.user == video.poster:
			return True
		return False

class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Video
	success_url = 'videolist/'
	def test_func(self):
		video = self.get_object()
		if self.request.user == video.poster:
			return True
		return False


