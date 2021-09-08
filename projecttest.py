import cv2
import numpy as np

frameWidth = 640  # chapter1
frameHeight = 480  # chapter1
cap = cv2.VideoCapture(0)  # chapter1
cap.set(3, frameWidth)  # chapter1
cap.set(4, frameHeight)  # chapter1
cap.set(10, 150)  # chapter1

myColors = [[0, 91, 0, 9, 255, 255],  # 要拥有最小和最大色相和饱和度值
            [104, 100, 33, 174, 255, 226],
            [77, 150, 0, 91, 255, 255]]

# 将设定好的颜色值转化为BGR的形式
myColorValues = [[0, 0, 255],  # 红色
                 [255, 0, 0],  # 蓝色
                 [0, 255, 0]]  # 绿色

myPoints = []  ## [x , y , colorId ]


def findColor(img, myColors, myColorValues):  # 查找颜色函数
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 8, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return newPoints


def getContours(img):  # chapter8
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # chapter8
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # chapter8
            x, y, w, h = cv2.boundingRect(approx)  # chapter8
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        # 重复画圆，达到绘制成路径的效果
        cv2.circle(imgResult, (point[0], point[1]), 8, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    if success == True:  # 用来实现输出的水平翻转
        new_img = cv2.flip(imgResult, 180)

    cv2.imshow("Result", new_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
