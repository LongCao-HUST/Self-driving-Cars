import cv2
import numpy as np

#tach duoc duong mau trang
def empty():
    pass
def colorTrackbar(width=640,height=240):
    cv2.namedWindow("HSV")
    cv2.resizeWindow("HSV", width, height)
    cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
    cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
    cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
    cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
    cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
    cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

def thresholding(img):
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    maskWhite = cv2.inRange(img_hsv, lower, upper)
    return maskWhite


def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp#anh kich co w,h


def nothing(a):
    pass


def initializeTrackbars(intialTracbarVals, wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0], wT // 2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2], wT // 2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)


def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop),
                         (widthBottom, heightBottom), (wT - widthBottom, heightBottom)])
    return points


def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv2.FILLED)
    return img


def getHistogram(img, minPer=0.1, display=False, region=1):
    if region == 1:
        histValues = np.sum(img, axis=0)#cong tong cac cot, mang gom width phan tu
    else:
        histValues = np.sum(img[img.shape[0] // region:, :], axis=0) #chia chieu height

    # print(histValues)
    maxValue = np.max(histValues) #gia tri max
    minValue = minPer * maxValue  #gia tri min = 0.5*max loc nhieu
                                  #0.9 gia tri min value cao-> chi con` 1 ben trai phai
    indexArray = np.where(histValues >= minValue) #chi so cac hang cua histvalue co gia tri lon hon min
    basePoint = int(np.average(indexArray))#cong tong indexarray/so phan tu = gia tri trung binh
    # print(basePoint)

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(histValues):
            cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0] - intensity // 255 // region), (255, 0, 255), 1) #intensity//255 so pixel
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)#1 diem trung binh goc duoi
        return basePoint, imgHist

    return basePoint
