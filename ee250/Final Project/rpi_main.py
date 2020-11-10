import paho.mqtt.client as mqtt
import time
import sys
import threading
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd/')
import grovepi
import grove_rgb_lcd

clock = 0
time_blocked = 0
people = 0
mood = 0
max_people = 10
LCD_needs_update = 0

buzzer_port = 8 # D8
ultrasonic_port = 7 # D7
rled_port = 3 #D3 Red led
bled_port = 2 #D2 Blue led
gled_port = 1 #D1 Green led
button_port = 0 # D0

lock = threading.Lock()

def customMood(client, userdata, mood_message):
    mood_payload = str(mood_message.payload, "utf-8")
    mood = int(mood_payload)
    LCD_needs_update = 1
    print("Custom Mood received!")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # Subscribed topics
    client.subscribe("chenjosh/customMood")
    client.message_callback_add("chenjosh/customMood", customMood)

# Default message callback.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def get_mood_info(mood_info): # Do the lighting functions + call them here!
    if mood_info == 0:
        return "No Custom Mood"
    elif mood_info == 1:
        return "Movie Mood"
    elif mood_info == 2:
        return "Party Mood"
    elif mood_info == 3:
        return "Conference Mood"
    elif mood_info == 4:
        return "Relaxing Mood"

def update_LCD(num_people, mood_info):
    text = "People: " + str(num_people) + "\n" + get_mood_info(mood_info)
    with lock:
        grove_rgb_lcd.setText(text)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60) # Connected to USC's MQTT server
    client.loop_start()

    grove_rgb_lcd.setText("People: 0\nNo Custom Mood") # Initializing LCD to initial conditions, with nobody inside the room and no custom mood.
    grove_rgb_lcd.setRGB(0, 0, 0)

while True:
    if clock == 100: # Publish every 0.05 x 100 = 5 seconds
        clock = 0
        client.publish("chenjosh/people", str(people))
        client.publish("chenjosh/mood", str(mood))
        #publish

    ultrasonic_value = grovepi.ultrasonicRead(ultrasonic_port)

    if int(ultrasonic_value) < 70: # If something is less than 70cm away from the ultrasonic ranger, then something must be going through the door
        time_blocked += 1
    elif time_blocked > 3: # If something blocks the doorway for 0.2s or more, then we assume that a person did go through
        people += 1
        time_blocked = 0
        LCD_needs_update = 1
    else:
        time_blocked = 0 # If not, then we don't count as someone went through the doorway.

    if LCD_needs_update:
        update_LCD(people, mood)
        LCD_needs_update = 0



    clock += 1
    time.sleep(0.05) # Sleep for 50ms


