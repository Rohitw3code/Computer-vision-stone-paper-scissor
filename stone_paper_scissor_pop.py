import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import random as rd
import numpy as np
import time

capture = cv2.VideoCapture(0)
capture.set(3, 980)
capture.set(4, 750)

# Stone Paper Scissor
stone = cv2.imread("stone.png")
paper = cv2.imread("paper.png")
scissor = cv2.imread("scissors.png")
objectType =[1,2,3,1,2,1,2,3,1,3,1,2,3,1,2,3]
spsx = 110
spsy = 480

detector = HandDetector(maxHands=1, detectionCon=0.8)


def subX(point1, point2):
    return point1[0] - point2[0]


def subY(point1, point2):
    return point1[1] - point2[1]


def detectStonePaperScissor(img, target):
    a1, a2, a3, a4 = target[8::4]
    b1, b2, b3, b4 = target[5::4]

    hx1, hy1 = target[3][:2]
    hx2, hy2 = target[17][:2]
    d1 = math.hypot(subX(a1, b1), subY(a1, b1))
    d2 = math.hypot(subX(a2, b2), subY(a2, b2))
    d3 = math.hypot(subX(a3, b3), subY(a3, b3))
    d4 = math.hypot(subX(a4, b4), subY(a4, b4))
    h = math.hypot(hx1 - hx2, hy1 - hy2)

    mean = ((d1 + d2 + d3 + d4) / 4) / h

    if 0.20 < mean < 0.623:
        drawStone(img, target)
        return 1
    elif 0.63 < mean < 0.94:
        drawPaper(img, target)
        return 2
    elif mean > 1:
        drawScissor(img, target)
        return 3
    else:
        print(mean)
        return -1


def drawScissor(img, cursor):
    points = [8, 7, 6, 5, 9, 10, 11, 12]
    scissorColor = (170, 224, 130)
    # displayImage(img, scissor, spsx, spsy)
    for p in range(len(points) - 1):
        cv2.line(img, (cursor[points[p]][0], cursor[points[p]][1]),
                 (cursor[points[p + 1]][0], cursor[points[p + 1]][1]), scissorColor, 5)


def drawPaper(img, cursor):
    points = [0, 1, 2, 3, 4, 3, 2, 5, 6, 7, 8, 7, 6, 5, 9, 10, 11, 12, 11, 10, 9, 13, 14, 15, 16, 15, 14, 13, 17, 18,
              19, 20, 19, 18, 17, 0]
    paperColor = (233, 193, 133)
    # displayImage(img, paper, spsx, spsy)
    for p in range(len(points) - 1):
        cv2.line(img, (cursor[points[p]][0], cursor[points[p]][1]),
                 (cursor[points[p + 1]][0], cursor[points[p + 1]][1]),
                 paperColor, 5)


def drawStone(img, cursor):
    points = [4, 3, 2, 5, 6, 7, 8, 7, 6, 5, 9, 10, 11, 12, 11, 10, 9, 13, 14, 15, 16, 15, 14, 13, 17, 18, 19, 20, 19,
              18, 17]
    stoneColor = (0, 128, 255)
    # displayImage(img, stone, spsx, spsy)
    for p in range(len(points) - 1):
        cv2.line(img, (cursor[points[p]][0], cursor[points[p]][1]),
                 (cursor[points[p + 1]][0], cursor[points[p + 1]][1]),
                 stoneColor, 5)


def createRectangleText(text, cx, cy, sizex, sizey, fontSize=1, bold=2):
    cv2.rectangle(img, (cx - sizex, cy - sizey), (cx + sizex-50, cy + sizey), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, f'{text}', (cx -10- sizex // 2, cy + sizey // 3), cv2.FONT_HERSHEY_DUPLEX,
                fontSize, (0, 0, 255), bold)


def displayImage(img, dispalyImg, x, y):
    desired_size = 64
    top,bottom,left,right = [10,10,10,10]


    dispalyImg = cv2.copyMakeBorder(dispalyImg, top, bottom, left, right, cv2.BORDER_CONSTANT,
                       value=(255,255,255))
    img[x:x + desired_size+20, y:y + desired_size+20, :] = dispalyImg[:desired_size+20,:desired_size+20,:]

def resultDisplay(result):
    x = 470
    y = 450
    cv2.rectangle(img, (450, 400), (630, 490), (255, 255, 255), cv2.FILLED)
    if result == "You Won":
        cv2.putText(img, f'{result}', (x,y), cv2.FONT_HERSHEY_DUPLEX,
            1, (0, 255, 0), 2)
    elif result == "You Loss":
        cv2.putText(img, f'{result}',(x,y), cv2.FONT_HERSHEY_DUPLEX,
            1, (0, 0, 255), 2)
    else:
        cv2.putText(img, f'{result}',(x,y), cv2.FONT_HERSHEY_DUPLEX,
            1, (255, 0, 0), 2)


def targetBox(img,colorCode):
    decisionBox = np.ones((200,200,3))*colorCode
    img[70:270,:200] = decisionBox

def startTimer(cx,cy,stop=False):
    cv2.circle(img, (cx, cy),30, (255, 255, 255), cv2.FILLED)
    if stop:
        cv2.putText(img, f'0', (cx-10, cy+10), cv2.FONT_HERSHEY_DUPLEX,
                1, (0, 0, 0), 1)
    else:
        cv2.putText(img, f'{int(totalTime-(time.time()-timeStart))}', (cx-10, cy+10), cv2.FONT_HERSHEY_DUPLEX,
                1, (0, 0, 0), 1)


def computerSPS(img):
    val = rd.choice(objectType)
    if val == 1:
        displayImage(img, stone, spsx, spsy)
        return 1
    elif val == 2:
        displayImage(img, paper, spsx, spsy)
        return 2
    else:
        displayImage(img, scissor, spsx, spsy)
        return 3

def lastPart():
    cv2.rectangle(img, (450, 50), (600, 250), (255, 255, 255), cv2.FILLED)
    if val == 1:
        displayImage(img, stone, spsx, spsy)
    elif val == 2:
        displayImage(img, paper, spsx, spsy)
    elif val == 3:
        displayImage(img, scissor, spsx, spsy)
    startTimer(530, 70, stop=True)
    resultDisplay(whoWin(playVal, val))
    if playVal == 1:
        drawStone(img, playerCood)
    elif playVal == 2:
        drawPaper(img, playerCood)
    else:
        drawScissor(img, playerCood)

def whoWin(userInput,systemInput):
    print(userInput,systemInput)
    if userInput == systemInput:
        print("draw")
        return "Draw"
    if userInput == 1 and systemInput == 2: # stone and paper
        print("System Win")
        return "You Loss"
    else:
        print("Player Win")
        return "You Won"

    if userInput == 2 and systemInput == 3: # paper and scissor
        print("System Win")
        return "You Loss"
    else:
        print("Player Loss")
        return "You Won"

    if userInput == 3 and systemInput == 1: # scissor and stone
        print("System Win")
        return "You Loss"
    else:
        print("Player Loss")
        return "You Won"


timeStart = time.time()
totalTime = 4
colorCode = 255

stop = 0
val = "Not selected"
playVal = -1
playerCood = []
while True:
    success, img = capture.read()
    img = cv2.flip(img, 1)
    hand = detector.findHands(img, draw=False)
    targetBox(img,colorCode)
    if stop == 1:
        lastPart()
    if hand:
        lmList = hand[0]['lmList']
        bx, by, bw, bh = hand[0]["bbox"]
        obj = detectStonePaperScissor(img, lmList)
        objText = {"1": "Stone", "2": "Paper", "3": "Scissor", "-1": "Hand not found"}
        createRectangleText(objText[str(playVal)], 100, 50, 150, 30)
        cv2.rectangle(img, (450, 50), (600, 250), (255, 255, 255), cv2.FILLED)
        if bx<200 and bx+bw < 200 and 70<by<270 and 70<by+bh<270:
            if int(totalTime-(time.time()-timeStart)) < 0:
                lastPart()
                stop = 1

            else:
                val = computerSPS(img)
                playVal = obj
                playerCood = lmList
                colorCode = 100
                startTimer(530, 70)
        else:
            colorCode = 255
            displayImage(img,stone,spsx,spsy)
            startTimer(530, 70)
            timeStart = time.time()



    else:
        createRectangleText("Hand not found", 100, 50, 150, 30, fontSize=0.7, bold=1)



    cv2.imshow("Stone Paper Scissor Detector", img)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
