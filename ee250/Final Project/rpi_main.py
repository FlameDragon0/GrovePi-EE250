import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd/')
import grovepi
import grove_rgb_lcd

time = 0
time_blocked = 0
people = 0
mood = 0
buzzer_port = 8 # D8
ultrasonic_port = 7 # D7
led_port = 3
button_port = 0 # D0


def mode(client, userdata, mood_message):
    mood_payload = str(mood_message.payload, "utf-8")
    mood = int(mood_payload)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # Subscribed topics
    client.subscribe("chenjosh/customMode")
    client.message_callback_add("chenjosh/customMode", mode)

# Default message callback.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))



if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60) # Connected to USC's MQTT server
    client.loop_start()

while True:
    if time = 100: # Publish every 0.05 x 100 = 5 seconds
        time = 0
        client.publish("chenjosh/people", str(people))
        client.publish("chenjosh/mood", str(mood))
        #publish
    
    grove_rgb_lcd.setText_norefresh("People: " + people + "\nNo custom mood")

    ultrasonic_value = grovepi.ultrasonicRead(ultrasonic_port)

    if int(ultrasonic_value) < 70: # If something is less than 70cm away from the ultrasonic ranger, then something must be going through the door
        time_blocked += 1
    elif time_blocked > 2: # If something blocks the doorway for 0.2s or more, then we assume that a person did go through
        people += 1
    else:
        time_blocked = 0 # If not, then we don't count as someone went through the doorway.
    
    time += 1
    time.sleep(0.05) # Sleep for 0.1 seconds


