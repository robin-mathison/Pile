#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def debounce(pin):
    v1 = GPIO.input(pin)
    if v1 == GPIO.LOW:
        time.sleep(0.001) # sleep 1 ms
        v2 = GPIO.input(pin)
        if v2 == GPIO.LOW:
            return True
    return False
    

GPIO.setmode(GPIO.BOARD) # use board I/O pin numbers rather than processor pin numbers

LED_B = 7 # GPIO pin 4
LED_G = 13 # GPIO pin 27
LED_R = 15 # GPIO pin 22

BTN_B = 29 # GPIO pin 5
BTN_R = 38 # GPIO pin 20
BTN_G = 40 # GPIO pin 21
BTN_Y = 22 # GPIO pin 25

ENC_1 = 11 # GPIO pin 17
ENC_2 = 12 # GPIO pin 18

GPIO.setup(LED_B, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_R, GPIO.OUT)

GPIO.setup(BTN_B, GPIO.IN)
GPIO.setup(BTN_R, GPIO.IN)
GPIO.setup(BTN_G, GPIO.IN)
GPIO.setup(BTN_Y, GPIO.IN)

GPIO.setup(ENC_1, GPIO.IN)
GPIO.setup(ENC_2, GPIO.IN)

try: 
    print('blinking LED')

    GPIO.output(LED_B, 0)
    GPIO.output(LED_G, 0)
    GPIO.output(LED_R, 0)

    time.sleep(0.2)

    GPIO.output(LED_B, 1)
    GPIO.output(LED_G, 1)
    GPIO.output(LED_R, 1)

    time.sleep(0.2)

    print('reading buttons')

    print(f'BTN_B: {GPIO.input(BTN_B)}')
    print(f'BTN_R: {GPIO.input(BTN_R)}')
    print(f'BTN_G: {GPIO.input(BTN_G)}')
    print(f'BTN_Y: {GPIO.input(BTN_Y)}')

    prev_1 = debounce(ENC_1)
    prev_2 = debounce(ENC_2)

    while True:
        curr_1 = debounce(ENC_1)
        curr_2 = debounce(ENC_2)
        
        if curr_1 != prev_1 or curr_2 != prev_2:
            print(f'prev: ({prev_1}, {prev_2}), curr: ({curr_1}, {curr_2})')
            if (prev_1, prev_2, curr_1, curr_2) == (False, False, False, True):
                print('clockwise')
            elif (prev_1, prev_2, curr_1, curr_2) == (False, False, True, False):
                print('counterclockwise')
            prev_1 = curr_1
            prev_2 = curr_2

finally:
    print('cleaning up GPIO state')
    GPIO.cleanup() # sets all GPIOs back to inputs for safety
