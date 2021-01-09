"""
File : ColorSegment.py 
Do : 影像色彩分割
Author : Chieh-Ting Chung
Date : 2020/11/30

https://rodrigoberriel.com/2014/11/opencv-color-spaces-splitting-channels/
上面link是opencv各個色彩空間的range
"""

import numpy as np
import cv2
import math
import random
from time import time
import os

start_time = time()

# 計算平均值
def average(im_colorSpace,colorNum):
    # colorNum : 1 is rgb, 2 is YCbCr, 3 is HSV

    mean = []

    #extrect value of diffient channel
    im_R = im_colorSpace[:,:,0]
    im_G = im_colorSpace[:,:,1]
    im_B = im_colorSpace[:,:,2]


    rows = len(im_R)  #
    cols = len(im_R[0])  # 
    totalPixel_R = 0
    totalPixel_G = 0
    totalPixel_B = 0
    count = 0
    for i in range(0, rows):
        for j in range(0, cols):
            if im_R[i][j] == 0 :
                continue
            totalPixel_R = im_R[i][j] + totalPixel_R
            totalPixel_G = im_G[i][j] + totalPixel_G
            totalPixel_B = im_B[i][j] + totalPixel_B
            count = count + 1

    meanPixel_R = totalPixel_R / count
    meanPixel_G = totalPixel_G / count
    meanPixel_B = totalPixel_B / count

    mean.append(meanPixel_R)
    mean.append(meanPixel_G)
    mean.append(meanPixel_B)

    if colorNum == 1 :
        print('圖片的 BGR 平均值為\n[{:.3f}，{:.3f}，{:.3f}]'.format( mean[0],mean[1],mean[2]) )
        return mean
    if colorNum == 2 :
        print('圖片的 YCbCr 平均值為\n[{:.3f}，{:.3f}，{:.3f}]'.format( mean[0],mean[1],mean[2]) )
        return mean
    if colorNum == 3 :
        print('圖片的 HSV 平均值為\n[{:.3f}，{:.3f}，{:.3f}]'.format( mean[0],mean[1],mean[2]) )
        return mean
    #cv.imread()讀取Img時候將rgb轉換為了bgr

# 計算標準差
def SD(im_colorSpace, mean, colorNum):
    # colorNum : 1 is rgb, 2 is YCbCr, 3 is HSV

    sd = []

    #extrect value of diffient channel
    im_R = im_colorSpace[:,:,0]
    im_G = im_colorSpace[:,:,1]
    im_B = im_colorSpace[:,:,2]

    rows = len(mask)  
    cols = len(mask[0])  

    total_R = np.zeros((rows, cols))
    total_G = np.zeros((rows, cols))
    total_B = np.zeros((rows, cols))
    count = 0
    for i in range(0, rows):
        for j in range(0, cols):
            if im_R[i][j] == 0 :
                continue
            total_R[i][j] = abs(im_R[i][j] - mean[0])**2
            total_G[i][j] = abs(im_G[i][j] - mean[1])**2
            total_B[i][j] = abs(im_B[i][j] - mean[2])**2
            count = count + 1

    num_sum_r = 0
    num_sum_g = 0
    num_sum_b = 0
    for i in range(0, rows):
        for j in range(0, cols):
            num_sum_r = total_R[i][j] + num_sum_r
            num_sum_g = total_G[i][j] + num_sum_g
            num_sum_b = total_B[i][j] + num_sum_b
            
    std_R = math.sqrt(num_sum_r / count)
    std_G = math.sqrt(num_sum_g / count)
    std_B = math.sqrt(num_sum_b / count)

    sd.append(std_R)
    sd.append(std_G)
    sd.append(std_B)

    if colorNum == 1 : 
        print('圖片的 BGR 標準差為\n[{:.3f}，{:.3f}，{:.3f}]'.format( sd[0], sd[1], sd[2]) )
        return sd
    if colorNum == 2 :
        print('圖片的 YCbCr 標準差為\n[{:.3f}，{:.3f}，{:.3f}]'.format( sd[0], sd[1], sd[2]) )
        return sd
    if colorNum == 3 :
        print('圖片的 HSV 標準差為\n[{:.3f}，{:.3f}，{:.3f}]'.format( sd[0], sd[1], sd[2]) )
        return sd

# 依每張圖設置不一樣的標準差放大倍率,調整mask分割效果
def sd_magMask(img, colorNum, sd_mag):
    # colorNum : 1 is rgb, 2 is YCbCr, 3 is HSV
    # sd_mag 為標準差放大倍率
    
    if colorNum == 1 :  
        # img_2 RGB mask
        #im2_rgbmask = cv2.inRange(img_2, (112, 82, 46), (248, 182, 106)) 手算
        im2_rgbmask = cv2.inRange(img, ( im_rgb_mean[0] - im_rgb_sd[0]*sd_mag, im_rgb_mean[1] - im_rgb_sd[1]*sd_mag, im_rgb_mean[2]- im_rgb_sd[2]*sd_mag ), 
                                        ( im_rgb_mean[0] + im_rgb_sd[0]*sd_mag, im_rgb_mean[1] + im_rgb_sd[1]*sd_mag, im_rgb_mean[2]+ im_rgb_sd[2]*sd_mag ))
        return im2_rgbmask

    if colorNum == 2 :
        # img_2 ycbcr mask
        #im2_YCbCrmask = cv2.inRange(YCbCr_img2, (75, 64, 100), (168, 132, 222)) 手算
        im2_YCbCrmask = cv2.inRange(img, ( im_ycbcr_mean[0] - im_ycbcr_sd[0]*sd_mag, im_ycbcr_mean[1] - im_ycbcr_sd[1]*sd_mag, im_ycbcr_mean[2] - im_ycbcr_sd[2]*sd_mag ), 
                                                ( im_ycbcr_mean[0] + im_ycbcr_sd[0]*sd_mag, im_ycbcr_mean[1] + im_ycbcr_sd[1]*sd_mag, im_ycbcr_mean[2] + im_ycbcr_sd[2]*sd_mag )) 
        return im2_YCbCrmask
    if colorNum == 3 :
        # img_2 hsv mask
        #im2_hsvmask = cv2.inRange(hsv_img2, (64, 91, 112), (142, 205, 248)) 手算
        im2_hsvmask = cv2.inRange(img, ( im_hsv_mean[0] - im_hsv_sd[0]*sd_mag, im_hsv_mean[1] - im_hsv_sd[1]*sd_mag, im_hsv_mean[2] - im_hsv_sd[2]*sd_mag ), 
                                                ( im_hsv_mean[0] + im_hsv_sd[0]*sd_mag, im_hsv_mean[1] + im_hsv_sd[1]*sd_mag, im_hsv_mean[2] + im_hsv_sd[2]*sd_mag ))
        return im2_hsvmask

# mask以外填色
def drawcolor(im_colorSpace, colorNum, displayWin):
    # colorNum : 1 is rgb, 2 is YCbCr, 3 is HSV
    # displayWin : 1 is fist image window, 2 is second image window 
    # -- 這樣做是因為, image 1 跟 image 2 都有call drawcolor()
    # -- 可是最後只會顯示 image2, 因為在副程式裡 inshow()的 window 名稱(draw_RGB)共用
    # -- example ==> cv2.imshow('draw_RGB', im_colorSpace)

    mean = []

    im_R = im_colorSpace[:,:,0]
    im_G = im_colorSpace[:,:,1]
    im_B = im_colorSpace[:,:,2]


    rows = len(im_R)  # first image 600/ second image 480
    cols = len(im_R[0]) # first image 800/ second image 640

    baseline_a = 166
    baseline_b = 143
    baseline_c = 158
    for i in range(0, rows):
        count_a = 0
        num_b = 0
        for j in range(0, cols):
            if im_R[i][j] != 0 :
                if count_a/100 == 0:
                    baseline_a = random.randint(1,255)
                    baseline_b = random.randint(1,255)
                    baseline_c = random.randint(1,255)
                else : 
                    im_R[i][j] = baseline_a
                    im_G[i][j] = baseline_b
                    im_B[i][j] = baseline_c
                count_a = count_a + 1
            else:
                if num_b % 10 == 0:
                    im_R[i][j] = 0
                    im_G[i][j] = 0
                    im_B[i][j] = 0
                elif num_b % 6 == 0: 
                    im_R[i][j] = 255
                    im_G[i][j] = 255
                    im_B[i][j] = 255
                num_b = num_b + 1

    if colorNum == 1 and displayWin == 1:           
        cv2.imshow('drawImg_RGB', im_colorSpace)
        #cv2.imwrite('image/drawImg_RGB.jpg',im_colorSpace)
    if colorNum == 1 and displayWin == 2:           
        cv2.imshow('drawImg2_RGB', im_colorSpace)
        #cv2.imwrite('image/drawImg2_RGB.jpg',im_colorSpace)

    if colorNum == 2 and displayWin == 1:
        cv2.imshow('drawImg_YCbCr', im_colorSpace)
        #cv2.imwrite('image/drawImg_YCbCr.jpg',im_colorSpace)
    if colorNum == 2 and displayWin == 2:
        cv2.imshow('drawImg2_YCbCr', im_colorSpace)
        #cv2.imwrite('image/drawImg2_YCbCr.jpg',im_colorSpace)

    if colorNum == 3 and displayWin == 1:
        cv2.imshow('drawImg_HSV', im_colorSpace)
        #cv2.imwrite('image/drawImg_HSV.jpg',im_colorSpace)
    if colorNum == 3 and displayWin == 2:
        cv2.imshow('drawImg2_HSV', im_colorSpace)
        #cv2.imwrite('image/drawImg2_HSV.jpg',im_colorSpace)

# 黑白灰階圖填入mask區域
def drawgray(im_colorSpace, colorNum, displayWin, draw_grayImg):
    # colorNum : 1 is rgb, 2 is YCbCr, 3 is HSV
    # displayWin : 1 is fist image window, 2 is second image window 
    # -- 這樣做是因為, image 1 跟 image 2 都有call drawcolor()
    # -- 可是最後只會顯示 image2, 因為在副程式裡 inshow()的 window 名稱(draw_RGB)共用
    # -- example ==> cv2.imshow('draw_RGB', im_colorSpace)
    # draw_grayImg : ex. draw_grayImg2, draw_grayImg3

    mean = []

    im_R = im_colorSpace[:,:,0]
    im_G = im_colorSpace[:,:,1]
    im_B = im_colorSpace[:,:,2]


    rows = len(im_R)  # first image 600/ second image 480
    cols = len(im_R[0]) # first image 800/ second image 640


    for i in range(0, rows):
        for j in range(0, cols):
            if im_R[i][j] == 0 :
                im_R[i][j] = draw_grayImg[i][j]
                im_G[i][j] = draw_grayImg[i][j]
                im_B[i][j] = draw_grayImg[i][j]
                


    if colorNum == 1 and displayWin == 1:           
        cv2.imshow('drawgrayImg_RGB', im_colorSpace)
        #cv2.imwrite('image/drawImg_RGB.jpg',im_colorSpace)
    if colorNum == 1 and displayWin == 2:           
        cv2.imshow('drawgrayImg2_RGB', im_colorSpace)
        #cv2.imwrite('image/drawImg2_RGB.jpg',im_colorSpace)

    if colorNum == 2 and displayWin == 1:
        cv2.imshow('drawgrayImg_YCbCr', im_colorSpace)
        #cv2.imwrite('image/drawImg_YCbCr.jpg',im_colorSpace)
    if colorNum == 2 and displayWin == 2:
        cv2.imshow('drawgrayImg2_YCbCr', im_colorSpace)
        #cv2.imwrite('image/drawImg2_YCbCr.jpg',im_colorSpace)

    if colorNum == 3 and displayWin == 1:
        cv2.imshow('drawgrayImg_HSV', im_colorSpace)
        #cv2.imwrite('image/drawImg_HSV.jpg',im_colorSpace)
    if colorNum == 3 and displayWin == 2:
        cv2.imshow('drawgrayImg2_HSV', im_colorSpace)
        #cv2.imwrite('image/drawImg2_HSV.jpg',im_colorSpace)
"""
===================================================================
= Step 1 : 
= 根據附件影像(sky.jpg)與其藍天區域遮罩(sky_mask.jpg)
= 分別統計藍天在 RGB/YCbCr/HSV 三種色空間中的平均值與標準差。
===================================================================
"""

# 相對路徑 image/cameraman.jpg 替代方案
# https://reurl.cc/Q7p4d0
path = os.path.join(os.path.dirname(__file__), 'image/')

# read original image and mask image
img = cv2.imread(path + 'sky.jpg')
#cv2.imshow('img', img)
img_2 = cv2.imread(path + 'sky_2.jpg')
#cv2.imshow('img_2', img_2)
img_3 = cv2.imread(path + 'sky_8.jpg')
#cv2.imshow('img_3', img_3)
mask = cv2.imread(path + 'sky_mask.jpg',0)

# 把原圖變灰階,因 drawgray function 需要把非藍天區域的 mask(黑色區域) 貼上對應的灰階 pixel
draw_grayImg2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
draw_grayImg3 = cv2.cvtColor(img_3, cv2.COLOR_BGR2GRAY)

#cv2.imshow('draw_grayImg2', draw_grayImg2)
#cv2.imshow('draw_grayImg3', draw_grayImg3)

# 轉色彩空間 YCbCr
YCbCr_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
YCbCr_img2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2YCR_CB)
YCbCr_img3 = cv2.cvtColor(img_3, cv2.COLOR_BGR2YCR_CB)

#cv2.imshow('YCbCr_img', YCbCr_img)
#cv2.imshow('YCbCr_img2', YCbCr_img2)
#cv2.imshow('YCbCr_img3', YCbCr_img3)

# 轉色彩空間 HSV
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_img2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2HSV)
hsv_img3 = cv2.cvtColor(img_3, cv2.COLOR_BGR2HSV)

#cv2.imshow('HSV_img', hsv_img)
#cv2.imshow('HSV_img2', hsv_img2)
#cv2.imshow('HSV_img3', hsv_img3)


# 二值化 
ret, mask = cv2.threshold(mask, 127, 255,cv2.THRESH_BINARY)

# Combine original image and mask image
im_rgb = cv2.bitwise_and(img, img, mask = mask)
im_ycbcr = cv2.bitwise_and(YCbCr_img, YCbCr_img, mask = mask)
im_hsv = cv2.bitwise_and(hsv_img, hsv_img, mask = mask)

#cv2.imshow('RGB_Mask', im_rgb)
#cv2.imshow('YCbCr_Mask', im_ycbcr)
#cv2.imshow('HSV_mask', im_hsv)

# 計算老師給的圖的平均值跟標準差，並印出
im_rgb_mean = average(im_rgb,1)
im_rgb_sd = SD(im_rgb,im_rgb_mean,1)

im_ycbcr_mean = average(im_ycbcr,2)
im_ycbcr_sd = SD(im_ycbcr,im_ycbcr_mean,2)

# https://www.itread01.com/content/1548504935.html
# OpenCV 中 HSV的範圍,照以下做就是標準的hsv顏色,符合線上調色盤
# h= h*2;
# s = (float)s/255*100;
# v = (float)v/255*100;

im_hsv_mean = average(im_hsv,3)
im_hsv_sd = SD(im_hsv,im_hsv_mean,3)


"""
===================================================================
= Step 2 : 
= 用自己找的 2 張有藍天的新圖轉換 RGB, YCbCr, HSV 三種色空間
= 並使用老師給的 image 算出後的平均值與標準差，取得新圖的二值化 image
===================================================================
"""

# img_2 的 HSV mask
# blue (110,150,50) ~ (120,255,255)

# im2_mask = cv2.inRange(hsv_img2, (100, 50, 100), (255, 255,255))  手調分割超成功
# HSV平均值+標準差範圍
# 參考 :
# https://stackoverflow.com/questions/48109650/how-to-detect-two-different-colors-using-cv2-inrange-in-python-opencv

im2_rgbmask = sd_magMask(img_2, 1, 3)
im2_YCbCrmask = sd_magMask(YCbCr_img2, 2, 3)
im2_hsvmask = sd_magMask(hsv_img2, 3, 3)

im3_rgbmask = sd_magMask(img_3, 1, 5)
im3_YCbCrmask = sd_magMask(YCbCr_img3, 2, 4)
im3_hsvmask = sd_magMask(hsv_img3, 3, 5)

#cv2.imshow('im2_RGB_Mask', im2_rgbmask)
#cv2.imshow('im2_YCbCr_Mask', im2_YCbCrmask)
#cv2.imshow('im2_HSV_Mask', im2_hsvmask)

#cv2.imshow('im3_RGB_Mask', im3_rgbmask)
#cv2.imshow('im3_YCbCr_Mask', im3_YCbCrmask)
#cv2.imshow('im3_HSV_Mask', im3_hsvmask)


"""
===================================================================
= Step 3 : 
= 把 Step 2 的二值化影像跟自己找的新圖做 AND 
= 並把產生後的 image，藍天部分處裡為"彩色"，其餘區域處裡為黑白的image
===================================================================
"""

im2_rgb = cv2.bitwise_and(img_2, img_2, mask = im2_rgbmask)
im2_ycbcr = cv2.bitwise_and(YCbCr_img2, YCbCr_img2, mask = im2_YCbCrmask)
im2_hsv = cv2.bitwise_and(hsv_img2, hsv_img2, mask = im2_hsvmask)

im3_rgb = cv2.bitwise_and(img_3, img_3, mask = im3_rgbmask)
im3_ycbcr = cv2.bitwise_and(YCbCr_img3, YCbCr_img3, mask = im3_YCbCrmask)
im3_hsv = cv2.bitwise_and(hsv_img3, hsv_img3, mask = im3_hsvmask)

# 顯示各個色彩空間mask後的圖
#cv2.imshow('im2_RGB_bitwise_and()_Mask', im2_rgb)
#cv2.imshow('im2_YCbCr_bitwise_and()_Mask', im2_ycbcr)
#cv2.imshow('im2_HSV_bitwise_and()_Mask', im2_hsv)

#cv2.imshow('im3_RGB_bitwise_and()_Mask', im3_rgb)
#cv2.imshow('im3_YCbCr_bitwise_and()_Mask', im3_ycbcr)
#v2.imshow('im3_HSV_bitwise_and()_Mask', im3_hsv)

# 顯示把mask後的圖著色的結果
#drawcolor(im2_rgb,1,1)
#drawcolor(im2_ycbcr,2,1)
#drawcolor(im2_hsv,3,1)

#drawcolor(im3_rgb,1,2)
#drawcolor(im3_ycbcr,2,2)
#drawcolor(im3_hsv,3,2)

drawgray(im2_rgb,1,1,draw_grayImg2)
drawgray(im2_ycbcr,2,1,draw_grayImg2)
drawgray(im2_hsv,3,1,draw_grayImg2)

drawgray(im3_rgb,1,2,draw_grayImg3)
drawgray(im3_ycbcr,2,2,draw_grayImg3)
drawgray(im3_hsv,3,2,draw_grayImg3)



end_time = time()
print("執行了這支程式共花了 {:.3f}".format(end_time-start_time)," 秒")


cv2.waitKey(0)
cv2.destroyAllWindows()