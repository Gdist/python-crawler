# coding: utf-8
import requests , json , time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import aria2

num = 3 #爬行頁數
seednum = 20 #最低需求上傳種子數
sortbyseeders = True #是否依照種子數排序
begin = "2018/08/15 00" #早於此日期的將不會被下載
begin_date = datetime.strptime(begin, '%Y/%m/%d %H')

def get_magnet(url):
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')

	articles = soup.find_all("tr",)
	articles = articles[1:]

	for i in articles:
		td = i.find_all("td")
		for td1 in td[1].find_all("a"):
			if "#comments" not in td1.get("href"):
				viewid = td1.get("href").replace("/view/","")
				title = td1.getText()
				break
		date = (td[4].getText())
		date2 = datetime.strptime(date, '%Y-%m-%d %H:%M')
		seeders = int(td[5].getText())
		if "#comments" in viewid:
			continue
			
		logNprint("Find ID : "+viewid)
		logNprint("Title   : "+title)
		logNprint("Seeders : "+str(seeders))

		if viewid in CheckList:
			logNprint("*Error  : "+viewid+" has been added to Aria2")
			continue
		elif seeders < seednum :
			logNprint("*Error  : "+viewid+" has too few seeders (<"+str(seednum)+")")
			if sortbyseeders==True:
				break
			else:
				continue
		elif (begin_date - date2 > timedelta(seconds= 0) ):
			logNprint("*Error  : "+viewid+" Time is too far")
			continue

		x = td[2].find_all("a")
		magnet = x[0].get("href") if "magnet" in x[0].get("href") else x[1].get("href")
		#添加到Aria2
		aria2.AddURL([magnet])
		checklist(viewid)
		logNprint("-----Success-----")
		time.sleep(0.5)


def logNprint(text):
	print(text)
	with open("Aria2_nyaa.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")

def checklist(text):
	with open("Check_nyaa.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")
#Main
try:
	with open("Check_nyaa.log" , "r") as clog: #ID紀錄
		CheckList1 = [l.strip() for l in clog ]
except:
	CheckList1 = []
try:
	with open("Check_nyaa2.log" , "r") as clog: #ID紀錄
		CheckList2 = [l.strip() for l in clog ]
except:
	CheckList2 = []

CheckList = CheckList1 + CheckList2

with open("Key_nyaa.txt" , "r", encoding = 'utf8') as keydata: #關鍵字紀錄
	KeyList = [l.strip() for l in keydata ]

localtime = time.asctime( time.localtime(time.time()))
logNprint("\nBeginTime: "+localtime)

for i in KeyList:
	keyword = i
	logNprint("\nKeyWord : "+keyword+"\n")
	for j in range(num):
		page = j+1
		url1 = "https://sukebei.nyaa.si/?f=0&c=0_0&q="+ keyword + "&p=" + str(page)
		url2 = "https://sukebei.nyaa.si/?f=0&c=0_0&q="+ keyword + "&s=seeders&o=desc" + "&p=" + str(page)
		url = ( url2 if sortbyseeders == True else url1 )
		get_magnet(url)
