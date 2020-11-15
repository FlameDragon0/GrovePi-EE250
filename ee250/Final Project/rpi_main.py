import paho.mqtt.client as mqtt
import time
import sys
import threading
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd/')
import grovepi
import grove_rgb_lcd


# Initializing global variables
LCD_needs_update = 0
mood = "No Custom Mood"
max_people = 10
sound_buzzer = 0


# Initializing ports
buzzer_port = 8 # D8
ultrasonic_port = 7 # D7
rled_port = 6 #D6 Red led
bled_port = 3 #D3 Blue led
gled_port = 5 #D5 Green led

rotary_port = 0 # A0, I used the rotary encoder instead of a button because my button was not working
grovepi.pinMode(rotary_port,"INPUT")
grovepi.pinMode(rled_port,"OUTPUT")
grovepi.pinMode(bled_port,"OUTPUT")
grovepi.pinMode(gled_port,"OUTPUT")


def no_custom_mood(num_people): # Normal mood where the LED's light on based on the percentage of people in the room
    global max_people
    global rled_port, bled_port, gled_port
    if num_people > 0: # Green LED will light up if at least 1 person is in the room
        grovepi.digitalWrite(gled_port, 1)
    else:
        grovepi.digitalWrite(gled_port, 0)
    
    if num_people >= (max_people/2):# Blue LED will light up if the room has reached 50% capacity
        grovepi.digitalWrite(bled_port, 1)
    else:
        grovepi.digitalWrite(bled_port, 0)
    
    if num_people >= max_people: # Red LED will light up if the room has reached 100% capacity
        grovepi.digitalWrite(rled_port, 1)
    else:
        grovepi.digitalWrite(rled_port, 0)


def custom_brightness_mood(brightness): # all 3 leds gets turned on but their brightness goes down
    global rled_port, bled_port, gled_port
    grovepi.analogWrite(gled_port, brightness) # Brightness = 31 (1/8th of the led's max brightness) in Movie Mood
    grovepi.analogWrite(bled_port, brightness) # Brightness = 256 (full led brightness) in Conference Mood
    grovepi.analogWrite(rled_port, brightness) # Brightness = 127 (half of the led's max brightness) in Relaxing Mood


def party_mood(clock): # three leds start flashing in an fun "party style" pattern!
    global rled_port, bled_port, gled_port
    if (clock < 2) + (clock >= 8) * (clock < 10) + (clock >= 164) * (clock < 18):
        grovepi.digitalWrite(gled_port, 1)
        grovepi.digitalWrite(bled_port, 0)
        grovepi.digitalWrite(rled_port, 0)
    elif (clock < 4) + (clock >= 6) * (clock < 8) + (clock >= 10) * (clock < 12) + (clock >= 14) * (clock < 16) + (clock >= 18) * (clock < 20) + (clock >= 22) * (clock < 24) + (clock >= 26) * (clock < 28) + (clock >= 30) * (clock < 32) + (clock >= 34) * (clock < 36):
        grovepi.digitalWrite(gled_port, 0)
        grovepi.digitalWrite(bled_port, 1)
        grovepi.digitalWrite(rled_port, 0)
    elif (clock < 6) + (clock >= 12) * (clock < 14) + (clock >= 20) * (clock < 22):
        grovepi.digitalWrite(gled_port, 0)
        grovepi.digitalWrite(bled_port, 0)
        grovepi.digitalWrite(rled_port, 1)
    elif (clock < 26) + (clock >= 28) * (clock < 30) + (clock >= 32) * (clock < 34) + (clock >= 36) * (clock < 38):
        grovepi.digitalWrite(gled_port, 1)
        grovepi.digitalWrite(bled_port, 0)
        grovepi.digitalWrite(rled_port, 1)
    elif (clock >= 42) * (clock < 44) + (clock >= 46) * (clock < 48):
        grovepi.digitalWrite(gled_port, 1)
        grovepi.digitalWrite(bled_port, 1)
        grovepi.digitalWrite(rled_port, 1)
    else:
        grovepi.digitalWrite(gled_port, 0)
        grovepi.digitalWrite(bled_port, 0)
        grovepi.digitalWrite(rled_port, 0)


def customMood(client, userdata, mood_message): # New mood command from controller
    global LCD_needs_update
    global mood
    mood = str(mood_message.payload, "utf-8")
    LCD_needs_update = 1 # Updates LCD with the new mood


def maxPeople(client, userdata, max_message): # New maximum from controller
    global max_people
    new_max = str(max_message.payload, "utf-8")
    max_people = int(new_max)


def buzzer_beep(clock, time_entered): # Buzzer will sound two beeps when someone enters the room
    global buzzer_port
    global sound_buzzer
    if (time_entered > 40) * (clock < 10): #In case clock was set to 0 before the buzzer finished beeping
        clock = clock + 50
    if (clock >= time_entered) * (clock < time_entered + 2) + (clock >= time_entered + 4) * (clock < time_entered + 6):
        grovepi.digitalWrite(buzzer_port, 1)
    else:
        grovepi.digitalWrite(buzzer_port, 0)
    if (time_entered + 6) == clock:
        sound_buzzer = 0


def on_connect(client, userdata, flags, rc): # Subscribed topics
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("chenjosh/customMood")
    client.message_callback_add("chenjosh/customMood", customMood)
    client.subscribe("chenjosh/maxPeople")
    client.message_callback_add("chenjosh/maxPeople", maxPeople)


# Default message callback.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def update_LCD(num_people): # Function that updates the LCD's display
    global mood
    text = "People: " + str(num_people) + "\n" + mood
    grove_rgb_lcd.setText(text)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60) # Connected to USC's MQTT server
    client.loop_start()


    # Initializing LCD to initial conditions, with nobody inside the room and no custom mood.
    grove_rgb_lcd.setText("People: 0\nNo Custom Mood")
    grove_rgb_lcd.setRGB(255, 255, 255)


    # Initalizing local variables
    clock = 0
    time_blocked = 0
    people = 0
    rotary_held = 0
    entered_time = 0

while True:
    if clock == 10: # Publish every 0.05 x 100 = 5 seconds
        clock = 0
        client.publish("chenjosh/people", str(people))
        percent = str((float(people) /  max_people) * 100) + "%"
        client.publish("chenjosh/percentage", percent)
        client.publish("chenjosh/currentMood", mood)
        if people == max_people:
            warning = "Room at maximum capacity!"
            client.publish("chenjosh/maxWarning", warning)
        elif people > max_people:
            warning = "WARNING: Room over maximum capacity!"
            client.publish("chenjosh/maxWarning", warning)


    # Reads the values from the ultrasonic and rotary encoder (which should be a button)
    ultrasonic_value = grovepi.ultrasonicRead(ultrasonic_port) # Reads every 50ms
    if (clock % 2) == 0:
        rotary_value = grovepi.analogRead(rotary_port) # Reads every 100ms because Analogue can't read too fast or else it will cause some problems


    if rotary_value > 0: # "Button" has been pressed
        rotary_held = 1
    elif (rotary_value == 0) * (rotary_held): # "Button" has been let go, so we assume 1 person exited the room"
        if people > 0:
            people = people - 1
            LCD_needs_update = 1
        rotary_held = 0
    

    if int(ultrasonic_value) < 70: # If something is less than 70cm away from the ultrasonic ranger, then something must be going through the door
        time_blocked += 1
    elif time_blocked > 2: # If something blocks the doorway for 0.15s or more, then we assume that a person did go through
        people += 1
        time_blocked = 0
        LCD_needs_update = 1
        sound_buzzer = 1
        entered_time = clock
    else:
        time_blocked = 0 # If not, then we don't count as someone went through the doorway.


    # Setting the different moods
    if mood == "No Custom Mood":
        no_custom_mood(people)
    elif mood == "Movie Mood":
        custom_brightness_mood(31)
    elif mood == "Party Mood":
        party_mood(clock)
    elif mood == "Conference Mood":
        custom_brightness_mood(255)
    elif mood == "Relaxing Mood":
        custom_brightness_mood(127)
    

    # Checking if LCD display needs an update
    if LCD_needs_update != 0:
        update_LCD(people)
        LCD_needs_update = 0
    

    # Checking if buzzer needs to be sounded
    if sound_buzzer:
        buzzer_beep(clock, entered_time)


    #Increments clock every 50ms
    clock += 1
    time.sleep(0.05) # Sleep for 50ms


