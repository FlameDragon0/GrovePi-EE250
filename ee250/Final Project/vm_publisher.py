import paho.mqtt.client as mqtt
import time
from pynput import keyboard

menu = 1

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def command(key):
    global menu
    if key == 'n':
        # reset to normal mode
        client.publish("chenjosh/customMood", "No Custom Mood")
        print("Room resetted back to normal mode!")
    elif key == 'm':
        # set to Movie mode (Dark)
        client.publish("chenjosh/customMood", "Movie Mood")
        print("Movie Mood on!")
    elif key == 'p':
        # set to Party mode (Flashing Lights)
        client.publish("chenjosh/customMood", "Party Mood")
        print("Party Mood on! Hooray!")
    elif key == 'c':
        # set to Conference mode (Bright Lights)
        client.publish("chenjosh/customMood", "Conference Mood")
        print("Conference Mood on!")
    elif key == 'r':
        # set to Relaxing mode (Dim Lights)
        client.publish("chenjosh/customMood", "Relaxing Mood")
        print("Relaxing Mood on~~~")
    elif key == 'x':
        # Set maximum number of people allowed in the room
        max_people = 0
        max_people = int(input("Type the number and press \"ENTER\". Enter 0 to cancel.\n"))
        if max_people:
            client.publish("chenjosh/maxPeople", str(max_people))
            print("New maximum capacity = " + str(max_people))
        elif max_people == 0: # In case the user missclicked, entering 0 will not update this maximum value
            print("Cancelled")
        else:
            print("That was an invalid input!")
    else: # If the user entered something invalid, then a warning will be displayed!
        print("That was an invalid input!")
    menu = 1


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60) # Connecting to USC's MQTT server
    client.loop_start()

    time.sleep(2) # Allowing the connection to print first before the menu!
    key = ""
    menu_text = "\nEnter the letter corresponding to the settings you wish to apply!\nn: Reset room to non-custom mode\nm: Set room to Movie\np: Set room to Party Mood\nc: Set room to Conference Mood\nr: Set room to Relaxing Mood\nx: Change maximum capacity"
    # Sorry for the long text! Python doesn't allow me to wrap around

    while True:
        if menu:
            print(menu_text)
            menu = 0
        
        key = input() # Obtain the input from the user
        if key != "": # If the user didn't input anything, then nothing will be done!
            command(key)

        time.sleep(1)