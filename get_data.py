import requests
requests.packages.urllib3.disable_warnings()
import urllib.request as ur
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup


session = requests.Session()
# session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}

hdr= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
#url = "https://sports.theonion.com/"
url = ur.urlopen("http://www.sinovision.net/").read()
nbalink = requests.get('http://nbastreams.xyz/schedule/')
nbadata = nbalink.text
nbasoup = BSoup(nbadata, 'html.parser')
# nbaPage = ur.urlopen(nbasoup)
games = nbasoup.find('div', {'class':'col-md-8'})
# print (games)
nbadict = {}
mainlinks = games.find_all('a')
for link in mainlinks:
	matchLink = link['href']
	matchTitle = link.find('h4').text
	nbadict[matchTitle]=matchLink
	# nbadict.update(matchLink='matchTitle')
	print (matchTitle)
# for game in games:
# 	mainlinks = game.find_all(href=True)
# 	# mainlinks = game.find('a').get_text()
# 	# nbatitles = game.find('media-heading')
# 	# matchLink = mainlinks['href']
# 	# matchTitle = nbatitles.find('h4').get_text()
# 	# print(matchTitle)
# 	print(matchLink)







#url = "https://www.worldjournal.com/topic/%e7%b4%90%e7%b4%84%e6%96%b0%e8%81%9e%e7%b8%bd%e8%a6%bd/"
# content = session.get(url, verify=False).content
soup = BSoup(url.decode("utf-8"), 'lxml')
# soup = BSoup(content, "html.parser")
# headline = soup.find_all('h2')[0:20]
# print (headline)
# News = soup.find_all('div', {"class":"curation-module__item"})
main_news = soup.find_all('div',{'class': 'centersection-r'})
# News = soup.find_all('li', {"class":"rolltitle"})
for article in main_news:
	headline = article.find_all('li', {'class':'rolltitle'})
	for news in headline:
		title = news.find('a').get_text()
		main = news.find_all('a')[0]
		link = main['href']
		print (title)
		print (link)
	# image_src =  str(main.find('img')['srcset']).split(" ")[-4]
	# title = main['title']
	# new_headline = Headline()
	# new_headline.title = main
	# new_headline.url = link
	# # new_headline.image = image_src
	# print (new_headline)
	# print(new_headline.url)
