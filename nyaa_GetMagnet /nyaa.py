import requests
from bs4 import BeautifulSoup
def get_magnet(url):
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')
	articles = soup.find_all("tr",)
	articles = articles[1:]

	for i in articles:
		td = i.find_all("td")
		title = td[1].find("a").getText()
		print(title)
		x = i.find("td","text-center").find_all("a")
		magnet = x[0].get("href") if "magnet" in x[0].get("href") else x[1].get("href")
		#print(magnet)
		List.append([title,magnet])

keyword = "key" #修改關鍵字
page = 1
num = 10 #修改終止頁數
url = "https://sukebei.nyaa.si/?f=0&c=2_2&q="+ keyword + "&p=" + str(page)
List = []

for i in range(num):
	page = i+1
	url = "https://sukebei.nyaa.si/?f=0&c=2_2&q="+ keyword + "&p=" + str(page)
	get_magnet(url)

filename = "nyaa_" + keyword + ".csv"

with open(filename, "w", encoding = "utf8") as data1:
	for i in List:
		for j in i:
			data1.write("%s,"% (j))
		data1.write("\n")
