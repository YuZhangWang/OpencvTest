import cv2
import numpy as np
#学习重新设置图片大小、裁剪图片

img = cv2.imread("picture/test.jpg")
print(img.shape)

imgResize = cv2.resize(img,(300,300))
print(imgResize.shape)

imgCropped = img[0:200,200:500]

cv2.imshow("Image",img)
cv2.imshow("Image Resize",imgResize)
cv2.imshow("Image Cropped",imgCropped)

cv2.waitKey(0)