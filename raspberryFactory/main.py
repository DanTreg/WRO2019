"""
Main
"""
import cv2
import numpy
from threading import Thread, Lock
from ListenerRobot import *
import ListenerRobot as ls
import time
import requests
import RPi.GPIO as GPIO
centerBall = None
#import paho.mqtt.client as mqtt
#client = mqtt.Client()
#client.connect("192.168.1.60",1883,60)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
dc = 0
GPIO.output(14, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
pwm.start(0)
pwm.ChangeDutyCycle(0)
response = requests.get("http://wro2019_api.therdteam.com/BallPlacesApi")
BallPlaces = response.json()
flagToStop = 1
def evaluateAvCollors(BallPlaces):
    arrToReturn = [] 
    for rows in BallPlaces:
        for place in rows:
            if place["Color"] != 0:
                arrToReturn.append(place["Color"])
    return(arrToReturn)
def checkCollor(arrOfColors, number):
    for color in arrOfColors:
        if color == number:
            return True
    return False

class DetectBall(Thread):
    def __init__(self):
        super(DetectBall, self).__init__()
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 640)
        self.camera.set(4, 480)
        self.const = True

        self.h_up_yellow = 255
        self.s_up_yellow = 255
        self.v_up_yellow = 255
        self.h_down_yellow=10
        self.s_down_yellow=220
        self.v_down_yellow=157
        
        self.h_up_white = 108
        self.s_up_white = 160
        self.v_up_white = 255
        self.h_down_white=0
        self.s_down_white=0
        self.v_down_white=144


        self.h_up_green = 128
        self.s_up_green = 255
        self.v_up_green = 255
        self.h_down_green=52
        self.s_down_green=97
        self.v_down_green=43
        
        self.h_up_blue = 255
        self.s_up_blue = 255
        self.v_up_blue = 255
        self.h_down_blue = 149
        self.s_down_blue = 157
        self.v_down_blue = 73
        
        self.h_up_red = 33
        self.s_up_red = 255
        self.v_up_red = 255
        self.h_down_red = 0
        self.s_down_red = 151
        self.v_down_red = 47
        
    def run(self):
        global centerBall
        global flagToStop
        while (self.const):
            kk = 0
            while kk < 3:
                ret, frame = self.camera.read()
                kk += 1
            frame = cv2.flip(frame, +1)
            
            FRAME_CROPPED=frame[260:640, 200:540]
            FRAME_CROPPED = cv2.GaussianBlur(FRAME_CROPPED, (5, 5), 2)
            self.hsv_min_yellow = numpy.array([self.h_down_yellow,self.s_down_yellow, self.v_down_yellow])
            self.hsv_max_yellow = numpy.array([self.h_up_yellow,self.s_up_yellow,self.v_up_yellow])
            self.hsv_min_green = numpy.array([self.h_down_green, self.s_down_green, self.v_down_green])
            self.hsv_max_green = numpy.array([self.h_up_green, self.s_up_green, self.v_up_green])
            self.hsv_min_blue = numpy.array([self.h_down_blue, self.s_down_blue, self.v_down_blue])
            self.hsv_max_blue = numpy.array([self.h_up_blue, self.s_up_blue, self.v_up_blue])
            self.hsv_min_red = numpy.array([self.h_down_red, self.s_down_red, self.v_down_red])
            self.hsv_max_red = numpy.array([self.h_up_red, self.s_up_red, self.v_up_red])
            self.hsv_min_white = numpy.array([self.h_down_white, self.s_down_white, self.v_down_white])
            self.hsv_max_white = numpy.array([self.h_up_white, self.s_up_white, self.v_up_white])
            frame_to_thresh = cv2.cvtColor(FRAME_CROPPED, cv2.COLOR_BGR2HSV_FULL)
            for number in [1, 2, 3, 4, 5]:
                arrOfColors = evaluateAvCollors(BallPlaces)
                
                boolCheckCollor = checkCollor(arrOfColors, number)
                print(str(arrOfColors))
                if len(arrOfColors) == 0:
                    flagToStop = 1 
                    continue
                if boolCheckCollor == False:
                    continue
                if number == 1 and boolCheckCollor == True:
                    self.mask = cv2.inRange(frame_to_thresh, self.hsv_min_red, self.hsv_max_red)
                    print("red")
                if number == 2 and boolCheckCollor == True:
                    self.mask = cv2.inRange(frame_to_thresh, self.hsv_min_white, self.hsv_max_white)
                    print("white")
                if number == 3 and boolCheckCollor == True:
                    self.mask = cv2.inRange(frame_to_thresh, self.hsv_min_yellow, self.hsv_max_yellow)
                    print("yellow")
                if number == 4 and boolCheckCollor == True:
                    self.mask = cv2.inRange(frame_to_thresh, self.hsv_min_green, self.hsv_max_green)
                    print("green")
                if number == 5 and boolCheckCollor == True:
                    print("blueeeeee")
                    self.mask = cv2.inRange(frame_to_thresh, self.hsv_min_blue, self.hsv_max_blue)

                _, self.cnts, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                
                cv2.imshow("cnts", self.mask)
                if number == 5:
                    print(str(len(self.cnts)))
                for cnt in self.cnts:
                    if len(cnt) > 100:
                        cntsArea = cv2.contourArea(cnt)
                        rect2 = cv2.minAreaRect(cnt) 
                        box = cv2.boxPoints(rect2)
                        box = numpy.int0(box)
                        if number == 1:
                            cv2.drawContours(FRAME_CROPPED, [box], 0, (0, 0, 255), 2)
                        if number == 2:
                            cv2.drawContours(FRAME_CROPPED, [box], 0, (255, 255, 255), 2)
                        if number == 3:
                            cv2.drawContours(FRAME_CROPPED, [box], 0, (0, 204, 255), 2)
                        if number == 4:
                            cv2.drawContours(FRAME_CROPPED, [box], 0, (0, 255, 0), 2)
                        if number == 5:
                            cv2.drawContours(FRAME_CROPPED, [box], 0, (255, 0, 0), 2)
                            print("blue")
                        centerBall = [int(rect2[0][0]),(int(rect2[0][1])), number]
                        cv2.circle(FRAME_CROPPED, (centerBall[0], centerBall[1]), 10, (0, 0, 255), -1)
            cv2.imshow("original", FRAME_CROPPED)
            if cv2.waitKey(1) == 27:
                self.stop()

    def stop(self):
        self.const = False
        
def evaluatePlace(centerBall, BallPlaces):
    enum = {
        "0": 1,
        "2": 2,
        "4": 3,
        "6": 4,
        "8": 5
    }
    
    print(BallPlaces)
    for rows in BallPlaces:
        for place in rows:
            if place["Color"] == centerBall[2]:
                placeRaw = place["Place"]
                place["Color"] = 0
                return(enum[str(placeRaw)], BallPlaces)


def left():
    pwm.ChangeDutyCycle(45 / 10.0 + 2.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)


def right():
    pwm.ChangeDutyCycle(15 / 10.0 + 2.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
def turnMotorOn():
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.HIGH)
def turnMotorOff():
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
try:
    client = mqtt.Client()
    client.connect("192.168.100.59", 1883, 1000)
    TrackBall = DetectBall()
    TrackBall.start()
    time.sleep(1)
    left()
    SubscribeEv3 = ls.ListenEV3("ListenToEv3")
    SubscribeEv3.start()
    oldMsgfromEv3 = ''
    
    print("started")
    while True:
        if flagToStop == 1:
            if ls.msgFromEV3 == "newModel":
                flagToStop = 0
                response = requests.get("http://wro2019_api.therdteam.com/BallPlacesApi")
                BallPlaces = response.json()
            if ls.msgFromEV3 == "realeaseBall":
                turnMotorOff()
                left()
                oldMsgfromEv3 = ls.msgFromEV3
                ls.msgFromEV3 = ""
            if ls.msgFromEV3 == "takeBall":
                print("takeBall")

                right()
                turnMotorOn()
                time.sleep(5)
                oldMsgfromEv3 = ls.msgFromEV3
                ls.msgFromEV3 = ""
            continue
        if ls.msgFromEV3 == "start" and ls.msgFromEV3 != oldMsgfromEv3:
            print(str(centerBall), str(BallPlaces))
            place, BallPlaces = evaluatePlace(centerBall, BallPlaces)
            print(str(BallPlaces), str(place))
            client.publish("CamToEv3", str(centerBall[0]) + "," + str(centerBall[1]) + "," + str(place))
            print(str(centerBall[0]) , "," , str(centerBall[1]) , "," , str(place))
            print("it also works")
            print(ls.msgFromEV3)
            oldMsgfromEv3 = ls.msgFromEV3
            print(oldMsgfromEv3)
            ls.msgFromEV3 = ""
        if ls.msgFromEV3 == "takeBall":
            print("takeBall")
            
            right()
            turnMotorOn()
            time.sleep(5)
            oldMsgfromEv3 = ls.msgFromEV3
            ls.msgFromEV3 = ""
        if ls.msgFromEV3 == "realeaseBall":
            turnMotorOff()
            left()
            oldMsgfromEv3 = ls.msgFromEV3
            ls.msgFromEV3 = ""
        time.sleep(1)
finally:
    TrackBall.stop()
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    listener_ev3.disconnect()
    client.disconnect()
    cv2.destroyAllWindows()
    pwm.stop()
    GPIO.cleanup()
