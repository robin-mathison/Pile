#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from enum import Enum
    
class Button:

    """
    A class for reading button presses.
    """
    BTN_B = 29 # GPIO pin 5
    BTN_R = 38 # GPIO pin 20
    BTN_G = 40 # GPIO pin 21
    BTN_Y = 22 # GPIO pin 25

    DEBOUNCE_MS = 100 # time for debouncing
    
    def __init__(self):
        """
        Initialize the button GPIOs.
        """
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.BTN_B, GPIO.IN)
        GPIO.setup(self.BTN_R, GPIO.IN)
        GPIO.setup(self.BTN_G, GPIO.IN)
        GPIO.setup(self.BTN_Y, GPIO.IN)

    def read(self) -> (int, int, int, int):
        """
        Read the button presses.
        Returns the tuple (B state, R state, G state, Y state).
        """

        return (GPIO.input(self.BTN_B), GPIO.input(self.BTN_R), GPIO.input(self.BTN_G), GPIO.input(self.BTN_Y))
    
    def setup_callback(self, fn):
        """
        Sets up a callback to be run when any buttons are pressed.
        The callback should be declared in the following way:
        def fn(channel):
            
        """
        GPIO.add_event_detect(self.BTN_B, GPIO.FALLING, callback=fn, bouncetime=self.DEBOUNCE_MS)
        GPIO.add_event_detect(self.BTN_R, GPIO.FALLING, callback=fn, bouncetime=self.DEBOUNCE_MS)
        GPIO.add_event_detect(self.BTN_G, GPIO.FALLING, callback=fn, bouncetime=self.DEBOUNCE_MS)
        GPIO.add_event_detect(self.BTN_Y, GPIO.FALLING, callback=fn, bouncetime=self.DEBOUNCE_MS)

class Led:
    """
    A class for writing to the onboard RGB LED.
    """

    LED_B = 7 # GPIO pin 4
    LED_G = 13 # GPIO pin 27
    LED_R = 15 # GPIO pin 22
    
    def __init__(self):
        """
        Initialize the LED GPIOs.
        """

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.LED_B, GPIO.OUT)
        GPIO.setup(self.LED_G, GPIO.OUT)
        GPIO.setup(self.LED_R, GPIO.OUT)

    def write(self, R: int, G: int, B: int):
        """
        Write the values of R, G, and B to the LED GPIOs.
        """

        GPIO.output(self.LED_B, B)
        GPIO.output(self.LED_G, G)
        GPIO.output(self.LED_R, R)

    def __del__(self):
        """
        Return all GPIO pins to inputs.
        """
        GPIO.setup(self.LED_B, GPIO.IN)
        GPIO.setup(self.LED_G, GPIO.IN)
        GPIO.setup(self.LED_R, GPIO.IN)

class RotState(Enum):
    NONE = 0
    CW = 1
    CCW = 2

class RotEnc:

    ENC_1 = 11 # GPIO pin 17
    ENC_2 = 12 # GPIO pin 18

    DEBOUNCE_MS = 100

    def debounce(self, pin):
        v1 = GPIO.input(pin)
        if v1 == GPIO.LOW:
            time.sleep(0.001) # sleep 1 ms
            v2 = GPIO.input(pin)
            if v2 == GPIO.LOW:
                return True
        return False

    def __init__(self):
        """
        Initialize the rotary encoder pins.
        """
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.ENC_1, GPIO.IN)
        GPIO.setup(self.ENC_2, GPIO.IN)

    def read(self):
        """
        Read the rotary encoder. Blocks until the knob is turned.
        """
        prev_1 = self.debounce(self.ENC_1)
        prev_2 = self.debounce(self.ENC_2)

        while True:
            curr_1 = self.debounce(self.ENC_1)
            curr_2 = self.debounce(self.ENC_2)
            
            if curr_1 != prev_1 or curr_2 != prev_2:
                if (prev_1, prev_2, curr_1, curr_2) == (False, False, False, True):
                    return RotState.CW
                elif (prev_1, prev_2, curr_1, curr_2) == (False, False, True, False):
                    return RotState.CCW
                prev_1 = curr_1
                prev_2 = curr_2

    def setup_callback(self, fn):
        """
        Sets up a callback to be run when the knob is turned.
        The callback should be declared in the following way:
        def fn(dir: RotState):
            
        """
        self.call_fn = fn

        def check_dir(channel):
            """
            Check which direction the rotary encoder is turning.
            """
            if channel == self.ENC_1 and GPIO.input(self.ENC_2) == GPIO.HIGH:
                self.call_fn(RotState.CCW)
            elif GPIO.input(self.ENC_1) == GPIO.HIGH:
                self.call_fn(RotState.CW)

        GPIO.add_event_detect(self.ENC_1, GPIO.FALLING, callback=check_dir, bouncetime=self.DEBOUNCE_MS)
        GPIO.add_event_detect(self.ENC_2, GPIO.FALLING, callback=check_dir, bouncetime=self.DEBOUNCE_MS)

class PDF_state:
    ROW = "1"
    COL = "1"
   
    def __init__(self):
        ROW = "1"
        COL = "1"
    
    # Rotate from top left --> right --> bottom left
    def rotate(self):
        if (self.ROW == "1" and self.COL == "1"):
            self.COL = "2"
        elif (self.ROW == "1" and self.COL == "2"):
            self.ROW = "2"
            self.COL = "1"
        elif (self.ROW == "2" and self.COL == "1"):
            self.ROW = "1"
        

def test():
    """
    Run a simple test procedure for the onboard peripherals (except the brightness sensor)
    """
    print('blinking LED')
    
    l = Led()
    l.write(0, 0, 0)

    time.sleep(0.2)

    l.write(1, 1, 1)

    time.sleep(0.2)

    def show_val(channel):
        print(f'press on channel {channel}')

    b = Button()
    b.setup_callback(show_val)
    
    def show_enc(dir: RotState):
        print(f'turn, direction: {dir}')

    enc = RotEnc()
    enc.setup_callback(show_enc)
    
    print('turn the rotary encoder or press buttons, they should show up here')
    while True:
        pass

if __name__ == "__main__":
    test()

