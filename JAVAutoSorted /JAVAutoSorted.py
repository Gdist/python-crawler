# coding: utf-8
import os , requests , urllib , time 
from bs4 import BeautifulSoup

key = input("請輸入番號名稱 : ")
#key = "ABP"

def logNprint(text):
	os.chdir(mypath)
	print(text)
	with open("error.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")
def log(text):
	with open("error.log","a", encoding = 'utf8') as data:
		data.write(str(text)+"\n")

def GetCode(filename):
	c = key.upper()+"-"
	if c in filename.upper():
		cpos = filename.upper().find(c)
	elif key.upper() in filename.upper():
		c = key.upper()
		cpos = filename.upper().find(c)
		filename = filename.upper().replace(c,c+"-")
		c = c+"-"
	else:
		return None

	for i in range(len(filename[cpos+len(c):])):
		if not filename[cpos+len(c)+i].isdigit():
			code = filename[cpos:cpos+len(c)+i]
			code = code.upper()
			break

	return code

def CoverDL(code):
	global TitleList , dirpath
	url = "https://www.javbus.com/"+code
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')

	if soup.find("h4") == None:
		logNprint("*Error : " + code+ " Unknown Error")
		log(str(soup))
		return
	elif soup.find("h4").getText() == "404 Page Not Found!" :
		text = "*Error : " + code+ " 404 Not Found"
		logNprint(text)
		return
		
	article = soup.find("div", {"class": "container"})
	if article == None:
		logNprint("*Error : " + code+ " Unknown Error")
		return
	title = article.find("h3").getText()
	imglink = article.find("a", {"class": "bigImage"}).get("href")
	TitleList += [title]

	r = requests.get(imglink)
	filename = title + ".jpg"

	if os.path.isdir(mypath+"\\@Sorted\\"+title):
		dirpath = mypath+"\\@Sorted\\"+title
	elif os.path.isdir(mypath+"\\@Sorted\\"+code):
		dirpath = mypath+"\\@Sorted\\"+code
	else:	
		try:
			os.mkdir(mypath+"\\@Sorted\\"+title)
			dirpath = mypath+"\\@Sorted\\"+title
		except:
			os.mkdir(mypath+"\\@Sorted\\"+code)
			dirpath = mypath+"\\@Sorted\\"+code
	os.chdir(dirpath)
	try:
		with open(filename, "wb") as imgdata:
			imgdata.write(r.content)
		print("CoverDL : "+title)
		return True
	except:
		with open(code+".jpg", "wb") as imgdata:
			imgdata.write(r.content)
		print("CoverDL : "+title)
		return True
#讀取先前的清單
try:
	with open("@FileList.txt" , "r") as clog: #ID紀錄
		TitleList = [l.strip() for l in clog ]
except:
	TitleList = []
try:
	with open("@CodeList.txt" , "r") as clog: #ID紀錄
		CodeList = [l.strip() for l in clog ]
except:
	CodeList = []

#讀取檔案清單
mypath = os.getcwd()
removeList = ['JAVCoverDL.py','JAVList.py',"","@CodeList.txt""error.log"]
for root, dirs, files in os.walk(mypath):
	for r in removeList:
		if r in files:
			files.remove(r)
	if mypath+"\\@Sorted" in root:
		continue
	if not os.path.isdir(mypath+"\\@Sorted"):
		os.mkdir(mypath+"\\@Sorted")

	os.chdir(root) #更改到當前目錄
	print("\nRoot : "+root+"\n")
	
	for i in files:
		code = GetCode(i) #從檔名找番號
		if code != None :
			if code not in CodeList:
				x = CoverDL(code)
				if x :
					CodeList += [code]
				else :
					continue
			try:
				print("File : "+i)
				print("Move : "+dirpath)
				os.rename(root+"\\"+i,dirpath+"\\"+i)
			except:
				logNprint("*Error : "+i+"\n *Exist in : "+root)
				pass
		else:
			continue

os.chdir(mypath) #匯出清單
with open("@FileList.txt","w", encoding = 'utf8') as data:
		for i in sorted(TitleList):
			data.write(i+"\n")
with open("@CodeList.txt","w", encoding = 'utf8') as data:
		for i in sorted(CodeList):
			data.write(i+"\n")

input("下載完成，請按Enter離開")