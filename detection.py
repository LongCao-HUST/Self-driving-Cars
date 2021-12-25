import cv2
import numpy as np
import utlis
import serial

curveList = []
avgVal = 10
arduino = serial.Serial('COM5', 9600)

def getLaneCurve(img, display=2):
    imgCopy = img.copy()
    imgResult = img.copy()

    #### STEP 1

    imgThres = utlis.thresholding(img) #thu duoc anh den trang

    #### STEP 2
    hT, wT, c = img.shape #240x480x3
    points = utlis.valTrackbars() #lay toa do 4 diem
    imgWarp = utlis.warpImg(imgThres, points, wT, hT) #xoay anh
    imgWarpPoints = utlis.drawPoints(imgCopy, points) #ve 4 diem vao` anh imgCopy

    #### STEP 3
    middlePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4) #do độ sáng gần góc dưới điểm cân bằng của biểu đồ sáng ở giữa, chia 4 phan lay' 3 phan duoi'
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)#tra ve 1 diem thể hiện số lượng pixel nhiều ở bên trái hay phải
    curveRaw = curveAveragePoint - middlePoint #tru gia tri - la left, + la right

    #### SETP 4
    curveList.append(curveRaw) #gia tri tru them vao list
    if len(curveList) > avgVal: #10 gia tri xoa gia tri dau(lon hon 10 khung hinh)
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))#gia tri trung binh cua list

    #### STEP 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
    if display == 2:
        imgStacked = [img,imgWarpPoints,imgWarp,imgHist,imgLaneColor,imgResult]
        imgStackedName = ['img','imgWarpPoints','imgWarp','imgHist','imgLaneColor','imgResult']
        for i in range(len(imgStacked)):
            cv2.imshow(imgStackedName[i],imgStacked[i])
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)

    #NORMALIZATION
    curve = curve / 100
    if curve > 1: curve == 1
    if curve < -1: curve == -1

    return curve

if __name__ == '__main__':
    cap = cv2.VideoCapture("https://192.168.43.1:8080/video")
    intialTrackBarVals = [102, 80, 20, 214]
    utlis.initializeTrackbars(intialTrackBarVals)
    utlis.colorTrackbar(640,240)
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (480, 240)) #h = 240,w = 480
        curve = getLaneCurve(img, display=2)
        print(curve)
        # cv2.imshow('Vid',img)
        if curve <= -0.2:
            arduino.write(b'0')
            print("LEFT")
        elif curve > -0.2 and curve < 0.2:
            arduino.write(b'1')
            print("STRAIGHT")
        elif curve >= 0.2:
            arduino.write(b'2')
            print("RIGHT")
        if cv2.waitKey(1) == ord("q"):
            break