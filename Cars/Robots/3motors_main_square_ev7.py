#!/usr/bin/env python3
# желтый 192.168.100.40
import time
from ev3dev.ev3 import *
from time import sleep
import math
from threading import Thread
import socket
import sys
import paho.mqtt.client as mqtt
from decimal import *

mA = MediumMotor('outA')
mB = MediumMotor('outB')
mC = MediumMotor('outC')
mD = LargeMotor('outD')

msg_start = ''
listener_ev3 = mqtt.Client()
listener_pc = mqtt.Client()
listener_sup = mqtt.Client()
client = mqtt.Client()
y2 = 240
x2 = 320
x1 = 0
y1 = 0
a=0
d=0
square = ''
sp = ''
flag_sp = 0

msgFromEv3 = ''
msgFromPC = ''
msgFromSup = ''

topic_sup_to_robot = 'supToRoadController2'
topic_sup = 'roadControllerToSup2'
topic_pc = 'ev4/to/pc'
topic_ev4_to_ev3 = 'ev4/to/ev3'
ip_to_connect = '192.168.100.56'


class ListenEv3(Thread):
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
        listener_ev3.subscribe('ev3/to/ev4')
        print("I am listening to sup")

    def on_message(self, client, userdata, msg):
        global msgFromEv3
        msgFromEv3 = msg.payload.decode()
        print("ev3 says: " + msgFromEv3)

class ListenSup(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_sup.connect(ip_to_connect, 1883, 60) #connect
        listener_sup.on_connect = self.on_connect
        listener_sup.on_message = self.on_message
        print("client is created")

    def run(self):
        print("pc_thread start")
        listener_sup.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_sup.subscribe(topic_sup_to_robot)
        print("I am listening to sup")

    def on_message(self, client, userdata, msg):
        global msgFromSup
        msgFromSup = msg.payload.decode()
        print("sup says: " + msgFromSup)

class ListenPC(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_pc.connect(ip_to_connect, 1883, 60) #connect
        listener_pc.on_connect = self.on_connect
        listener_pc.on_message = self.on_message
        print("client is created")

    def run(self):
        print("pc_thread start")
        listener_pc.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_pc.subscribe("pc/to/ev4")
        print("I am listening to pc")

    def on_message(self, client, userdata, msg):
        global msgFromPC
        msgFromPC = msg.payload.decode()
        print("pc says: " + msgFromPC)

def move(angle, speed, time):
    a = angle
    power=speed
    a_r = math.radians(a)  # перевод угла в радианы
    y = round(math.cos(a_r), 2)
    x = round(math.sin(a_r), 2)
    ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
    n = [-x, y, 0]
    c = [0, 0, 0]
    c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
    c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
    c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
    c[0] = c[0] * 10
    c[1] = c[1] * 10
    c[2] = c[2] * 10
    mA.run_timed(time_sp=time, speed_sp=c[0])
    mB.run_timed(time_sp=time, speed_sp=c[1])
    mC.run_timed(time_sp=time, speed_sp=c[2])
    mA.wait_while('running')
    mB.wait_while('running')
    mC.wait_while('running')

def move_oracul(msgFromPc, command):
    global msgFromPC
    global square
    global sp
    while True:
        #client.publish(topic_pc, 'ok')
        msgFromPC = ''
        client.publish(topic_pc, command)
        print('command')
        while msgFromPC == '':
            print('msgFromPC is clear')

            #client.publish(topic_pc, 'ok')
            time.sleep(1)
            client.publish(topic_pc, command)
        print(msgFromPC)
        a, d = pars(msgFromPC)
        print('a, d =', a, ',', d)

        if a == 1000 and d == 1000:
            print('stooooooooooooooooooooooooooooooooooooooooooop')
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            square = ''
            sp = ''
            break

        if a == 0 and d == 0:
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            print('exit')  # Выход из цикла
            break
        if a != 0 and d == 0:  # Если дистанция равна 0, то поворачивает на какой-то угол влево или вправо
            print('a!=0 and d==0')
            power = 200
            mA.run_to_rel_pos(position_sp=a * 4.4, speed_sp=power, stop_action="brake")
            mB.run_to_rel_pos(position_sp=a * 4.4, speed_sp=power, stop_action="brake")
            mC.run_to_rel_pos(position_sp=a * 4.4, speed_sp=power, stop_action="brake")
            mA.wait_while('running')
            mB.wait_while('running')
            mC.wait_while('running')
            client.publish(topic_pc, 'ok')
            print('done')
            # sleep(1)
            print('d=0 done')
        else:  # Иначе едет на какое-то расстояние, на какой-то угол
            # if (d>200):
            #     power = 30
            # elif(d<=200 and d>100):
            #     power = 15
            # else:
            #     power = 5
            power = d * 0.25
            # print('power='+str(power))
            # if power > 100:
            # power = 20
            a_r = math.radians(a)  # перевод угла в радианы
            y = round(math.cos(a_r), 2)
            x = round(math.sin(a_r), 2)
            ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
            n = [-x, y, 0]
            c = [0, 0, 0]
            c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
            c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
            c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
            c[0] = c[0] * 10
            c[1] = c[1] * 10
            c[2] = c[2] * 10
            mA.run_forever(speed_sp=c[0])
            mB.run_forever(speed_sp=c[1])
            mC.run_forever(speed_sp=c[2])
            client.publish(topic_pc, 'ok')
            # mA.run_timed(time_sp=d, speed_sp=c[0])
            # mB.run_timed(time_sp=d, speed_sp=c[1])
            # mC.run_timed(time_sp=d, speed_sp=c[2])
            # mA.wait_while('running')
            # mB.wait_while('running')
            # mC.wait_while('running')
            # sleep(1)
            # print('done')

        msgFromPC = ''

def stop():
    client.disconnect()
    listener_pc.disconnect()
    listener_sup.disconnect()
    msgFromPC = ''
    mA.stop(stop_action="brake")
    mB.stop(stop_action="brake")
    mC.stop(stop_action="brake")
    #mD.stop(stop_action="brake")
    print('**************************************************stop')

def open(angle, speed):
    mD.run_to_rel_pos(position_sp=-angle, speed_sp=speed, stop_action="brake")

def close(angle, speed):
    mD.run_to_rel_pos(position_sp=angle, speed_sp=speed, stop_action="brake")

#def open(angle, speed):
#    mD.run_to_rel_pos(position_sp=-angle, speed_sp=speed, stop_action="brake")

#def close(angle, speed):
#    mD.run_to_rel_pos(position_sp=angle, speed_sp=speed, stop_action="brake")

def stroka(l):
    global x1
    global y1
    l=str(l)
    l = l.split(',')
    x1 = str(l[0])
    y1 = str(l[1])
    x1 = x1.replace('(', '')
    y1 = y1.replace(')', '')
    x1 = int(x1)
    y1 = int(y1)
    # print(x1)
    # print(y1)

def alfa(x1, y1, x2, y2):
    try:
        x1=int(x1)
        y1=int(y1)
        x2=int(x2)
        y2=int(y2)
        s1 = math.fabs(x1 - x2)
        s2 = math.fabs(y1 - y2)
        c = s1 / s2
        a = math.atan(c)
        a = math.degrees(a)
        if a==None:
            a=0
        if x1 > x2 and y1 > y2:
            return a
        if x1 > x2 and y1 < y2:
            return (90-a)+90
        if x1 < x2 and y1 < y2:
            return 180+a
        if x1 < x2 and y1 > y2:
            return (90-a)+270
    except ZeroDivisionError:
        if x1 > x2:
            return 0
        if x1 < x2:
            return 180

def pars(string):
    string = string.split(',')
    a = string [0]
    d = string [1]
    a = int(a)
    d = int(d)
    return a, d


client.connect(ip_to_connect,1883,1000) #connect
pc_thread = ListenPC("Listen to PC")
pc_thread.start()
sup_thread = ListenSup('Listen to sup')
sup_thread.start()
ev3_thread = ListenEv3('Listen to ev3')
ev3_thread.start()

def main():
    global msgFromPC
    global msgFromSup
    global msgFromEv3
    global flag_sp
    global sqaure
    global sp
    try:
        while True:
            while msgFromPC != 'start':
                print('msgFromPC', msgFromPC)
                sleep(1)
            print('msgFromPC', msgFromPC)
            msg_start = 'start'
            msgFromEv3 = ''
            while msg_start == 'start':
                print('while True')
                print('msgFromPc', msgFromPC)
                while msgFromPC != 'p1' and msgFromPC != 'p2' and msgFromPC != 'done_p1' and msgFromPC != 'done_p2' and msgFromPC != 'square':
                    print('while msgFromPC != p1 and msgFromPC != p2', msgFromPC)
                    sleep(1)
                    #continue
                print('msgFromPC', msgFromPC)

                if msgFromPC == 'square':
                    square = 'square'
                    print('msgFromPC = square')

                #while square == 'square':
                while msgFromPC != '1000,1000':
                    while msgFromPC != 'sp1' and msgFromPC != 'sp2' and msgFromPC != '1000,1000':
                        print('square' ,msgFromPC)
                        print('sp', sp)
                        sleep(1)
                        if sp != '' and msgFromPC != '1000,1000':
                            break
                    if square != 'square':
                        print('square != square', square)
                        break
                    if flag_sp == 0:
                        sp = msgFromPC
                        flag_sp = 1
                    #print(sp)

                    if sp == 'sp1':
                        print('sp = sp1')
                        print('wait_zone111111111111111111111111111')
                        client.publish(topic_pc, 'wait_zone1')
                        sleep(2)
                        msgFromPC = ''
                        move_oracul(msgFromPC, 'wait_zone1')
                        client.publish(topic_pc, 'wait_zone2')
                        while msgFromEv3 != 'go':
                            print(msgFromEv3)
                            time.sleep(1)
                        msgFromEv3 = ''
                        sleep(2)
                        print('wait_zone222222222222222222222222')
                        msgFromPC = ''
                        move_oracul(msgFromPC, 'wait_zone2')
                        client.publish(topic_pc, 'wait_zone3')
                        sleep(2)
                        msgFromPC = ''
                        print('wait_zone333333333333333333333333')
                        move_oracul(msgFromPC, 'wait_zone3')
                        client.publish(topic_pc, 'wait_zone4')
                        sleep(2)
                        print('wait_zone44444444444444444444444444')
                        msgFromPC = ''
                        move_oracul(msgFromPC, 'wait_zone4')
                        msgFromPC = ''
                        print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')

                    if sp == 'sp2':
                        print('sp = sp2')
                        print('wait_zone333333333333333333333333')
                        client.publish(topic_pc, 'wait_zone3')
                        sleep(2)
                        msgFromPC = ''
                        move_oracul(msgFromPC, 'wait_zone3')
                        client.publish(topic_ev4_to_ev3, 'go')
                        client.publish(topic_pc, 'wait_zone4')
                        sleep(2)
                        print('wait_zone44444444444444444444444444')
                        msgFromPC = ''
                        move_oracul(msgFromPC, 'wait_zone4')
                        #client.publish(topic_ev4_to_ev3, 'go')
                        client.publish(topic_pc, 'wait_zone1')
                        sleep(2)
                        msgFromPC = ''
                        print('wait_zone111111111111111111111111111')
                        move_oracul(msgFromPC, 'wait_zone1')
                        client.publish(topic_pc, 'wait_zone2')
                        sleep(2)
                        print('wait_zone222222222222222222222222')
                        msgFromPC = ''
                        move_oracul(msgFromPC, 'wait_zone2')
                        msgFromPC = ''
                        print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')

                #print(square)
                #print(sp)
                print('ouuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuut')
                while msgFromPC != 'p1' and msgFromPC != 'p2' and msgFromPC != 'done_p1' and msgFromPC != 'done_p2':
                    client.publish(topic_pc, '1000')
                    print('publishhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                    sleep(1)

                if msgFromPC == 'done_p1':
                    print('msgFromPC = done_p1')
                    client.publish(topic_pc, 'done')
                    move_oracul(msgFromPC, 'afk_zone1')
                    msg_start = ''

                if msgFromPC == 'done_p2':
                    print('msgFromPC = done_p2')
                    client.publish(topic_pc, 'done')
                    move_oracul(msgFromPC, 'afk_zone2')
                    msg_start = ''

                if msgFromPC != 'done_p1' and msgFromPC != 'done_p2' and msgFromPC != 'sqaure':
                    print('out while')
                    proizv = msgFromPC
                    print('proizv', proizv)
                    msgFromPC = ''
                    move_oracul(msgFromPC, 'p')

                    client.publish(topic_pc, 'stop')
                    print('here')
                    move(90, 20, 2000)
                    print('after move')
                    msgFromPC = ''

                    if proizv == 'p1':
                        client.publish(topic_pc, 'first,ev4,p1')

                        if msgFromEv3 == 'wait':
                            while msgFromEv3 == 'wait':
                                print(msgFromEv3)
                                time.sleep(1)

                        if msgFromEv3 == 'go' or msgFromEv3 == 'ev4_run':
                            print('open1')
                            client.publish(topic_sup, 'open1')

                            while msgFromSup != 'go1':
                                print('i am waiting msgFromSup', msgFromSup)
                                sleep(1)

                            while msgFromEv3 != 'ev4_run':
                                print(msgFromEv3)
                                sleep(1)

                            sleep(3)
                            print('ready')
                            msgFromPC = ''
                            move(270, 20, 3000)
                            client.publish(topic_pc, 'ready')
                            #client.publish(topic_pc, 'first,ev4,p1,zav')
                            move_oracul(msgFromPC, 'zav')
                            # move(0, 20 ,3000)
                            move(270, 20, 2000)
                            open(100, 200)
                            time.sleep(2)
                            move(90, 20, 2000)
                            close(100, 200)
                            # move(180, 20, 3500)
                            print('client.publish(topic_pc, ev3_run)')
                            msgFromPC = ''
                            move_oracul(msgFromPC, 'afk_zone1')
                            msgFromPC = ''
                            client.publish(topic_pc, 'done')
                            msgFromSup = ''
                            #msgFromEv3 = ''
                            msg_start = ''
                            flag_sp = 0

                        if msgFromEv3 != 'wait' and msgFromEv3 != 'go' and msgFromEv3 != 'ev4_run':

                            client.publish(topic_ev4_to_ev3, 'wait')
                            print('open1')
                            client.publish(topic_sup, 'open1')

                            while msgFromSup != 'go1':
                                print('i am waiting msgFromSup', msgFromSup)
                                sleep(1)

                            sleep(1)
                            print('ready')

                            move(270, 20, 3000)
                            client.publish(topic_ev4_to_ev3, 'go')
                            msgFromPC = ''
                            client.publish(topic_pc, 'first,ev4,p1,zav')
                            sleep(2)
                            move_oracul(msgFromPC, 'zav')
                            #move(0, 20 ,3000)
                            move(270, 20, 2000)
                            open(100, 200)
                            time.sleep(2)
                            move(90, 20, 2000)
                            close(100, 200)
                            #move(180, 20, 3500)
                            print('client.publish(topic_pc, ev3_run)')
                            msgFromPC = ''
                            client.publish(topic_ev4_to_ev3, 'ev3_run')
                            move_oracul(msgFromPC, 'afk_zone1')
                            msgFromPC = ''
                            client.publish(topic_pc, 'done')
                            msgFromSup = ''
                            msgFromEv3 = ''
                            msg_start = ''
                            flag_sp = 0

                    if proizv == 'p2':
                        client.publish(topic_pc, 'first,ev4,p2')

                        if msgFromEv3 == 'wait':
                            while msgFromEv3 == 'wait':
                                print(msgFromEv3)
                                time.sleep(1)

                        if msgFromEv3 == 'go' or msgFromEv3 == 'ev4_run':

                            print('open2')
                            client.publish(topic_sup, 'open2')
                            while msgFromSup != 'go2':
                                print('i am waiting msgFromSup', msgFromSup)
                                sleep(1)
                            while msgFromEv3 != 'ev4_run':
                                print(msgFromEv3)
                                sleep(1)

                            sleep(3)
                            print('msgFromPC', msgFromPC)
                            print('ready')
                            msgFromPC = ''
                            move(270, 20, 3000)
                            # client.publish(topic_pc, 'ready')
                            move_oracul(msgFromPC, 'zav')
                            print('zav')
                            # move(0, 20 ,3000)
                            move(270, 20, 2000)
                            open(100, 200)
                            time.sleep(2)
                            move(90, 20, 2000)
                            close(100, 200)
                            # move(180, 20, 3000)
                            msgFromPC = ''
                            move_oracul(msgFromPC, 'afk_zone2')
                            msgFromPC = ''
                            client.publish(topic_pc, 'done')
                            msgFromSup = ''
                            #msgFromEv3 = ''
                            msg_start = ''
                            flag_sp = 0

                        if msgFromEv3 != 'wait' and msgFromEv3 != 'go' and msgFromEv3 != 'ev4_run':
                            client.publish(topic_ev4_to_ev3, 'wait')

                            print('open2')
                            client.publish(topic_sup, 'open2')
                            while msgFromSup != 'go2':
                                print('i am waiting msgFromSup', msgFromSup)
                                sleep(1)

                            sleep(1)
                            print('msgFromPC', msgFromPC)
                            print('ready')
                            msgFromPC = ''
                            move(270, 20, 3000)
                            client.publish(topic_ev4_to_ev3, 'go')
                            client.publish(topic_pc, 'first,ev4,p2,zav')
                            sleep(2)
                            move_oracul(msgFromPC, 'zav')
                            print('zav')
                            move(270, 20, 2000)
                            open(100, 200)
                            time.sleep(2)
                            move(90, 20, 2000)
                            close(100, 200)
                            msgFromPC = ''
                            client.publish(topic_ev4_to_ev3, 'ev3_run')
                            move_oracul(msgFromPC, 'afk_zone2')
                            msgFromPC = ''
                            client.publish(topic_pc, 'done')
                            msgFromSup = ''
                            msgFromEv3 = ''
                            msg_start = ''
                            flag_sp = 0


    finally:
        stop()
        #msgFromPC = ''


main()