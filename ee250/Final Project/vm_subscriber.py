import paho.mqtt.client as mqtt
import time


def people(client, userdata, people_message): # Displays the current number of people in the room
    people_payload = str(people_message.payload, "utf-8")
    print("\nNumber of people in room: " + people_payload)

def percentage(client, userdata, percentage_message): # Displays the percentage of how full the room is
    percentage_payload = str(percentage_message.payload, "utf-8")
    print("Current capacity: " + percentage_payload)

def mood(client, userdata, mood_message): # Displays the current mood that the room is in
    mood_payload = str(mood_message.payload, "utf-8")
    print("Current mood: " + mood_payload)

def maxWarning(client, userdata, warning_message): # Displays a warning if the room is full or over capacity
    warning_payload = str(warning_message.payload, "utf-8")
    print(warning_payload)


def on_connect(client, userdata, flags, rc): # Subscribed topics
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("chenjosh/people")
    client.message_callback_add("chenjosh/people", people)
    client.subscribe("chenjosh/percentage")
    client.message_callback_add("chenjosh/percentage", percentage)
    client.subscribe("chenjosh/currentMood")
    client.message_callback_add("chenjosh/currentMood", mood)
    client.subscribe("chenjosh/maxWarning")
    client.message_callback_add("chenjosh/maxWarning", maxWarning)


# Default message callback.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)