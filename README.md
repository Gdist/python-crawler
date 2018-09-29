# Python-crawler
只是一些練手用的小玩具

## 簡介
* maxjav&javpop

學爬蟲的動機，基本的網址獲取已經達到，搭配JD2使用

* nyaa_GetMagnet

磁力連結爬蟲，搭配AriaNg使用

* JAVHD-DL

非原創，針對不要太容易被識別為爬蟲做了點調整

[修改自eqblog](http://www.hostloc.com/thread-433873-1-1.html)

* JAVAutoSorted

近來最滿意(也最急需)之作，能辨識番號→搜尋封面+標題→建立以標題為名的資料夾→將檔案移進新的資料夾

* Aria2

將爬到的網址匯入Aria2下載，內含feikebt和nyaa的爬蟲

## 使用方法
* maxjav&javpop

將keyword修改為想要搜尋的關鍵字後，直接執行即可

若要更複雜的功能，參考9~20行的說明並更改對應參數(原想設計成互動式介面，但使用上反而造成麻煩XD)

* nyaa_GetMagnet

將keyword修改為想要搜尋的關鍵字，將num修改為終止頁數後(沒寫檢查是不是最後一頁)，即可執行

* JAVHD-DL

### 首先須準備兩樣東西
1. JAVHD的試用會員/正式會員，到信箱複製credentials，並更改cert變數

> 範例：secure.javhd.com/login/?credentials=YXhkMmVnY2dhdHxhbnhma2h3d2Ni&lang=en

> cert即為YXhkMmVnY2dhdHxhbnhma2h3d2Ni

2. Proxy代理池，可自己架或使用該項目內的測試地址，改動get_proxy()下的網址

> [參考proxy_pool](https://github.com/jhao104/proxy_pool)

再來即可開始執行，受限於硬碟空間，所以可以手動續傳

操作方法為更改run()下的flag變數，以及info的串列切割長度

(自動續傳有空會實現，目前想法是將以下載的檔案存成log，並比對紀錄)

## 待完善

* maxjav&javpop

導入cookies並實現自動下載，或使用PyLoad整合AllDebrid下載(待研究)

* nyaa_GetMagnet

暫無

* JAVHD-DL

將下載紀錄存成log(實現)，並調用這個紀錄，透過實現自動續傳(未實現)

修正隨機暫停秒數
