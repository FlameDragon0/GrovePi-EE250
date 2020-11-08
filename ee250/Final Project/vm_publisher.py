import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == '0':
        # reset to normal mode
        client.publish("chenjosh/customMode", "0")
    elif k == '1':
        # set to Movie mode (Dark)
        client.publish("chenjosh/customMode", "1")
    elif k == '2':
        # set to Party mode (Flashing Lights)
        client.publish("chenjosh/customMode" , "2")
    elif k == '3':
        # set to Conference mode (Bright Lights)
        client.publish("chenjosh/customMode", "3")
    elif k == '4':
        # set to Relaxing mode (Dim Lights)
        client.publish("chenjosh/customMode", "4")

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)