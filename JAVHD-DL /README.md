## 使用方法

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
