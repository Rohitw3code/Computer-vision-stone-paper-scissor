import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import random as rd
import numpy as np
import time

capture = cv2.VideoCapture(0)
frameWidth = 980
frameHeight = 750
capture.set(3, frameWidth)
capture.set(4, frameHeight)

# Stone Paper Scissor
stone = cv2.imread("stone.png")
paper = cv2.imread("paper.png")
scissor = cv2.imread("scissors.png")
objectType =[1,2,3,1,2,1,2,3,1,3,1,2,3,1,2,3]
totalTime = 4

detector = HandDetector(maxHands=1, detectionCon=0.8)

class Rect():
    def __init__(self,x,y,w,h,tx=0,ty=0,bgColor=(255,255,255),fgColor=(0,0,0),fontSize=1,thickness=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tx = tx
        self.ty = ty
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.fontSize = fontSize
        self.thickness = thickness
        self.text = ""

    def createRectangle(self, img, text=""):
        cv2.rectangle(img, (self.x,self.y), (self.x+self.w,self.y+self.h),self.bgColor, cv2.FILLED)
        cv2.putText(img, f'{text}', (self.x+self.tx,self.y+self.ty), cv2.FONT_HERSHEY_DUPLEX,
                    self.fontSize,self.fgColor, self.thickness)
    def updateFgColor(self,fgcolor):
        self.fgColor = fgcolor


class Game():
    def __init__(self):
        self.you_win = "You Win"
        self.you_loss = "You Loss"
        self.you_draw = "Draw"
        self.timeStart = time.time()
    def subX(self,point1, point2):
        return point1[0] - point2[0]
    def subY(self,point1, point2):
        return point1[1] - point2[1]

    def drawScissor(self,img, cursor):
        points = [8, 7, 6, 5, 9, 10, 11, 12]
        scissorColor = (170, 224, 130)
        # displayImage(img, scissor, spsx, spsy)
        for p in range(len(points) - 1):
            cv2.line(img, (cursor[points[p]][0], cursor[points[p]][1]),
                     (cursor[points[p + 1]][0], cursor[points[p + 1]][1]), scissorColor, 5)

    def drawPaper(self,img, cursor):
        points = [0, 1, 2, 3, 4, 3, 2, 5, 6, 7, 8, 7, 6, 5, 9, 10, 11, 12, 11, 10, 9, 13, 14, 15, 16, 15, 14, 13, 17,
                  18,
                  19, 20, 19, 18, 17, 0]
        paperColor = (233, 193, 133)
        # displayImage(img, paper, spsx, spsy)
        for p in range(len(points) - 1):
            cv2.line(img, (cursor[points[p]][0], cursor[points[p]][1]),
                     (cursor[points[p + 1]][0], cursor[points[p + 1]][1]),
                     paperColor, 5)

    def drawStone(self,img, cursor):
        points = [4, 3, 2, 5, 6, 7, 8, 7, 6, 5, 9, 10, 11, 12, 11, 10, 9, 13, 14, 15, 16, 15, 14, 13, 17, 18, 19, 20,
                  19,
                  18, 17]
        stoneColor = (0, 128, 255)
        # displayImage(img, stone, spsx, spsy)
        for p in range(len(points) - 1):
            cv2.line(img, (cursor[points[p]][0], cursor[points[p]][1]),
                     (cursor[points[p + 1]][0], cursor[points[p + 1]][1]),
                     stoneColor, 5)

    def detectObject(self,img,lmList):
        a1, a2, a3, a4 = lmList[8::4]
        b1, b2, b3, b4 = lmList[5::4]
        hx1, hy1 = lmList[3][:2]
        hx2, hy2 = lmList[17][:2]
        d1 = math.hypot(self.subX(a1, b1), self.subY(a1, b1))
        d2 = math.hypot(self.subX(a2, b2), self.subY(a2, b2))
        d3 = math.hypot(self.subX(a3, b3), self.subY(a3, b3))
        d4 = math.hypot(self.subX(a4, b4), self.subY(a4, b4))
        h = math.hypot(hx1 - hx2, hy1 - hy2)
        try:
            mean = ((d1 + d2 + d3 + d4) / 4) / h
        except ZeroDivisionError:
            mean = ((d1 + d2 + d3 + d4) / 4) / h+1
        if 0.20 < mean < 0.623:
            self.drawStone(img, lmList)
            return 1
        elif 0.63 < mean < 0.94:
            self.drawPaper(img, lmList)
            return 2
        elif mean > 1:
            self.drawScissor(img, lmList)
            return 3
        else:
            print(mean)
            return -1
    def detectFingerPrintArea(self,fingerPrint,bbox):
        bx, by, bw, bh = bbox
        if bx<fingerPrint.w and bx+bw < fingerPrint.w and fingerPrint.y<by<fingerPrint.h+fingerPrint.y\
                and fingerPrint.y<by+bh<fingerPrint.y+fingerPrint.h:
            fingerPrint.bgColor = (100,100,100)
            return True
        else:
            fingerPrint.bgColor = (255,255,255)
            return False
    def startTimer(self,cx,cy,stop=False):
        cv2.circle(img, (cx, cy), 30, (255, 255, 255), cv2.FILLED)
        if stop:
            cv2.putText(img, f'0', (cx - 10, cy + 10), cv2.FONT_HERSHEY_DUPLEX,
                        1, (0, 0, 0), 1)
            return 0
        else:
            cv2.putText(img, f'{int(totalTime - (time.time() - self.timeStart))}', (cx - 10, cy + 10),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1, (0, 0, 0), 1)
            return self.suffleImages()

    def displayImage(self,img, displayImg, x, y):
        desired_size = 64
        top, bottom, left, right = [10, 10, 10, 10]
        displayImg = cv2.copyMakeBorder(displayImg, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                        value=(255, 255, 255))
        img[x:x + desired_size + 20, y:y + desired_size + 20, :] = displayImg[:desired_size + 20, :desired_size + 20, :]

    def whoWin(self, userInput, systemInput):
        print(userInput, systemInput)
        if userInput == systemInput:
            return self.you_draw
        if userInput == 1 and systemInput == 2:  # stone and paper
            return self.you_loss
        else:
            return self.you_win

        if userInput == 2 and systemInput == 3:  # paper and scissor
            return self.you_loss
        else:
            return self.you_win

        if userInput == 3 and systemInput == 1:  # scissor and stone
            return self.you_loss
        else:
            return self.you_win
    def resultInfo(self,match):
        if match == self.you_win:
            return [(0,204,0)]
        elif match == self.you_loss:
            return [(0,0,255)]
        else:
            return [(255,0,0)]

    def suffleImages(self):
        val = rd.choice(objectType)
        if val == 1:
            self.displayImage(img, stone, spsx, spsy)
            return 1
        elif val == 2:
            self.displayImage(img, paper, spsx, spsy)
            return 2
        else:
            self.displayImage(img, scissor, spsx, spsy)
            return 3







# default values
objText = {"1": "Stone", "2": "Paper", "3": "Scissor", "-1": "Your Move"}
objImage = {"1":stone,"2":paper,"3":scissor}
obj = -1
spsy = 510
spsx = 150
timeX = 540
timerY = 310

game = Game()

spsText = Rect(x=0, y=50, w=170, h=70, tx=10, ty=40
                             , fgColor=(0, 0, 255), thickness=2,fontSize=0.8)

fingerPrint = Rect(x=0, y=120, w=170, h=250, tx=30, ty=40
                             , fgColor=(192, 192, 192), thickness=2)

timerAndImage = Rect(x=450, y=60, w=600, h=200, tx=30, ty=40
                             , fgColor=(0, 0, 255), thickness=2)
resultDisplay = Rect(x=450, y=400, w=600, h=70, tx=30, ty=40
                             , fgColor=(0, 0, 255), thickness=2)

playerObject = ""
playerImpression = []
systemObject = ""
while True:
    success, img = capture.read()
    img = cv2.flip(img, 1)
    hand = detector.findHands(img, draw=False)
    spsText.createRectangle(img,objText[str(obj)])
    fingerPrint.createRectangle(img)
    timerAndImage.createRectangle(img)
    game.displayImage(img,stone,spsx,spsy)
    if hand:
        lmList = hand[0]['lmList']
        obj = game.detectObject(img,lmList)
        isDetected = game.detectFingerPrintArea(fingerPrint,hand[0]['bbox'])
        if isDetected:
            if int(totalTime - (time.time() - game.timeStart)) < 0:
                print("game over")
                game.startTimer(540, 110,stop=True)
                print("system : ",objText[str(systemObject)])
                print("You : ",objText[str(playerObject)])
                playerObject = game.detectObject(img, playerImpression)
                spsText.createRectangle(img, objText[str(playerObject)])
                match = game.whoWin(userInput=playerObject,systemInput=systemObject)
                resultDisplay.createRectangle(img,match)
                resultDisplay.updateFgColor(game.resultInfo(match)[0])
                game.displayImage(img,objImage[str(systemObject)],spsx,spsy)
            else:
                playerObject = obj
                playerImpression = lmList
                systemObject = game.startTimer(timeX,timerY)  # return system object


        else:
            game.startTimer(timeX,timerY, stop=False)
            game.timeStart = time.time()
            if playerImpression and systemObject:
                playerObject = game.detectObject(img, playerImpression)
                spsText.createRectangle(img, objText[str(playerObject)])
                game.displayImage(img,objImage[str(systemObject)],spsx,spsy)
                match = game.whoWin(userInput=playerObject,systemInput=systemObject)
                resultDisplay.createRectangle(img,match)
                resultDisplay.updateFgColor(game.resultInfo(match)[0])


    else:
        game.displayImage(img,rd.choice([stone,paper,scissor]),spsx,spsy)
        game.timeStart = time.time()

    cv2.putText(img, f'AI Move', (490, 70 + 20), cv2.FONT_HERSHEY_DUPLEX,
                    1, (0, 128, 255), 2)

    cv2.imshow("Stone Paper Scissor Detector", img)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

if __name__ == "__main__":
    pass