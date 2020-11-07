# Unsharp Masking(USM)影像銳化

import numpy as np
import cv2

# 1. 輸入影像模糊參數(例如均值濾波的濾鏡尺寸 n)。
while True:
    inputValue = int(input("input a filter number ex. n = 3, 5, 7, 11 : "))

    if inputValue == 3:
        meanFilter = np.array([(1,1,1),(1,1,1),(1,1,1)]) *(1/9)
        break
    elif inputValue == 5:
        meanFilter = np.array([(1,1,1,1,1),(1,1,1,1,1),(1,1,1,1,1),(1,1,1,1,1),(1,1,1,1,1)]) *(1/25)
        break
    elif inputValue == 7:
        meanFilter = np.array([(1,1,1,1,1,1,1), (1,1,1,1,1,1,1), (1,1,1,1,1,1,1), (1,1,1,1,1,1,1), (1,1,1,1,1,1,1), (1,1,1,1,1,1,1), (1,1,1,1,1,1,1)]) *(1/49)
        break
    elif inputValue == 11:
        meanFilter = np.array([(1,1,1,1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1,1,1,1),
                         (1,1,1,1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1,1,1,1),
                         (1,1,1,1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1,1,1,1),
                         (1,1,1,1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1,1,1,1)]) *(1/121)
        break
    else:
        continue

# 2. 讀取附件的 8-bit 灰階影像。
inputImg = cv2.imread('image/cameraman.jpg',0)
tempImg = cv2.imread('image/cameraman.jpg',0)

# 3. 顯示輸入影像。
cv2.imshow('Original image', inputImg)

# 4. 將影像轉換成 double 格式，數值範圍在[0 1]之間。
inputImg = inputImg/255
tempImg = tempImg / 255

s = inputImg.shape
f = meanFilter.shape

# martix 邊界都填0
rowLength = s[0]+f[0]-1 # s[0]原圖二維length + filter[0] 二維length -1 等於原圖加入四周都加入padding , np.shape[0] 第二維長度 
colLength = s[1]+f[1]-1 # s[1]原圖一維length + filter[1] 一維length -1 等於原圖加入四周都加入padding , np.shape[1] 第一維長度 
z = np.zeros((rowLength,colLength))
# martix 邊界都填0

# 在不屬於padding 處增加原圖的image pixel
for i in range(s[0]):
    for j in range(s[1]):
        z[i+np.int((f[0]-1)/2), j+np.int((f[1]-1)/2)] = inputImg[i,j]

# 5. 用雙層迴圈對 n*n 濾鏡(均值濾鏡或高斯濾鏡)做影像模糊化，獲得近似圖3(b)的結果。
for i in range(s[0]):
    for j in range(s[1]):
        #卷積處理
        k = z[i:i+f[0], j:j+f[1]] # 原圖的長、寬控制filter滑動次數, numpy Slicing 寫法，回傳指定參數一部份的array
        #if j == 0:
        #    print(k)
        convpixelResult = np.sum(k * meanFilter)
        #卷積處理
        inputImg[i,j] = convpixelResult

cv2.imshow('fuzzy',inputImg)

# 6. 利用原圖與模糊影像的差異，加上原圖，獲得類似圖 3(c)的銳利影像。 
outputImg =   0.8*(tempImg - inputImg) +tempImg

cv2.imshow('sharp',outputImg)
cv2.waitKey(0)