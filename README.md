# Python-crawler
只是一些練手感的小玩具
## 簡介
* maxjav&javpop

學爬蟲的動機，基本的網址獲取已經達到，剩下導入cookies自動下載未完成

* nyaa_GetMagnet

磁力連結爬蟲，搭配AriaNg使用

* JAVHD-DL

非原創，針對不要太容易被識別為爬蟲做了點調整

[修改自eqblog](http://www.hostloc.com/thread-433873-1-1.html)

## 使用方法
* maxjav&javpop

將keyword修改為想要搜尋的關鍵字後，直接執行即可
若要更複雜的功能，參考9~20行的說明並更改對應參數(原想設計成互動式介面，但使用上反而造成麻煩XD)

* nyaa_GetMagnet

沒有其他參數需設置，所以將keyword修改為想要搜尋的關鍵字後，直接執行即可

* JAVHD-DL

### 首先須準備兩樣東西
1. JAVHD的試用會員/正式會員，到信箱複製credentials，並更改cert變數

>>範例：secure.javhd.com/login/?credentials=YXhkMmVnY2dhdHxhbnhma2h3d2Ni&lang=en

>>cert即為YXhkMmVnY2dhdHxhbnhma2h3d2Ni

2. Proxy代理池，可自己架或使用該項目內的測試地址，改動get_proxy()下的網址

>>[參考proxy_pool] （https://github.com/jhao104/proxy_pool）

再來即可開始執行，受限於硬碟空間，所以可以手動續傳，
更改run()下的flag變數，以及info的串列切割長度
(自動續傳有空會實現，目前想法是將以下載的檔案存成log，並比對紀錄)
