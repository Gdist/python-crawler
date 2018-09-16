import requests , json , time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def get_magnet(url):
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')

	articles = soup.find_all("tr",)
	articles = articles[1:]

	for i in articles:
		td = i.find_all("td")
		viewid = td[1].find("a").get("href").replace("/view/","")
		title = td[1].find("a").getText()
		date = (td[4].getText())
		date2 = datetime.strptime(date, '%Y-%m-%d %H:%M')
		seeders = int(td[5].getText())
		if "#comments" in viewid:
			continue
		logNprint("Find ID : "+viewid)
		logNprint("Title   : "+title)

		if viewid in ChcekList:
			logNprint("*Error  : "+viewid+" has been added to OffCloud")
			continue
		elif seeders < seednum :
			logNprint("*Error  : "+viewid+" has too few seeders (<"+str(seednum)+")")
			continue
		'''elif (begin_date - date2 > timedelta(seconds= 0) ) :
			logNprint("*Error  : "+viewid+" Time is too far")
			continue'''

		x = td[2].find_all("a")
		magnet = x[0].get("href") if "magnet" in x[0].get("href") else x[1].get("href")
		#print(magnet)
		api(magnet)
		if "success" in apijson.keys():
			checklist(viewid)
			logNprint("Success : " +viewid)


def	api(apilink):
	global apijson
	apiurl = "https://offcloud.com/api/remote/download?apikey=" + apikey + "&url=" + apilink
	apires = requests.get(apiurl) #調用API
	apijson = json.loads(apires.text) #利用json.loads()解碼JSON

def logNprint(text):
	print(text)
	with open("offcloud.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")

def checklist(text):
	with open("checklist.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")

num = 1 #爬行頁數
seednum = 5 #最低需求上傳種子數
apikey = "" #填寫OffCloud API
'''begin = "2018/09/16 00" #早於此日期的將不會被下載
begin_date = datetime.strptime(begin, '%Y/%m/%d %H')'''

with open("checklist.log" , "r") as clog: #ID紀錄
	ChcekList = [l.strip() for l in clog ]

with open("keyword.txt" , "r") as keydata: #ID紀錄
	KeyList = [l.strip() for l in keydata ]

localtime = time.asctime( time.localtime(time.time()))
logNprint("\nBeginTime: "+localtime)

for i in KeyList:
	keyword = i
	logNprint("\nKeyWord : "+keyword+"\n")
	for j in range(num):
		page = j+1
		url = "https://sukebei.nyaa.si/?f=0&c=0_0&q="+ keyword + "&p=" + str(page)
		#url = "https://sukebei.nyaa.si/?f=0&c=0_0&q="+ keyword + "&s=seeders&o=desc" + "&p=" + str(page)
		get_magnet(url)
