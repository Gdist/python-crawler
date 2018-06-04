import requests
from bs4 import BeautifulSoup
import cfscrape #Anti-CDN
scraper = cfscrape.create_scraper() #Anti-CDN
Dic = {}
result1 , result2 , ag_maxjav = 0 , 0 , 0
###Set Up
'''
keyword = input("請輸入關鍵字: ")
page_check = input("是否指定搜尋範圍(頁碼)? (Y/N): ")
if page_check == "Y":
	begin_page = int(input("請輸入起始頁碼(留空默認從頭開始): ")) or 1
	end_page = int(input("請輸入結束頁碼(留空默認搜尋到最後): ")) or 0
else:
	begin_page,end_page = 1,0
site = input("搜尋哪個網站? (1=JAVPOP/2=MAXJAV/3=BOTH): ") or "1"
site = site if site.lower() in ["1","javpop","2","maxjav","3","both"] else "1"

print_check = input("是否在執行時印出執行進度? (Y/N): ") or "N"
export_check = input("匯出格式? (1=CSV/2=TXT): ") or "1"
'''
keyword = "words" #修改關鍵字
page_check = "N"
if page_check == "Y":
	begin_page = 1
	end_page = 1
else:
	begin_page,end_page = 1,0
site = "1"
site = site if site.lower() in ["1","javpop","2","maxjav","3","both"] else "1"
print_check = "Y"
export_check = "1"

###Define
##Get DL Links
def getdl_javpop(link):
	dl = [] #為了只印出當次結果
	
	response = requests.get(link)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')
	articles = soup.find_all('div','box-b')
	for article in articles :
		meta1 = article.find("h1")
		if type(meta1) != type(None):
			title = meta1.getText().replace("[","").replace("]","").replace(" / "," ")
			Dic[title] = Dic[title] if title in list(Dic.keys()) else []
		meta2 = article.find('div','entry')
		if type(meta2) != type(None):
			poster = meta2.find('p','poster').find('img').get("src")
			dl += [poster]
			for i in meta2.find_all('p','screenshot'): #Screenshot
				dl += [i.find('img').get("src")]
			for i in meta2.find_all('a'): #下載網址
				if "wushare" in str(i) and ("rar" or "zip" ) not in str(i):
					dl += [i.get('href')]
	Dic[title] += dl #為了只印出當次結果
	if print_check == "Y" : #Print Process Check
		print(title)
		for i in dl:
			print(i)
		print()

def getdl_maxjav(link):
	'''global ag_maxjav''' #Anti-CDN
	dl = [] #為了只印出當次結果

	response = scraper.get(link)
	soup = BeautifulSoup(response.text, 'lxml')
	articles = soup.find('div','entry').find_all('p')

	title = articles[0].getText().split("\n")[0] #Title
	Dic[title] = Dic[title] if title in list(Dic.keys()) else []
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
	'''ag_maxjav = 1 if dl != [] else ag_maxjav'''#Anti-CDN
	Dic[title] += dl #為了只印出當次結果

	if print_check == "Y" : #Print Process Check
		print(title)
		for i in dl:
			print(i)
		print()

## Get Page Links
def get_javpop():
	global result1 , end_page

	page = begin_page
	while True:
		url = "http://javpop.com/page/" + str(page) +"?s=" + keyword
		response = requests.get(url)
		response.encoding = 'UTF-8' 
		soup = BeautifulSoup(response.text, 'lxml')
		

		articles = soup.find_all('li')
		for article in articles : #
			meta = article.find('a')
			if type(meta) != type(None) and keyword in str(meta):
				#每篇文章的網址
				link = meta.get("href")
				getdl_javpop(link)

		##Shut up Check
		check = soup.find('h2').getText()
		if check == "No posts found. Try a different search?" : # Search Not Found 
			result1 = 404
			print("無法在 javpop 搜尋到結果，請確認關鍵字是否正確\n ")
			break
		elif check == "Error 404 - Not Found" or page == end_page :
			end_page = end_page if page == end_page else 0
			break
		page += 1 #去下一頁

def get_maxjav():
	global result2 , end_page

	page = begin_page
	end = 0
	while True:
		url = "http://maxjav.com/page/" + str(page) + "/?s=" + keyword
		response = scraper.get(url)
		soup = BeautifulSoup(response.text, 'lxml')
		articles = soup.find_all('p')
		for article in articles : #
			meta = article.find('a')
			if type(meta) != type(None) and keyword in str(article):
				#每篇文章的網址
				link = meta.get("href")
				getdl_maxjav(link)
		##Shut up Check
		check = soup.find_all('h2')
		for i in check :
			if type(i) != type(None) and i.getText() == "Error 404 - Not Found":
				end = True
				end_page = 0
		if end and page == 1 :
			result2 = 404
			print("無法在 maxjav 搜尋到結果，請確認關鍵字是否正確\n ")
			break
		elif end or page == end_page :
			break		
		page += 1 #去下一頁

###Main
if site.lower() not in ["2","maxjav"]:
	print("即將開始搜索 javpop ... \n")
	get_javpop()	
if site.lower() not in ["1","javpop"]:
	print("即將開始搜索 maxjav ... \n")
	get_maxjav()


	'''if ag_maxjav == 0: #Anti-CDN
		while True : #Anti-CDN ,try again
			#ag = input("無法搜索 maxjav，是否停止搜索? (Y/N): ")
			print("無法搜索 maxjav，是否停止搜索? (Y/N): ")
			print(ag_maxjav)
			ag = "N"
			if ag.lower() != "y" :
				get_maxjav()
				if ag_maxjav != 0:
					break
			else:
				break'''
print("搜尋完成! 共搜尋到%d筆資料\n" % (len(Dic)))
###Export
pre = "both_" #檔名前綴
pre = "javpop_" if site.lower() in ["1","javpop"] else pre
pre = "maxjav_" if site.lower() in ["2","maxjav"] else pre
page_txt = ".p" + str(begin_page) + "-p" + str(end_page) if page_check == "Y" and end_page != 0 else ""

if Dic != {} and export_check.lower() in ["2","txt"]:
	filename = pre + keyword + page_txt + ".txt"
	with open(filename , "w", encoding = "utf8") as data1:
		for i in sorted(Dic.keys()):
			data1.write("%s\n"% (i))
			for j in Dic[i] :
				data1.write("%s\n" % (j))
			data1.write("\n")		
elif Dic != {} :
	filename = pre + keyword + page_txt + ".csv"
	with open(filename , "w", encoding = "utf8") as data2:
		for i in sorted(Dic.keys()):
			data2.write("%s," % (i))
			for j in Dic[i] :
				data2.write("%s," % (j))
			data2.write("\n")
input("匯出完成! 請按Enter離開")

