Team members: Joshuah Chen (solo)

Note: In my demo video, I didn't explicitly mention that my data was processed on the
"server" (my RPI), so I wanted to let you know about it here.

Link to Demo: https://drive.google.com/file/d/1TxLV7kcTtqCsg3zwPwbpqPQSEptRr-OW/view?usp=sharing

Instructions on how to compile:
You will need 3 terminals to run my final project:
 1) First terminal is connected to your RPI and have it run rpi_main.py. Some peripherals that
    need to be connected to the GrovePi on the RPI are:
        - LCD (on any of the I2C ports)
        - Rotary Encoder on A0
        - Green LED on D5
        - Blue LED on D3
        - Red LED on D6
        - Ultrasonic Ranger on D7
        - Buzzer on D8
 2) Second terminal will run vm_publisher.py. Through this terminal is where you will be sending
    commands to the RPI through the MQTT server at USC by typing directly to the terminal.
 3) Third terminal will run vm_subscriber.py. This terminal will be displaying information that
    the RPI sent to the MQTT. There is no need to type in this command terminal.
        
External Libraries used:
    - paho.mqtt.client
    - time
    - sys
    - threading
    - grovepi
    - grove_rgb_lcd
    - pynput