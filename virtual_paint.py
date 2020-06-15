import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)     # sets width
cap.set(4, 480)     # sets height
cap.set(10, 150)    # sets brightness

# to add more colors,
# add the [h_min, s_min, v_min, h_max, s_max, v_max] to the myColors
myColors = [[104, 115, 140, 179, 255, 255]]

# add the [B, G, R] value of list you want to be displayed.
myColorValues = [[255, 0, 0]]

# my_points = [x, y, colorIndex]
my_points = []


def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = -1, -1, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def find_color(img, myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    for color in myColors:
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = get_contours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            my_points.append([x, y, count])
        count += 1
        cv2.imshow(str(color[0]), mask)
    return my_points


def drawOnCanvas():
    for point in my_points:
        cv2.circle(imgResult, (point[0], point[1]), 10, point[2], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    new_points = find_color(img, myColors)
    drawOnCanvas()
    cv2.imshow('Video', img)
    cv2.imshow('color Pen', imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
