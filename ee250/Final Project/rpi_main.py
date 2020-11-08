import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd/')
import grovepi
import grove_rgb_lcd

buzzer_port = 8 # D8
ultrasonic_port = 7 # D7
led_port = 3
button_port = 0 # D0


def mode(client, userdata, mode_message):
    mode_payload = str(mode_message.payload, "utf-8")
    if mode_payload == "0":
        print(0)
    elif mode_payload == "1":
        print(1)
    elif mode_payload == "2":
        print(2)
    elif mode_payload == "3":
        print(3)
    elif mode_payload == "4":
        print(4)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("chenjosh/customMode")
    client.message_callback_add("chenjosh/customMode", mode)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))



if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60) # Connected to USC's MQTT server
    client.loop_start()

while True:
    time.sleep(1)