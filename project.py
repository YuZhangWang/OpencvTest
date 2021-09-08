import cv2
import numpy as np

'''
官方文档第1章的内容，获取摄像头，以便进行读取
官方文档第2章的内容，进行每一种颜色的识别测试，然后用for循环进行多个颜色的读取识别
官方文档第8章的内容，获取需要识别颜色的轮廓，然后绘制圆形，这是绘制运动路径的基础
然后创建一个新的drawOnCanvas，在画布上绘制的函数，进行重复画圆，达到绘制成路径的效果
'''

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

myPoints = []  # [x , y , colorId ]


def findColor(img, myColors, myColorValues):  # 查找颜色函数
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # chapter2
    count = 0  # 计数器来计算实际计数多少次

    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])  # chapter2 这里改为取前三个值
        upper = np.array(color[3:6])  # chapter2 这里改为取3-6的值
        mask = cv2.inRange(imgHSV, lower, upper)  # chapter2
        x, y = getContours(mask)  # 调用获取轮廓的函数
        # 绘制圆，中心点由x和y坐标确定，半径定为8，获取识别的颜色，然后进行圆的填充
        cv2.circle(imgResult, (x, y), 8, myColorValues[count], cv2.FILLED)
        # 在计数前，如果x和y不等于0，每次记录新的点进行追加
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # 测试用到的输出
        # cv2.imshow(str(color[0]),mask)
    return newPoints


def getContours(img):  # chapter8
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # chapter8
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # 、 cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # chapter8
            x, y, w, h = cv2.boundingRect(approx)  # chapter8
    return x + w // 2, y  # 返回尖端的最高点和中心点，如果小于500未检测到，仍需要返回一些值


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        # 重复画圆，达到绘制成路径的效果
        cv2.circle(imgResult, (point[0], point[1]),
                   8, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()  # chapter1
    imgResult = img.copy()

    newPoints = findColor(img, myColors, myColorValues)

    # 如果得到的新点长度不等于0，就要进行迭代
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    if success == True:  # 用来实现输出的水平翻转
        new_img = cv2.flip(imgResult, 180)

    cv2.imshow("Result", new_img)  # chapter1
    if cv2.waitKey(1) & 0xFF == ord('q'):  # chapter1
        break  # chapter1
