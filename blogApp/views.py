from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
requests.packages.urllib3.disable_warnings()
import urllib.request as ur
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .forms import BlogPostForm
from .models import Blog
from videos.models import Video
from news.models import Headline
from .filters import BlogFilter

def nba_view(request):
	url = ur.urlopen("http://www.sinovision.net/").read()
	nbalink = requests.get('http://nbastreams.xyz/schedule/')
	nbadata = nbalink.text
	nbasoup = BSoup(nbadata, 'html.parser')
	games = nbasoup.find('div', {'class':'col-md-8'})
	nbadict = {}
	mainlinks = games.find_all('a')
	for link in mainlinks:
		matchLink = link['href']
		matchTitle = link.find('h4').text
		nbadict[matchTitle]=matchLink

	return render(request,'blogApp/nba_live.html', {'nbadict': nbadict})

class HomeView(ListView):
	template_name = 'blogApp/home.html'
	context_object_name = 'home_list'
	queryset = Blog.objects.all().order_by('-id')[:10]

	def scrape(request):
		session = requests.Session()
		session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
		url = ur.urlopen("http://www.sinovision.net/").read()
		soup = BSoup(url.decode("utf-8"), 'lxml')
		main_news = soup.find('div',{'class': 'centersection-r'})
		
		for news in main_news.find_all('li',{'class': 'rolltitle'}):
			
			title = news.find('a').get_text()
			main = news.find_all('a')[0]
			link = main['href']

			if Headline.objects.filter(url=link):
				continue
			elif link == '':
				continue
			new_headline=Headline()
			new_headline.title = title
			new_headline.url = link
			new_headline.save()

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['blogs'] = self.queryset
		context['videos'] = Video.objects.all().order_by('-id')[:4]
		context['news'] = Headline.objects.all().order_by('-id')[:12]
		# context['nbagames']=nbadict
		return context

class MyBlogsView(LoginRequiredMixin, ListView):
	model = Blog
	template_name = 'blogApp/user_blogs.html'
	context_object_name = 'blogs'
	ordering = ['-date_posted']

	def get_queryset(self,**kwargs):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Blog.objects.filter(poster=user)


class ToRentView(ListView):
	model = Blog
	template_name = 'blogApp/to_rent.html'
	context_object_name = 'rentals'

	def get_queryset(self):
		return Blog.objects.filter(status='cz')

class SeekingRentView(ListView):
	model = Blog
	template_name = 'blogApp/seek_rent.html'
	context_object_name = 'rentals'
	
	def get_queryset(self):
		return Blog.objects.filter(status='qz')


class BlogListView(ListView):
	model = Blog
	template_name = 'blogApp/blog_list.html'
	context_object_name = 'blogs'
	ordering = ['-date_posted']

	def get_context_data(self, **kwarg):
		context = super().get_context_data(**kwarg)
		context['filter'] = BlogFilter(self.request.GET, queryset=self.get_queryset())
		return context

class BlogDetailView(LoginRequiredMixin, DetailView):
	model = Blog
	query_pk_and_slug = True
	
class BlogCreateView(CreateView):
	model = Blog
	form_class = BlogPostForm
	# model = Blog
	template_name = 'blogApp/blog_form.html'

	def form_valid(self, form):
		form.instance.poster = self.request.user
		return super().form_valid(form)
	# fields = ['title','status','description', 'contact']
	
	# def form_valid(self, form):
	# 	form.instance.poster = self.request.user
	# 	return super().form_valid(form)
	# def get(self, request, *args, **kwargs):
	# 	form = self.form_class()
	# 	return render(request, self.template_name, {'form': form})

	# def post(self, request, *args, **kwargs):
	# 	form = self.form_class(request.POST)
	# 	if form.is_valid():
	# 		form.instance.poster = self.request.user
	# 		form.save()
	# 		kwargs={
	# 			'pk': form.id,
	# 			'slug': form.slug
	# 			}
	# 	return HttpResponseRedirect(reverse('blog-detail', kwargs=kwargs))
			
		#return render(request, 'self.template_name', {'form': form})

class UserBlogsView(LoginRequiredMixin,ListView):
	model = Blog
	template_name = "Blog/user_blog.html"
	context_object_name = 'blogs'
	ordering = ['-date_posted']

	def get_queryset(self,**kwargs):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Blog.objects.filter(poster=user)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Blog
	fields = ['title','description']

	def test_func(self):
		blog = self.get_object()
		if self.request.user == blog.poster:
			return True
		return False

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Blog
	success_url = 'bloglist/'
	def test_func(self):
		blog = self.get_object()
		if self.request.user == blog.poster:
			return True
		return False

