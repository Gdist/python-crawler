# coding: utf-8
import requests , json , time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import aria2 as aria2

num = 3 #爬行頁數
seednum = 3 #最低需求上傳種子數
begin = "2018/08/15 00" #早於此日期的將不會被下載
begin_date = datetime.strptime(begin, '%Y/%m/%d %H')

def get_magnet(url):
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')
	if not soup.find("tbody"):
		print("#Stop  : Page %s Not Found" % (str(page)))
		return
	articles = soup.find("tbody").find_all("tr",)

	for i in articles:
		td = i.find_all("td")
		date = td[0].find("span").getText()
		date2 = datetime.strptime(date, '%Y/%m/%d %H:%M')
		title = td[2].find_all("a")[-1].getText().replace("	","").replace("\n","")
		link = td[2].find_all("a")[-1].get("href")
		viewid = link[:link.find('_')].replace("/topics/view/","")
		magnet = td[3].find("a").get("href")
		size = td[4].getText()
		seeders = int(td[5].getText()) if td[5].getText() != "-" else 0
			
		logNprint("Find ID : "+viewid)
		logNprint("Title   : "+title)
		logNprint("Seeders : "+str(seeders))
		logNprint("Size    : "+size)

		if viewid in CheckList:
			logNprint("*Error  : "+viewid+" has been added to Aria2")
			continue
		elif seeders < seednum :
			logNprint("*Error  : "+viewid+" has too few seeders (<"+str(seednum)+")")
			continue
		elif (begin_date - date2 > timedelta(seconds= 0) ):
			logNprint("*Error  : "+viewid+" Time is too far")
			continue

		#添加到Aria2
		aria2.AddURL([magnet])
		checklist(viewid)
		logNprint("-----Success-----")
		time.sleep(0.5)


def logNprint(text):
	print(text)
	with open("Aria2_dmhy.log","a", encoding = 'utf-8-sig') as data:
		data.write(str(text)+"\n")

def checklist(text):
	with open("Check_dmhy.log","a", encoding = 'utf-8-sig') as data:
		data.write(str(text)+"\n")

try:
	with open("Check_dmhy.log" , "r", encoding = 'utf-8-sig') as clog: #ID紀錄
		CheckList = [l.strip() for l in clog ]
except:
	CheckList = []

with open("Key_dmhy.txt" , "r", encoding = 'utf-8-sig') as keydata: #關鍵字紀錄
	KeyList = [l.strip() for l in keydata ]

localtime = time.asctime( time.localtime(time.time()))
logNprint("\nBeginTime: "+localtime)

for i in KeyList:
	keyword = i
	logNprint("\nKeyWord : "+keyword+"\n")
	for j in range(num):
		page = j+1
		url = "https://share.dmhy.org/topics/list/page/"+ str(page) +"?keyword="+keyword
		get_magnet(url)
