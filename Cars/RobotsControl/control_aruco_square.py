import cv2.aruco as aruco
import math
from shapedetector import ShapeDetector
import cv2  # библиотека opencv
import numpy  # работа с массивамиpip3 install paho-mqtt
import paho.mqtt.client as mqtt
import time
from threading import Thread
import socket
import sys
import json
import requests
import random

flag_4 = 0
flag_3 = 0
flag_j = 0
flag_t = 0
flag_z = 0
flag_square = 0

#urlJson = 'http://192.168.100.35/getBallForCars?v='
urlJson = 'http://wro2019_api.therdteam.com/getBallForCars?v='

old_model = ''
new_model = ''
ev3_done = ''
ev4_done = ''
msgFromEv3 = ''
msgFromEv4 = ''
ip_to_connect = '192.168.100.56'

class ListenApi(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        print("client is created")

    def run(self):
        global new_model
        while True:
            a = random.randint(1, 9)
            a = str(a)
            url = urlJson + a
            print(a)
            print(url)
            response = requests.get(url)
            json_get = response.json()
            p1 = []
            p2 = []
            data = json_get
            data = json.dumps(data)

            data = json.loads(data)

            k0 = data[0].keys()
            for key in k0:
                p2.append(data[0][key])
            k1 = data[1].keys()
            for key in k1:
                p1.append(data[1][key])
            new_model = p1, p2
            #print(new_model)
            #print(p1)
            #print(p2)
            #print("api_thread start")

class ListenEV3(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_ev3.connect(ip_to_connect, 1883, 60) #connect
        listener_ev3.on_connect = self.on_connect
        listener_ev3.on_message = self.on_message
        print("client is created")

    def run(self):
        print("pc_thread start")
        listener_ev3.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_ev3.subscribe("ev3/to/pc")
        print("I am listening to car")

    def on_message(self, client, userdata, msg):
        global msgFromEv3
        msgFromEv3 = msg.payload.decode()
        print("ev3 says: " + msgFromEv3)
        # print(msgFromEv3)


class ListenEV4(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_ev4.connect(ip_to_connect, 1883, 60) #connect
        listener_ev4.on_connect = self.on_connect
        listener_ev4.on_message = self.on_message
        print("client is created")

    def run(self):
        print("pc_thread start")
        listener_ev4.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_ev4.subscribe("ev4/to/pc")
        print("I am listening to car")

    def on_message(self, client, userdata, msg):
        global msgFromEv4
        msgFromEv4 = msg.payload.decode()
        print("ev4 says: " + msgFromEv4)
        # print(msgFromEv4)



def get_json(urlJson):
    response = requests.get(urlJson)
    # print(response)
    json_get = response.json()
    return json_get
    # print(json_get)


def parse_json(p1, p2):
    p1 = []
    p2 = []
    data = get_json(urlJson)
    #print(data)
    data = json.dumps(data)
    # data = json.loads(json_str)

    data = json.loads(data)
    #print(data)
    #print(data[0])
    #print(data[1])

    k0 = data[0].keys()
    for key in k0:
        p2.append(data[0][key])
    k1 = data[1].keys()
    for key in k1:
        p1.append(data[1][key])
    print(p1)
    print(p2)
    return p1, p2


def alfa(x1, y1, x2, y2):
    try:
        s1 = math.fabs(x1 - x2)
        s2 = math.fabs(y1 - y2)
        c = s1 / s2
        a_radian = math.atan(c)
        a = math.degrees(a_radian)

        if x1 >= x2 and y1 > y2:
            betta = a

            return betta
        if x1 >= x2 and y1 < y2:
            betta = 180 - a

            return betta
            # return a+90
        if x1 < x2 and y1 < y2:
            betta = 180 + a

            return betta
        if x1 < x2 and y1 > y2:
            betta = 360 - a

            return betta

    except ZeroDivisionError:
        if x1 > x2:
            return -90
        if x1 < x2:
            return 90


def znak(alfa):
    alfa = int(alfa)
    if alfa > 180:
        alfa = -360 + alfa
    if alfa <= 180:
        alfa = alfa
    return alfa


def povorot(topic, x1, y1, x2, y2):
    if alfa(x1, y1, x2, y2) > 8 or alfa(x1, y1, x2, y2) < 352:
        client.publish(topic, str(round(-(znak(alfa(x1, y1, x2, y2))))) + ',' + '0')
    if alfa(x1, y1, x2, y2) <= 8 or alfa(x1, y1, x2, y2) >= 352:
        print('alfa(x1, y1, x2, y2) <= 5 or alfa(x1, y1, x2, y2) >= 355')


def move_to_point(x1, y1, x2, y2, topic):
    client.publish(topic, str(round((move_alfa(x1, y1, x2, y2)))) + ',' + str(round(math.hypot(x2 - x1, y2 - y1))))


def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def distance_to_p(xR1, yR1, xR2, yR2, xP1, yP1, xP2, yP2, x_proizv, y_proizv):
    p1 = 'p1'
    p2 = 'p2'

    r1_to_p1 = distance(xR1, yR1, xP1, yP1) + distance(xP1, yP1, x_proizv, y_proizv)
    r1_to_p2 = distance(xR1, yR1, xP2, yP2) + distance(xP2, yP2, x_proizv, y_proizv)
    r2_to_p1 = distance(xR2, yR2, xP1, yP1) + distance(xP1, yP1, x_proizv, y_proizv)
    r2_to_p2 = distance(xR2, yR2, xP2, yP2) + distance(xP2, yP2, x_proizv, y_proizv)
    print(r1_to_p1, r1_to_p2, r2_to_p1, r2_to_p2)
    if r1_to_p1 < r1_to_p2 and r1_to_p1 < r2_to_p1:
        return p1, p2
    if r2_to_p1 < r2_to_p2 and r2_to_p1 < r1_to_p1:
        return p2, p1
    if r1_to_p2 < r1_to_p1 and r1_to_p2 < r2_to_p2:
        return p2, p1
    if r2_to_p2 < r2_to_p1 and r2_to_p2 < r1_to_p2:
        return p1, p2
    if r1_to_p1 == r1_to_p2 and r2_to_p1 < r1_to_p1 and r2_to_p1 < r2_to_p2:
        return p2, p1
    if r1_to_p1 == r1_to_p2 and r2_to_p2 < r1_to_p2 and r2_to_p2 < r2_to_p1:
        return p1, p2
    if r2_to_p1 == r2_to_p2 and r1_to_p1 < r2_to_p1 and r1_to_p1 < r1_to_p2:
        return p1, p2
    if r2_to_p1 == r2_to_p2 and r1_to_p2 < r2_to_p2 and r1_to_p2 < r1_to_p1:
        return p2, p1
    if r1_to_p1 == r1_to_p2 and r1_to_p1 < r2_to_p1 and r1_to_p2 < r2_to_p2 and r2_to_p1 < r2_to_p2:
        return p2, p1
    if r1_to_p1 == r1_to_p2 and r1_to_p1 < r2_to_p1 and r1_to_p2 < r2_to_p2 and r2_to_p2 < r2_to_p1:
        return p1, p2
    if r2_to_p1 == r2_to_p2 and r2_to_p1 < r1_to_p1 and r2_to_p2 < r1_to_p2 and r1_to_p1 < r1_to_p2:
        return p1, p2
    if r2_to_p1 == r2_to_p2 and r2_to_p1 < r1_to_p1 and r2_to_p2 < r1_to_p2 and r1_to_p2 < r1_to_p1:
        return p2, p1


def move_alfa(x1, y1, x2, y2):
    try:
        s1 = math.fabs(x1 - x2)
        s2 = math.fabs(y1 - y2)
        c = s1 / s2
        a_radian = math.atan(c)
        a = math.degrees(a_radian)
        if x1 >= x2 and y1 > y2:
            # betta = a + 90
            betta = a + 270
            print('x1 > x2 and y1 > y2 (4)', a, betta)
            return betta
        if x1 >= x2 and y1 < y2:
            # betta = 180 + (90-a)
            betta = 90 - a
            print('x1 >= x2 and y1 < y2 (1)', a, betta)
            return betta
        if x1 < x2 and y1 < y2:
            betta = a + 90
            # betta = a + 270
            print('x1 < x2 and y1 < y2 (2)', a, betta)
            return betta
        if x1 < x2 and y1 > y2:
            # betta = 90-a
            betta = 180 + (90 - a)
            print('x1 < x2 and y1 > y2 (3)', a, betta)
            return betta
    except ZeroDivisionError:
        if x1 > x2:
            return 0
        if x1 < x2:
            return 180


def move(x1, y1, x2, y2, x3, y3, center_x, center_y, topic, msg, flag, dist):
    print(msg)
    if alfa(x1, y1, x2, y2) > 6 and alfa(x1, y1, x2, y2) < 354 and flag == 0:
        povorot(topic, x1, y1, x2, y2)
        msg = ''
        flag = 1

    if alfa(x1, y1, x2, y2) <= 6 or alfa(x1, y1, x2, y2) >= 354:
        flag = 0
    if msg == 'ok':
        print('msg', msg)
        print("msg = ok")
        flag = 0
    print('flag', flag)
    if alfa(x1, y1, x2, y2) <= 6 or alfa(x1, y1, x2, y2) >= 354:

        if center_x > x3 + dist or center_x < x3 - dist or center_y > y3 + dist or center_y < y3 - dist:
            cv2.line(frame, (center_x, center_y), (x3, y3), (0, 255, 0), 2)
            move_to_point(center_x, center_y, x3, y3, topic)
        else:
            print('0,0')
            client.publish(topic, '0,0')

#url_post_first = 'http://192.168.100.35/createTranspContract'
url_post_first = 'http://wro2019_api.therdteam.com/createTranspContract'
listener_ev3 = mqtt.Client()
listener_ev4 = mqtt.Client()
client = mqtt.Client()

p1 = []
p2 = []
topic_ev3 = "pc/to/ev3"
topic_ev4 = "pc/to/ev4"

client.connect(ip_to_connect, 1883, 1000)
ev3_thread = ListenEV3("Listen to EV3")
ev3_thread.start()
ev4_thread = ListenEV4("Listen to EV4")
ev4_thread.start()
api_thread = ListenApi("Listen to API")
api_thread.start()

xP1 = 90
yP1 = 330
xP2 = 320
yP2 = 330
x_proizv = 150
y_proizv = 30
afk_zone_x1 = 90
afk_zone_y1 = 330
afk_zone_x2 = 320
afk_zone_y2 = 330
wait_zone_x1 = 90
wait_zone_y1 = 330
wait_zone_x2 = 320
wait_zone_y2 = 330
wait_zone_x3 = 330
wait_zone_y3 = 50
wait_zone_x4 = 60
wait_zone_y4 = 50


sd = ShapeDetector()

font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_CONTRAST, -950)
# cap.set(11, 0.1)

new_model = parse_json(p1, p2)
old_model = new_model
print(new_model)
print(type(new_model))
print(old_model)
print(type(old_model))

while True:

    _, frame = cap.read()
    frame = frame[80:560, 100:480]
    aruco_dictionary = aruco.Dictionary_get(aruco.DICT_4X4_250)

    #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    corner, id, false_points = aruco.detectMarkers(frame, aruco_dictionary)
    print(id)
    cv2.circle(frame, (xP1, yP1), 3, (255, 0, 0), -1)
    cv2.circle(frame, (xP2, yP2), 3, (255, 0, 0), -1)
    cv2.circle(frame, (x_proizv, y_proizv), 3, (255, 0, 0), -1)

    if numpy.all(id) != None:
        aruco.drawDetectedMarkers(frame, corner)

        if len(id) == 2:
            print('len(id) == 2')

            if 7 in id:
            #if 4 in id:
                #i, _ = numpy.where(id == 4)
                i, _ = numpy.where(id == 7)
                i = int(i)
                #print(i)
                marker_points = corner[i][0]
                # marker_points = corner[0][0]
                x1_4, y1_4 = int(marker_points[0][0]), int(marker_points[0][1])
                x2_4, y2_4 = int(marker_points[1][0]), int(marker_points[1][1])
                x3_4, y3_4 = int(marker_points[2][0]), int(marker_points[2][1])
                #x4_4, y4_4 = int(marker_points[3][0]), int(marker_points[3][1])
                center_x_4 = round((x1_4 + x3_4) / 2)
                center_y_4 = round((y1_4 + y3_4) / 2)
                cv2.putText(frame, "7", (center_x_4, center_y_4), font, 1, (0,255,0), 2, cv2.LINE_AA)
                cv2.circle(frame, (center_x_4, center_y_4), 3, (0, 0, 255), -1)
                cv2.circle(frame, (x1_4, y1_4), 5, (0, 0, 0), -1)
                cv2.circle(frame, (x2_4, y2_4), 5, (0, 0, 0), -1)
                angle = znak(alfa(x1_4, y1_4, x2_4, y2_4))


                aruco.drawDetectedMarkers(frame, [corner[i]])

            if 5 in id:

                j, _ = numpy.where(id == 5)
                j = int(j)
                #print(j)
                marker_points = corner[j][0]
                x1_3, y1_3 = int(marker_points[0][0]), int(marker_points[0][1])
                x2_3, y2_3 = int(marker_points[1][0]), int(marker_points[1][1])
                x3_3, y3_3 = int(marker_points[2][0]), int(marker_points[2][1])
                center_x_3 = round((x1_3 + x3_3) / 2)
                center_y_3 = round((y1_3 + y3_3) / 2)
                cv2.putText(frame, "5", (center_x_3, center_y_3), font, 1, (0,255,0), 2, cv2.LINE_AA)
                cv2.circle(frame, (center_x_3, center_y_3), 3, (0, 255, 0), -1)
                cv2.circle(frame, (x1_3, y1_3), 5, (255, 255, 255), -1)
                cv2.circle(frame, (x2_3, y2_3), 5, (255, 255, 255), -1)
                angle = znak(alfa(x1_3, y1_3, x2_3, y2_3))

                aruco.drawDetectedMarkers(frame, [corner[j]])

                #ew_model = parse_json(p1, p2)
                print(new_model)
                print(old_model)
                print('msgFromEV3', msgFromEv3)
                print('msgFromEV4', msgFromEv4)
                if new_model == old_model and new_model != '' and old_model != '':

                    if flag_square == 0:

                        client.publish(topic_ev3, 'start')
                        client.publish(topic_ev4, 'start')
                        time.sleep(3)
                        print(new_model)
                        print(old_model)
                        client.publish(topic_ev3, 'square')
                        client.publish(topic_ev4, 'square')
                        time.sleep(3)

                        if center_x_3 >= center_x_4:

                            client.publish(topic_ev3, 'sp2')
                            client.publish(topic_ev4, 'sp1')
                            flag_square = 1

                        if center_x_4 > center_x_3:

                            client.publish(topic_ev3, 'sp1')
                            client.publish(topic_ev4, 'sp2')
                            flag_square = 1

                    cv2.circle(frame, (wait_zone_x1, wait_zone_y1), 3, (0, 0, 255), -1)
                    cv2.circle(frame, (wait_zone_x2, wait_zone_y2), 3, (0, 255, 255), -1)
                    cv2.circle(frame, (wait_zone_x3, wait_zone_y3), 3, (255, 0, 255), -1)
                    cv2.circle(frame, (wait_zone_x4, wait_zone_y4), 3, (0, 0, 0), -1)

                    if msgFromEv3 == 'wait_zone1':
                        move(x1_3, y1_3, x2_3, y2_3, wait_zone_x1, wait_zone_y1, center_x_3, center_y_3, topic_ev3,
                             msgFromEv3, flag_3, 20)

                    if msgFromEv3 == 'wait_zone2':
                        move(x1_3, y1_3, x2_3, y2_3, wait_zone_x2, wait_zone_y2, center_x_3, center_y_3, topic_ev3,
                             msgFromEv3, flag_3, 20)

                    if msgFromEv3 == 'wait_zone3':
                        move(x1_3, y1_3, x2_3, y2_3, wait_zone_x3, wait_zone_y3, center_x_3, center_y_3, topic_ev3,
                             msgFromEv3, flag_3, 20)

                    if msgFromEv3 == 'wait_zone4':
                        move(x1_3, y1_3, x2_3, y2_3, wait_zone_x4, wait_zone_y4, center_x_3, center_y_3, topic_ev3,
                             msgFromEv3, flag_3, 20)

                    if msgFromEv4 == 'wait_zone1':
                        move(x1_4, y1_4, x2_4, y2_4, wait_zone_x1, wait_zone_y1, center_x_4, center_y_4, topic_ev4,
                             msgFromEv4, flag_4, 20)

                    if msgFromEv4 == 'wait_zone2':
                        move(x1_4, y1_4, x2_4, y2_4, wait_zone_x2, wait_zone_y2, center_x_4, center_y_4, topic_ev4,
                             msgFromEv4, flag_4, 20)

                    if msgFromEv4 == 'wait_zone3':
                        move(x1_4, y1_4, x2_4, y2_4, wait_zone_x3, wait_zone_y3, center_x_4, center_y_4, topic_ev4,
                             msgFromEv4, flag_4, 20)

                    if msgFromEv4 == 'wait_zone4':
                        move(x1_4, y1_4, x2_4, y2_4, wait_zone_x4, wait_zone_y4, center_x_4, center_y_4, topic_ev4,
                             msgFromEv4, flag_4, 20)

                    if msgFromEv3 == 'ok':
                        print("msgfromEv3 ok")
                        flag_3 = 0

                    if msgFromEv4 == 'ok':
                        print("msgfromEv4 ok")
                        flag_4 = 0

                if old_model != new_model and new_model != '' and old_model != '':

                    if msgFromEv3 == 'ok':
                        print("msgfromEv3 ok")
                        flag_3 = 0

                    if msgFromEv4 == 'ok':
                        print("msgfromEv4 ok")
                        flag_4 = 0

                    if flag_j == 0:
                        while msgFromEv3 != '1000' or msgFromEv4 != '1000':
                            client.publish(topic_ev3, '1000,1000')
                            client.publish(topic_ev4, '1000,1000')
                            print(msgFromEv4)
                            print(msgFromEv3)
                            time.sleep(1)
                        time.sleep(2)
                        #client.publish(topic_ev3, 'start')
                        #client.publish(topic_ev4, 'start')
                        #while msgFromEv3 != '1000' or msgFromEv4 != '1000':
                        #    client.publish(topic_ev3, '1000,1000')
                        #    client.publish(topic_ev4, '1000,1000')
                        #    print(msgFromEv4)
                        #    print(msgFromEv3)
                        #    time.sleep(1)
                        p1, p2 = parse_json(p1, p2)
                        s1 = p1[1] + p1[2] + p1[3] + p1[4] + p1[5]
                        s2 = p2[1] + p2[2] + p2[3] + p2[4] + p2[5]

                        dist_to_p = distance_to_p(center_x_3, center_y_3, center_x_4, center_y_4, xP1, yP1, xP2, yP2,
                                                  x_proizv, y_proizv)

                        print(dist_to_p)

                        if dist_to_p[0] == 'p1' and s1 != 0 and s2 != 0:
                            print('dist_to_p[0] == p1')
                            client.publish(topic_ev3, 'p1')
                            client.publish(topic_ev4, 'p2')
                            flag_j = 1

                        if dist_to_p[0] == 'p2' and s1 != 0 and s2 != 0:
                            print('dist_to_p[0] == p2')
                            client.publish(topic_ev3, 'p2')
                            client.publish(topic_ev4, 'p1')
                            flag_j = 1

                        if dist_to_p[0] == 'p1'and s1 == 0:
                            client.publish(topic_ev3, 'done_p1')
                            client.publish(topic_ev4, 'p2')
                            flag_j = 1

                        if dist_to_p[0] == 'p2' and s2 == 0:
                            client.publish(topic_ev3, 'done_p2')
                            client.publish(topic_ev4, 'p1')
                            flag_j = 1

                        if dist_to_p[0] == 'p1' and s2 == 0:
                            client.publish(topic_ev3, 'p1')
                            client.publish(topic_ev4, 'done_p2')
                            flag_j = 1

                        if dist_to_p[0] == 'p2' and s1 == 0:
                            client.publish(topic_ev3, 'p2')
                            client.publish(topic_ev4, 'done_p1')
                            flag_j = 1

                    if msgFromEv4 == 'first,ev4,p1' and msgFromEv3 != 'first,ev3,p1' and msgFromEv3 != 'first,ev3,p2' and flag_t == 0:
                        json_to_post_ev4 = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":1,
                                                "ManufacturerID":0
                                            },
                                            "isManufContract":0
                                        }
                        json_to_post_ev3 = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":0,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":0
                                        }
                        requests.post(url_post_first, json=json_to_post_ev4)
                        requests.post(url_post_first, json=json_to_post_ev3)
                        flag_t = 1
                    if msgFromEv4 == 'first,ev4,p2' and msgFromEv3 != 'first,ev3,p1' and msgFromEv3 != 'first,ev3,p2' and flag_t == 0:
                        print('msgFromEv4 == first,ev4,p2 and msgFromEv3 != first,ev3,p1 and msgFromEv3 != first,ev3,p2')
                        json_to_post_ev4 = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":1,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":0
                                        }
                        json_to_post_ev3 = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":0,
                                                "ManufacturerID":0
                                            },
                                            "isManufContract":0
                                        }
                        requests.post(url_post_first, json=json_to_post_ev4)
                        requests.post(url_post_first, json=json_to_post_ev3)

                    if msgFromEv3 == 'first,ev3,p1' and msgFromEv4 != 'first,ev4,p1' and msgFromEv4 != 'first,ev4,p2' and flag_t == 0:
                        print('msgFromEv3 == first,ev3,p1 and msgFromEv4 != first,ev4,p1 and msgFromEv4 != first,ev4,p2')
                        json_to_post_ev4 = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":1,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":0
                                        }
                        json_to_post_ev3 = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":0,
                                                "ManufacturerID":0
                                            },
                                            "isManufContract":0
                                        }
                        requests.post(url_post_first, json=json_to_post_ev3)
                        requests.post(url_post_first, json=json_to_post_ev4)
                        flag_t = 1
                    if msgFromEv3 == 'first,ev3,p2' and msgFromEv4 != 'first,ev4,p1' and msgFromEv4 != 'first,ev4,p2' and flag_t == 0:
                        print('msgFromEv3 == first,ev3,p2 and msgFromEv4 != first,ev4,p1 and msgFromEv4 != first,ev4,p2')
                        json_to_post_ev4 = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":1,
                                                "ManufacturerID":0
                                            },
                                            "isManufContract":0
                                        }
                        json_to_post_ev3 = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":0,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":0
                                        }
                        requests.post(url_post_first, json=json_to_post_ev3)
                        requests.post(url_post_first, json=json_to_post_ev4)
                        flag_t = 1
                    if msgFromEv4 == 'first,ev4,p1,zav' and msgFromEv3 != 'first,ev3,p1,zav' and msgFromEv3 != 'first,ev3,p2,zav' and flag_z == 0:
                        print('msgFromEv4 == first,ev4,p1,zav and msgFromEv3 != first,ev3,p1,zav and msgFromEv3 != first,ev3,p2,zav')
                        json_to_post_ev4_zav = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":1,
                                                "ManufacturerID":0
                                            },
                                            "isManufContract":1
                                        }
                        json_to_post_ev3_zav = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":0,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":1
                                        }
                        requests.post(url_post_first, json=json_to_post_ev4_zav)
                        requests.post(url_post_first, json=json_to_post_ev3_zav)
                        flag_z = 1
                    if msgFromEv4 == 'first,ev4,p2,zav' and msgFromEv3 != 'first,ev3,p1,zav' and msgFromEv3 != 'first,ev3,p2,zav' and flag_z == 0:
                        print('msgFromEv4 == first,ev4,p2,zav and msgFromEv3 != first,ev3,p1,zav and msgFromEv3 != first,ev3,p2,zav')
                        json_to_post_ev4_zav = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":1,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":1
                                        }
                        json_to_post_ev3_zav = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":0,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":0
                                        }
                        requests.post(url_post_first, json=json_to_post_ev4_zav)
                        requests.post(url_post_first, json=json_to_post_ev3_zav)
                        flag_z = 1
                    if msgFromEv3 == 'first,ev3,p1,zav' and msgFromEv4 != 'first,ev4,p1,zav' and msgFromEv4 != 'first,ev4,p2,zav' and flag_z == 0:
                        print('msgFromEv3 == first,ev3,p1,zav and msgFromEv4 != first,ev4,p1,zav and msgFromEv4 != first,ev4,p2,zav')
                        json_to_post_ev4_zav = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":1,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":1
                                        }
                        json_to_post_ev3_zav = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":0,
                                                "ManufacturerID":0
                                            },
                                            "isManufContract":1
                                        }
                        requests.post(url_post_first, json=json_to_post_ev3_zav)
                        requests.post(url_post_first, json=json_to_post_ev4_zav)
                        flag_z = 1
                    if msgFromEv3 == 'first,ev3,p2,zav' and msgFromEv4 != 'first,ev4,p1,zav' and msgFromEv4 != 'first,ev4,p2,zav' and flag_z == 0:
                        print('msgFromEv3 == first,ev3,p2,zav and msgFromEv4 != first,ev4,p1,zav and msgFromEv4 != first,ev4,p2,zav')
                        json_to_post_ev4_zav = {
                                            "transpContract":{
                                                "fastDelievery":0,
                                                "RobotID":1,
                                                "ManufacturerID":0
                                            },
                                            "isManufContract":1
                                        }
                        json_to_post_ev3_zav = {
                                            "transpContract":{
                                                "fastDelievery":1,
                                                "RobotID":0,
                                                "ManufacturerID":1
                                            },
                                            "isManufContract":1
                                        }
                        requests.post(url_post_first, json=json_to_post_ev3_zav)
                        requests.post(url_post_first, json=json_to_post_ev4_zav)
                        flag_z = 1

                    if msgFromEv3 == 'p':
                        print('msgFromEv3 = p')

                        if dist_to_p[0] == 'p1':
                            print('msgFromEv3', msgFromEv3)
                            move(x1_3, y1_3, x2_3, y2_3, xP1, yP1, center_x_3, center_y_3, topic_ev3, msgFromEv3, flag_3, 10)

                        if dist_to_p[0] == 'p2':
                            print('msgFromEv3', msgFromEv3)
                            move(x1_3, y1_3, x2_3, y2_3, xP2, yP2, center_x_3, center_y_3, topic_ev3, msgFromEv3, flag_3, 10)

                    if msgFromEv4 == 'p':
                        print('msgFromEv4 = p')

                        if dist_to_p[1] == 'p1':
                            print('msgFromEv3', msgFromEv3)
                            move(x1_4, y1_4, x2_4, y2_4, xP1, yP1, center_x_4, center_y_4, topic_ev4, msgFromEv4, flag_4, 10)

                        if dist_to_p[1] == 'p2':
                            print('msgFromEv3', msgFromEv3)
                            move(x1_4, y1_4, x2_4, y2_4, xP2, yP2, center_x_4, center_y_4, topic_ev4, msgFromEv4, flag_4, 10)

                    if msgFromEv3 == 'zav':
                        print('msgFromEv3 = zav')
                        move(x1_3, y1_3, x2_3, y2_3, x_proizv, y_proizv, center_x_3, center_y_3, topic_ev3, msgFromEv3, flag_3, 10)

                    if msgFromEv4 == 'zav':
                        print('msgFromEv4 = zav')
                        move(x1_4, y1_4, x2_4, y2_4, x_proizv, y_proizv, center_x_4, center_y_4, topic_ev4, msgFromEv4, flag_4, 10)

                    if msgFromEv3 == 'afk_zone1':
                        print('msgFromEv3 = afk_zone1')
                        move(x1_3, y1_3, x2_3, y2_3, afk_zone_x1, afk_zone_y1, center_x_3, center_y_3, topic_ev3,
                             msgFromEv3, flag_3, 10)

                    if msgFromEv3 == 'afk_zone2':
                        print('msgFromEv3 = afk_zone2')
                        move(x1_3, y1_3, x2_3, y2_3, afk_zone_x2, afk_zone_y2, center_x_3, center_y_3, topic_ev3,
                             msgFromEv3, flag_3, 10)

                    if msgFromEv4 == 'afk_zone1':
                        print('msgFromEv4 = afk_zone1')
                        move(x1_4, y1_4, x2_4, y2_4, afk_zone_x1, afk_zone_y1, center_x_4, center_y_4, topic_ev4,
                             msgFromEv4, flag_4, 10)

                    if msgFromEv4 == 'afk_zone2':
                        print('msgFromEv4 = afk_zone2')
                        move(x1_4, y1_4, x2_4, y2_4, afk_zone_x2, afk_zone_y2, center_x_4, center_y_4, topic_ev4,
                             msgFromEv4, flag_4, 10)

                    if msgFromEv3 == 'done':
                        ev3_done = 'done'

                    if msgFromEv4 == 'done':
                        ev4_done = 'done'

                    if ev3_done == 'done' and ev4_done == 'done':
                        client.publish('Ev3ToCam', 'newModel')
                        flag_z = 0
                        flag_t = 0
                        flag_j = 0
                        flag_4 = 0
                        flag_3 = 0
                        msgFromEv4 = ''
                        msgFromEv3 = ''
                        flag_square = 0
                        old_model = new_model
                        print('***********************************************************************')
                        ev3_done = ''
                        ev4_done = ''

                    msgFromEv4 = ''
                    msgFromEv3 = ''

    cv2.imshow('okno.aruco_lessons', frame)
    if cv2.waitKey(1) == 32:
        break
