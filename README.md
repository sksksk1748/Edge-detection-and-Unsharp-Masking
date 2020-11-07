# Edge detection and Unsharp Masking

|Author|Chieh-Ting Chung|
|---|---
|E-mail|sksksk1748@gmail.com

## Memo

* Image Processing , Edge detection and Unsharp Masking

## Algorithm
* Edge detection
    1. 讀取附件的 8-bit 灰階影像
    2. 顯示輸入影像
    3. 將影像轉換成 double 格式，數值範圍在[0 1]之間
    4. 用雙層迴圈由左而右，由上而下讀取以(x,y)為中心的 3x3 影像區域
    5. 將 3 x 3 影像區域點對點乘上圖 1 Sobel 濾鏡數值矩陣後，將數值總和存入輸出影像的(x,y) 位置
    6. 將濾波後的影像加上 0.5，呈現近似浮雕影像
    7. 分別將濾波後的影像開絕對值，再二值化(門檻值自訂)，用 bitor (bitwise or)或直接相加，產生近似輪廓影像
    8. 轉成 8bit，儲存影像檔

* Unsharp Masking
    * [詳細卷積原理請看【HackMD】影像處理實作筆記](https://hackmd.io/wy83HZzVSFSjIW16y6Rtfg)
    1. 輸入影像模糊參數(例如均值濾波的濾鏡尺寸 n)
    2. 讀取附件的 8-bit 灰階影像
    3. 顯示輸入影像
    4. 將影像轉換成 double 格式，數值範圍在[0 1]之間
    5. 用雙層迴圈對 n*n 濾鏡(均值濾鏡或高斯濾鏡)做影像模糊化
    6. 利用原圖與模糊影像的差異，加上原圖，獲得銳利影像


## Your `~/ImageHW1/` folder should look like this
```
ImageHW1
├── image/
│   └── ...
└── ...

```

## Result

* Edge detection
    * ![](https://i.imgur.com/sa4bN9L.png)

* Unsharp Masking
    * ![](https://i.imgur.com/IAWdDc3.png)

## Reference

* NTUST , Pei-Li Sun PROFESSOR