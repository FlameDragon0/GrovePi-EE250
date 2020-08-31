""" EE 250L Lab 02: GrovePi Sensors

List team members here.

Insert Github repository link here.
""" #git@github.com:FlameDragon0/GrovePi-EE250.git

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages

The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi

if sys.platform == 'uwp': # If statements used by the LCD [Statements copied from grove_rgb_lcd.py]
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# I2C addresses used by the LCD
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# set backlight to (R,G,B) (values from 0..255 for each) [Function copied from grove_rgb_lcd.py]
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use) [Function copied from grove_rgb_lcd.py]   
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap) [Function copied from grove_rgb_lcd.py]    
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 grovepi_sensors.py` in terminal, this if-statement will 
be true"""
if __name__ == '__main__':
    ultrasonic = 4    # D4
    rotary = 0 #A0
    #grovepi.pinMode(rotary,"INPUT")
    printText = ""

    while True:
        #So we do not poll the sensors too quickly which may introduce noise,
        #sleep for a reasonable time of 200ms between each iteration.
        time.sleep(0.2)
        printText = "" # Resets the text printed on the screen

        # Read sensor value from rotary angle sensor
        rotary_value = grovepi.analogRead(rotary)/2

        # Read sensor value from ultrasonic ranger
        ultrasonic_value = grovepi.ultrasonicRead(ultrasonic)

        if rotary_value < 100: # Indenting the rotary value
          printText += " "
        printText += str(int(rotary_value)) + "cm"

        if ultrasonic_value < rotary_value: # Checks if an object is within the threshold value
          printText += " OBJ PRES"
          setRGB(255,0,0) # sets screen color to red
        else:
          setRGB(0,255,0) # sets screen color to green
        
        if ultrasonic_value < 100: # Indenting the ultrasonic value
          printText += "\n "
        else:
          printText += "\n"
        printText += str(int(ultrasonic_value)) + "cm"

        setText(printText) # Prints text on LCD

