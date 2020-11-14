import paho.mqtt.client as mqtt
import time

def people(client, userdata, people_message):
    people_payload = str(people_message.payload, "utf-8")
    print("Number of people in room: " + people_payload)

def percentage(client, userdata, percentage_message):
    percentage_payload = str(percentage_message.payload, "utf-8")
    print("Current capacity: " + percentage_payload)

def mood(client, userdata, mood_message):
    mood_payload = str(mood_message.payload, "utf-8")
    print("Current mood: " + mood_payload)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #Subscribed topics
    client.subscribe("chenjosh/people")
    client.message_callback_add("chenjosh/people", people)
    client.subscribe("chenjosh/percentage")
    client.message_callback_add("chenjosh/percentage", percentage)
    client.subscribe("chenjosh/currentMood")
    client.message_callback_add("chenjosh/currentMood", mood)

#Default message callback. Please use custom callbacks.
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