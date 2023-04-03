import time, datetime
import sys
import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4

#-----------
# Constants
#-----------
LED_PINS = [5, 6, 7]
KEY1_PIN = 8
KEY2_PIN = 9
RED_LED_PIN = 4
#------------------------------
# Initialized global variables
#------------------------------
prevPin = LED_PINS[0]
board = CustomPymata4()

#-----------
# Functions
#-----------

def countdown(h, m, s):
    global timer_started
    
    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s

    # Create a flag to indicate whether the timer is running or not
    timer_running = True
    
    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0 and timer_running:

        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds=total_seconds)

        # Extract minutes and seconds from the timer
        minutes, seconds = divmod(timer.seconds, 60)

        # Format the minutes and seconds as a string
        time_str = '{:02d}{:02d}'.format(minutes, seconds)

        # Display the time left on the timer on the Arduino
        board.displayShow(time_str)
        
        # Prints the time left on the timer
        print(timer, end="\r")
 
        # Delays the program one second
        time.sleep(1)
 
        # Reduces total time by one second
        total_seconds -= 1

    # Reset the timer_started flag when the countdown is over
    timer_started = False

    if board.digital_read(KEY1_PIN) == 0:
        print("Timer restarted")
        countdown(h, m, s)

def setup():
    # Initialize the board and set the pins to output and input mode
    global board
    board = CustomPymata4()

    for pin in LED_PINS:
        board.set_pin_mode_digital_output(pin)
    board.set_pin_mode_digital_input_pullup(KEY1_PIN) # Enable internal pull-up resistor
    board.set_pin_mode_digital_input_pullup(KEY2_PIN) # Enable internal pull-up resistor

def start_countdown():
    # Inputs for hours, minutes, seconds on timer
    h = int(input("Enter the time in hours: "))
    m = int(input("Enter the time in minutes: "))
    s = int(input("Enter the time in seconds: "))
    
    global countdown_running, timer_started
    countdown_running = True
    timer_started = True
    countdown(h, m, s)
    print("Bzzzt! pizza is done done!")

def restart_countdown():
    global countdown_running, timer_started
    countdown_running = True
    timer_started = True

def cook():
    # Turn on the red LED to simulate cooking
    board.digital_pin_write(RED_LED_PIN, 1)
    time.sleep(10) # Cook for 10 seconds
    board.digital_pin_write(RED_LED_PIN, 0)
    notify_server()

def notify_server():
    # Send an HTTP POST request to the server to notify that the cooking is done
    # Replace the URL with the actual server endpoint
    url = "http://127.0.0.1:5000/"
    payload = {'message': 'Cooking is done'}
    requests.post(url, data=payload)

def loop():
    global timer_started

    # Check if the button is pressed to start cooking
    if board.digital_read(KEY1_PIN) == 0 and not timer_started:
        start_countdown()  # Call the start_countdown function
        timer_started = True  # Set the flag to indicate that the timer has been started

    # Cycle through the LED pins and light them up one at a time
    for pin in LED_PINS:
        board.digital_pin_write(prevPin, 0)
        board.digital_pin_write(pin, 1)
        time.sleep(0.5)
        prevPin = pin

start_countdown()
countdown()
restart_countdown()
cook()
loop()
#--------------
# Main program
#--------------

# Initialize a variable to keep track of whether the timer has been started or not
timer_started = False
# Main program loop
while True:
    try:
        # Check if the button is pressed to start cooking
        if board.digital_read(KEY1_PIN) == 0 and not timer_started:
            countdown_running=False
            start_countdown()  # Call the start_countdown function
            timer_started = True  # Set the flag to indicate that the timer has been started
            
            

        # Check if the key2 button is pressed to restart the timer
        if board.digital_read(KEY2_PIN) == 0 and timer_started:
            print("Timer restarted")
            restart_countdown()  # Call the restart_countdown function
            h = input("Enter the time in hours: ")
            m = input("Enter the time in minutes: ")
            s = input("Enter the time in seconds: ")
            countdown(int(h), int(m), int(s))

        if board.digital_read(KEY1_PIN) == 0:
            print("Button 1 pressed")
        if board.digital_read(KEY2_PIN) == 0:
            print("Button 2 pressed")
        
        loop()  # Move the loop function call to the end of the while loop    
    
    except KeyboardInterrupt:
        print('Shutdown')
        board.shutdown()
        sys.exit(0)
