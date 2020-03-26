from django.urls import path
from news.views import scrape, news_list
from . import views

urlpatterns = [
	path('scrape/', scrape, name="scrape"),
	path('news/', news_list, name="news-home")
	# path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]