import cv2

# 学习视频输出和退出

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while True:
    success, img = cap.read()
    if success == True:
        new_img = cv2.flip(img, 180)
    cv2.imshow("Video", new_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
