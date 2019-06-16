import serial
import time
import requests
from ListenerRobot import *
import ListenerRobot as ls
ser1 = serial.Serial('/dev/ttyUSB1', 9600)
ser2 = serial.Serial('/dev/ttyUSB0', 9600)
ser1.flushInput()
ser2.flushInput()
def openServo(whichToOpen, BallPlaces):
    if whichToOpen == 2:
        print(str(BallPlaces))
        if BallPlaces["blue"] != 0:
            i = 0
            print(str(BallPlaces["blue"]))
            while BallPlaces["blue"] > i:
                ser2.write(b'1\n')
                time.sleep(0.5)
                i += 1
        if BallPlaces["yellow"] != 0:
            i = 0
            print(str(BallPlaces["yellow"]))
            while BallPlaces["yellow"] > i:
                ser2.write(b'2\n')
                time.sleep(0.5)
                i += 1
        if BallPlaces["white"] != 0:
            i = 0
            print(str(BallPlaces["white"]))
            while BallPlaces["white"] >  i:
                ser2.write(b'3\n')
                time.sleep(0.5)
                i += 1
    if whichToOpen == 1:
        print(str(BallPlaces))
        if BallPlaces["red"] != 0:
            i = 0
            print(str(BallPlaces["red"]))
            while BallPlaces["red"] > i:
                ser1.write(b'1\n')
                time.sleep(0.5)
                i += 1
        if BallPlaces["green"] != 0:
            i = 0
            print(str(BallPlaces["green"]))
            while BallPlaces["green"] > i:
                ser1.write(b'2\n')
                time.sleep(0.5)
                i += 1
        if BallPlaces["white"] != 0:
            i = 0
            print(str(BallPlaces["white"]))
            while BallPlaces["white"] > i:
                ser1.write(b'3\n')
                time.sleep(0.5)
                i += 1

def convertModel(BallPlaces):
    manufacturerOne = None
    manufacturerTwo = None
    for place in BallPlaces:
        if place['manufacturerID'] == 1:
            manufacturerOne = place
        if place['manufacturerID'] == 2:
            manufacturerTwo = place
    return(manufacturerOne, manufacturerTwo)
def fetchApi():
    response = requests.get(
                "http://wro2019_api.therdteam.com/getBallForCars")
    BallPlaces = response.json()
    return BallPlaces
try:
    
    SubscribeEv3 = ls.ListenEV3("ListenToEv3")
    SubscribeEv3.start()
    SubscribeEv4 = ls.ListenEV4("ListenEv4")
    SubscribeEv4.start()
    client = mqtt.Client()
    client.connect("192.168.100.59", 1883, 1000)
    while True:
        if ls.msgFromEV3 == "open1" or ls.msgFromEV4 == 'open1':
            BallPlaces = fetchApi()
            print(str(BallPlaces))
            manufacturerOne, manufacturerTwo = convertModel(BallPlaces)
            openServo(1, manufacturerOne)
            if ls.msgFromEV4 != '':
                client.publish("supToRoadController2", 'go1')
                print("supToRoadController2", 'go1')
                ls.msgFromEV4 = ''
            if ls.msgFromEV3 != '':
                client.publish("supToRoadController1", 'go1')
                print("supToRoadController1", 'go1')
                ls.msgFromEV3 = ''
        if ls.msgFromEV3 == "open2" or ls.msgFromEV4 == 'open2':
            BallPlaces = fetchApi()
            print(str(BallPlaces))
            manufacturerOne, manufacturerTwo = convertModel(BallPlaces)
            openServo(2, manufacturerTwo)
            if ls.msgFromEV4 != '':
                client.publish("supToRoadController2", 'go2')
                print("supToRoadController2", 'go2')
                ls.msgFromEV4 = ''
            if ls.msgFromEV3 != '':
                client.publish("supToRoadController1", 'go2')
                print("supToRoadController1", 'go2')
                ls.msgFromEV3 = ''
finally:
    ser1.close()
    ser2.close()
    listener_ev4.disconnect()
    listener_ev3.disconnect()
    client.disconnect()
