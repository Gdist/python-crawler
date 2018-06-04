import requests,re,threading,os,time,random
cert='YXhkMmVnY2dhdHxhbnhma2h3d2Ni'
quality=1080
time_sleep=random.randint(10,20)
flag = 0
def logNprint(text):
    print(text)
    with open("javhd.log","a") as data:
        data.write(str(text)+"\n")
def change_unit(size):
    global unit,size_List
    n = 0
    temp = size
    size_List = ["B","KB","MB","GB","TB"]
    while(temp>=1024):
        n +=1
        temp = temp /1024
    return str(round(temp,2))+size_List[n]

def get_proxy():
    return requests.get("https://ip.gd4.us/get/").text
class spider:
    def __init__(self,sp):
        self.sp=sp
    def page(self,flag):
        page_url='https://javhd.com/en/japanese-porn-videos/justadded/all/'+str(flag)
        return page_url
    def req(self,proxies):
        req=requests.Session()
        response=req.get('https://secure.javhd.com/login/index/direct?credentials='+cert+'&back=javhd.com&lang=en', allow_redirects=False,proxies=proxies)
        req.get(response.headers['location'],proxies=proxies)
        return req
    def find_info(self,page_url,proxies):
        req=requests.get(page_url,proxies=proxies)
        info=re.findall(r'clickitem="(.*?)" class="tackclick thumb-link"><img src=".*?" alt="(.*?)"/>',str(req.text),re.M)
        return info
    def find_mp4(self,id,reqget,proxies):
        url='https://javhd.com/zh/player/'+str(id)+'?type=vjs'
        req=reqget.get(url,proxies=proxies)
        return req.json()
    def sources_mp4(self,dict,reqget,proxies):
        for i in dict['sources']:
            if int(i['res'])==self.sp:
                w=reqget.get(i['src'],allow_redirects=False,proxies=proxies)
                return w.headers['location']
def Handler(start, end, url, filename):
    headers = {'Range': 'unit=%d-%d' % (start, end)}
    with requests.get(url, headers=headers,stream=True) as r:
        with open(filename+'.mp4', "r+b") as fp:
            fp.seek(start)
            var = fp.tell()
            fp.write(r.content)
def download(url,tittle, num_thread = 1):
    r = requests.head(url)
    try:
        file_name = tittle
        file_size = int(r.headers['content-length'])
    except:
        logNprint("Check URL")
        return
    logNprint('Start : %s' % file_name)
    time1 = time.time() #Time
    fp = open(file_name+'.mp4', "wb")
    fp.truncate(file_size)
    fp.close()
    part = file_size // num_thread
    for i in range(num_thread):
        start = part * i
        if i == num_thread - 1:
            end = file_size
        else:
            end = start + part
        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
        t.setDaemon(True)
        t.start()
 
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    logNprint('Finish : %s' % file_name)
    time2 = time.time()
    size = os.path.getsize(file_name+'.mp4')
    speed = size/(time2-time1)
    logNprint("Speed : "+change_unit(speed)+"/s")
    #logNprint("This is No."+ str(Num) +"of Page"+str(flag))
    
def run():
    proxy = get_proxy()
    print('Proxy：'+proxy)
    proxies={"http": "http://{}".format(proxy)}
    flag=5
    s=spider(quality)
    while True:
        try:
            page=s.page(flag)
            info=s.find_info(page,proxies)
            if flag ==5:
                info = info[60:]
            for i in info:
                reqget=s.req(proxies)
                mp4_dict=s.find_mp4(i[0],reqget,proxies)
                tittle=i[1].strip('\xa0')
                #print(tittle)
                try:
                    if os.path.exists(str(tittle)+'.mp4')==False:
                        sources_url=s.sources_mp4(mp4_dict,reqget,proxies)
                        print(sources_url)
                        if 'cdn_cv_memberid' in sources_url:
                            download(sources_url,tittle)
                            time.sleep(time_sleep)
                        else:
                            reqget=s.req(proxies)
                            download(sources_url,tittle)
                            time.sleep(time_sleep)
                    else:
                        print("Exist : " + str(tittle))
                        time.sleep(time_sleep)
                        continue
                except:
                    proxy = get_proxy()
                    print('Proxy：' +proxy)
                    proxies={"http": "http://{}".format(proxy)}
                    continue
            logNprint('***Page : '+str(flag)+' Finish***\n' )
            flag+=1
            time.sleep(time_sleep)
        except:continue
if __name__=='__main__':
    run()
