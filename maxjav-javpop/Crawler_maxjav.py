import requests
from bs4 import BeautifulSoup
import cfscrape #Anti-CDN
scraper = cfscrape.create_scraper() #Anti-CDN

###進入每篇文章抓網址
DL = []
def get_dl_link(link):
	global DL
	dl = []
	response = scraper.get(link)
	soup = BeautifulSoup(response.text, 'lxml')
	articles = soup.find('div','entry').find_all('p')

	title = articles[0].getText().split("\n")[0] #Title
	#print(title)
	dl += [title]
	for article in articles :
		if type(article) != type(None):
			if type(article.find('img')) != type(None): #Poster
				poster = article.find('img').get("src") 
				dl += [poster]
			for i in article.find_all('a'): #DL Link
				dl += [i.get('href')]
	meta1 = soup.find('div','entry').find('div','sh-content pressrelease-content sh-hide')
	if type(meta1) != type(None): #Screenshot
		for i in meta1.find_all('a'): 
			dl += [i.get('href')]
	for i in dl :
		print(i)
	print()
	DL.append(dl)

###Main
page = 1
keyword = "300MAAN"
end = 0

while True:
	url = "http://maxjav.com/page/" + str(page) + "/?s=" + keyword
	response = scraper.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	#檢查是不是沒有下一頁
	check = soup.find_all('h2')
	for i in check :
		if type(i) != type(None) and i.getText() == "Error 404 - Not Found":
			end = True
	if end :
		break

	articles = soup.find_all('p')
	for article in articles : #
		meta = article.find('a')
		if type(meta) != type(None) and keyword in str(article):
			#每篇文章的網址
			link = meta.get("href")
			get_dl_link(link)
	page += 1 #去下一頁

###Export
filename = "maxjav_" + keyword +".csv"
with open(filename , "w", encoding = "utf8") as data:
	for i in DL :
		for j in i :
			data.write("%s," % (j))
		data.write("\n")	