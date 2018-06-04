import requests
from bs4 import BeautifulSoup

###進入每篇文章抓網址
DL = []
def get_dl_link(link):
	global DL
	dl = []
	response = requests.get(link)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')
	articles = soup.find_all('div','box-b')
	for article in articles :
		meta1 = article.find("h1")
		if type(meta1) != type(None):
			title = meta1.getText().replace("[","").replace("]","").replace(" / "," ")
			print(title)
		meta2 = article.find('div','entry')
		if type(meta2) != type(None):
			poster = meta2.find('p','poster').find('img').get("src")
			dl += [title] + [poster]
			for i in meta2.find_all('p','screenshot'): #Screenshot
				dl += [i.find('img').get("src")]
			for i in meta2.find_all('a'): #下載網址
				if "wushare" in str(i) and ("rar" or "zip" ) not in str(i):
					dl += [i.get('href')]
	DL.append(dl)

###Main
page = 1
keyword = "SSNI"

while True:
	url = "http://javpop.com/page/" + str(page) +"?s=" + keyword
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')
	#檢查是不是沒有下一頁
	check = soup.find('h2').getText()
	if check == "Error 404 - Not Found":
		break

	articles = soup.find_all('li')
	for article in articles : #
		meta = article.find('a')
		if type(meta) != type(None) and keyword in str(meta):
			#每篇文章的網址
			link = meta.get("href")
			get_dl_link(link)
	page += 1 #去下一頁

###Export
filename = "javpop_" + keyword +".csv"
with open(filename , "w", encoding = "utf8") as data:
	for i in DL :
		for j in i :
			data.write("%s," % (j))
		data.write("\n")	