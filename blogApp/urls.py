from django.urls import path
from .views import (BlogListView, BlogDetailView, BlogDeleteView, MyBlogsView,
BlogCreateView, BlogUpdateView, UserBlogsView, 
HomeView, ToRentView, SeekingRentView, nba_view)
from blogApp import views

urlpatterns = [
	path('', HomeView.as_view(), name='blog-home'),
	path('torent/', ToRentView.as_view(), name='to-rent'),
	path('lookrent/', SeekingRentView.as_view(), name='seek-rent'),
	path('nbalivestream/', nba_view, name='nba-game'),
	path('blog/new/', BlogCreateView.as_view(), name='blog-create'),
	path('bloglist/', BlogListView.as_view(), name='blog-list'),
	path('blog/<int:pk>/<str:slug>/', BlogDetailView.as_view(), name='blog-detail'),
	path('myblogs/<str:username>/', MyBlogsView.as_view(), name='user-blogs')
]