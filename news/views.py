import requests
requests.packages.urllib3.disable_warnings()
import urllib.request as ur
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from .models import Headline

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
	return redirect("/")

def news_list(request):
	scrape(request)
	headlines = Headline.objects.all().order_by('-newsdate')[::-1]
	context = {
		'object_list': headlines,
	}
	return render(request, "news/news.html", context)