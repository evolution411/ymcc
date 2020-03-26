from django.urls import path
from .views import VideoListView, VideoDeleteView, VideoCreateView, VideoUpdateView, UserVideosView, VideoDetailView #video_detail_view
from . import views

urlpatterns = [
	path('videolist/', VideoListView.as_view(), name='video-list'),
	path('video/<int:pk>/<str:slug>/',VideoDetailView.as_view() , name='video-detail'),
	path('video/<int:pk>/update', VideoUpdateView.as_view(), name='video-update'),
	path('video/<int:pk>/delete', VideoDeleteView.as_view(), name='video-delete'),
	path('video/new/', VideoCreateView.as_view(), name='video-create'),
	path('video/<str:username>', UserVideosView.as_view(), name='user-videos'),
	# path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]