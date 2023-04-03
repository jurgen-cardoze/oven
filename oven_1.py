import time
import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4

# Constants
GREEN_LED_PIN = 5
YELLOW_LED_PIN = 7
BLUE_LED_PIN = 6
RED_LED_PIN = 4
LEFT_BUTTON= 9
RIGHT_BUTTON=8

# Create the Arduino board object
board = CustomPymata4("COM4")

def countdown(minutes, seconds):
    minutes= int(input("Enter the time in minutes: "))
    seconds= int(input("Enter the time in seconds: "))
    total_seconds = minutes * 60 + seconds

    for i in range(total_seconds, -1, -1):
        print("Time remaining:{:02d}:{:02d}".format(i // 60, i % 60))
        time_str= '{:02d}{:02d}'.format(i //60, i % 60)
        board.displayShow(time_str)
        time.sleep(1)

# Set the LED pins as output pins
board.set_pin_mode_digital_output(GREEN_LED_PIN)
board.set_pin_mode_digital_output(YELLOW_LED_PIN)
board.set_pin_mode_digital_output(BLUE_LED_PIN)
board.set_pin_mode_digital_output(RED_LED_PIN)


# Turn on the red LED to indicate that the oven is ON
board.digital_pin_write(RED_LED_PIN,1)

# Wait for 5 seconds to simulate start up time

time.sleep(5)


# Turn off the red LED and turn on the yellow LED to indicate that the food is being prepared
board.digital_pin_write(RED_LED_PIN,0)
board.digital_pin_write(YELLOW_LED_PIN,1)

# Wait for 1 seconds to simulate prep time
time.sleep(1)
response = requests.post("http://example.com/oven/done")
if response.status_code == 200:
    print("kitchen notified food is in the oven ")
else:
    print("Failed to notify the server")

# Turn off the yellow LED and turn on the blue LED to indicate that the food cooking
board.digital_pin_write(YELLOW_LED_PIN,0)
board.digital_pin_write(BLUE_LED_PIN,1)

# Wait for 3 seconds to simulate cooking time
countdown(0,5)
time.sleep(3)

# Turn off the blue LED and turn on the green LED to indicate that the food is done
board.digital_pin_write(BLUE_LED_PIN,0) 
board.digital_pin_write(GREEN_LED_PIN,1)

# Wait for 5 second to display the green LED for some time
time.sleep(5)

# Turn off the green LED
board.digital_pin_write(GREEN_LED_PIN,0)

# Communicate with the server application that the oven is done cooking
response = requests.post("http://example.com/oven/done")
if response.status_code == 200:
    print("Server notified that the oven is done cooking")
else:
    print("Failed to notify the server")
