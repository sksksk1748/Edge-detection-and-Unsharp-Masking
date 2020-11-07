# 影像邊緣偵測
import numpy as np
import cv2


# 卷積filter，並return各pixel跟filter相乘的sum
def convolution(imgPixel, kernel):
    row1_Sum = imgPixel[0, 0] * kernel[0, 0] + imgPixel[0, 1] * kernel[0, 1] + imgPixel[0, 2] * kernel[0, 2]
    row2_Sum = imgPixel[1, 0] * kernel[1, 0] + imgPixel[1, 1] * kernel[1, 1] + imgPixel[1, 2] * kernel[1, 2]
    row3_Sum = imgPixel[2, 0] * kernel[2, 0] + imgPixel[2, 1] * kernel[2, 1] + imgPixel[2, 2] * kernel[2, 2]
    return row1_Sum + row2_Sum + row3_Sum


# 取得部分3 x 3 影像區域
def takePartImage(inpimg, i, j):
    image = np.zeros((3, 3))
    a = i
    b = j
    for k in range(0, 3):
        b = j
        for l in range(0, 3):
            image[k, l] = inpimg[a, b]
            b = b + 1
        a = a + 1
    return image


# 取得sobel垂直filter的martix
def sobelX(inputimg):
    rows = len(inputimg)
    cols = len(inputimg[0])
    filtX = np.array(np.mat('-1 0 1; -2 0 2; -1 0 1'))
    outputimg = np.zeros((rows, cols))
    for i in range(0, rows - 3):
        for j in range(0, cols - 3):
            # 取得部分3 x 3 影像區域，由左至右、由上而下
            partImage = takePartImage(inputimg, i, j)
            # 用取得部分3 x 3 的影像區域，去跟filter卷積
            outputimg[i, j] = convolution(partImage, filtX)
    return outputimg


# 取得sobel水平filter的martix
def sobelY(inputimg):
    rows = len(inputimg)
    cols = len(inputimg[0])
    filtY = np.array(np.mat('-1 -2 -1; 0 0 0; 1 2 1'))
    outputimg = np.zeros((rows, cols))
    for i in range(0, rows - 3):
        for j in range(0, cols - 3):
            # 取得部分3 x 3 影像區域，由左至右、由上而下
            partImage = takePartImage(inputimg, i, j)
            # 用取得部分3 x 3 的影像區域，去跟filter卷積
            outputimg[i, j] = convolution(partImage, filtY)
    return outputimg


# 1. 讀取附件的 8-bit 灰階影像
inputimg = cv2.imread('image/cameraman.jpg', 0)
# 2. 顯示輸入影像
cv2.imshow('Original image', inputimg)

# 3. 將影像轉換成 double 格式，數值範圍在[0 1]之間
inputimg = inputimg / 255

# 4. 用雙層迴圈由左而右，由上而下讀取以(x,y)為中心的 3x3 影像區域。
# 5.將 3 x 3 影像區域點對點乘上圖 1 Sobel 濾鏡數值矩陣後，將數值總和存入輸出影像的(x,y) 位置。
sobelimagex = sobelX(inputimg)
sobelimagey = sobelY(inputimg)

# 6. 將濾波後的影像加上 0.5，呈現近似圖 2(b)的浮雕影像。
cv2.imshow('Relief image', sobelimagex + 0.5)

rows = len(inputimg)  # 256
cols = len(inputimg[0])  # 256
outputimg = np.zeros([rows, cols])  # 把 array 都填 0

# 7. 分別將濾波後的影像開絕對值，再二值化(門檻值自訂))，用 bitor (bitwise or)或直接相加，產生近似圖 2(c)的輪廓影像。
for i in range(0, rows):
    for j in range(0, cols):
        if abs(sobelimagex[i, j]) >= 0.5:
            sobelimagex[i, j] = 1
        else:
            sobelimagex[i, j] = 0

        if abs(sobelimagey[i, j]) >= 0.5:
            sobelimagey[i, j] = 1
        else:
            sobelimagey[i, j] = 0

        outputimg[i, j] = sobelimagex[i, j] + sobelimagey[i, j]

cv2.imshow('Sobel image', outputimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
