import paho.mqtt.client as mqtt
from threading import Thread


listener_ev3 = mqtt.Client()
listener_ev4 = mqtt.Client()
broker = "192.168.100.59"

msgFromEV3 = ""
msgFromEV4 = ""

class ListenEV3(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_ev3.connect(broker, 1883, 1000)
        listener_ev3.on_connect = self.on_connect
        listener_ev3.on_message = self.on_message
        print("client is created")

    def run(self):
        print("ev3_thread start")
        listener_ev3.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_ev3.subscribe("roadControllerToSup1")
        print("I am listening to ev3")

    def on_message(self, client, userdata, msg):
        global msgFromEV3
        msgFromEV3 = msg.payload.decode()


class ListenEV4(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_ev4.connect(broker, 1883, 1000)
        listener_ev4.on_connect = self.on_connect
        listener_ev4.on_message = self.on_message
        print("client is created")

    def run(self):
        print("ev3_thread start")
        listener_ev4.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_ev4.subscribe("roadControllerToSup2")
        print("I am listening to ev3")

    def on_message(self, client, userdata, msg):
        global msgFromEV4
        msgFromEV4 = msg.payload.decode()

