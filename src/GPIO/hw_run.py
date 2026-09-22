import requests
import sys
from time import sleep

import brightness
import hw_api

# Run on launch for button and rotary encoder updates
def hw_run():

    BTN_UP = 40     # Green button
    BTN_DWN = 38    # Red button
    BTN_BRT = 22    # Yellow button
    BTN_TGL = 29    # Blue button
    
    # Information for post / get requests
    url = "http://127.0.0.1:5000/chungus"

    # Information for brightness sensor
    auto = True
    sensor = brightness.BrightnessSensor()
    adjust = brightness.BrightnessAdjuster()

    state = hw_api.PDF_state()

    # Toggles between automatic and manual brightness adjustment
    # Scrolls PDF up and down
    def btn_func(channel):
        if (channel == BTN_BRT):
            if (adjust.AUTO == True):
                adjust.AUTO = False
            else:
                adjust.AUTO = True
        elif (channel == BTN_UP):
            up_col_row = 'Up c' + state.COL + 'r' + state.ROW
            data_up = {'scroll-action': up_col_row}
            requests.post(url, data_up)
        elif (channel == BTN_DWN):
            down_col_row = 'Down c' + state.COL + 'r' + state.ROW
            data_down = {'scroll-action': down_col_row}
            requests.post(url, data_down)
        elif (channel == BTN_TGL):
            state.rotate()

    # Set up buttons
    btn = hw_api.Button()
    btn.setup_callback(btn_func)

    # Launch brightness sensor
    adjust.brightness_adjustment(sensor)

hw_run()