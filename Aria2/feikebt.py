import requests , json , time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import aria2

#變數定義區
keyword = "新作 連發"
start = 3
num = 1
begin = "2018/09/16" #早於此日期的將不會被下載
begin_date = datetime.strptime(begin, '%Y/%m/%d')

#Define Function
def get_magnet(url):
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')

	articles = soup.find_all("div", {"class": "ffbox"})
	articles = articles[1:]

	for i in articles:
		span = i.find_all("span")
		title = i.find("h3").getText()
		ID = i.find("a").get("href")[27:-5]

		for j in span:
			if j.getText()[:3] == "磁力链":
				magnet = j.find("a").get("href")
			elif j.getText()[:4] == "文件大小":
				filesize = j.getText()[5:]
			elif j.getText()[:4] == "收录时间":
				date = j.getText()[5:]
				date2 = datetime.strptime(date, '%Y-%m-%d')

		logNprint("Find ID : "+ID)
		logNprint("Title   : "+title)
		logNprint("Date    : "+date)
		logNprint("Size    : "+filesize)

		if ID in ChcekList:
			logNprint("**Error : This torrent has been added to Aria2")
			continue
		elif (begin_date - date2 > timedelta(seconds= 0) ):
			logNprint("**Error : Date of the torrent is too far")
			continue
		#添加到Aria2
		aria2.AddURL([magnet])
		checklist(ID)
		logNprint("-----Success-----")
		
		
def logNprint(text):
	print(text)
	with open("Aria2_fkbt.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")

def checklist(text):
	with open("Check_fkbt.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")

#Main
try:
	with open("Check_fkbt.log" , "r") as clog: #ID紀錄
		ChcekList = [l.strip() for l in clog ]
except:
	ChcekList = []

for i in range(num):
	page = start+i
	url = "http://feikebt.com/s/"+ keyword + "/"+str(page)+"/1/0.html"
	get_magnet(url)