import requests
import sys
from time import sleep

if __name__ == '__main__':
    url = "http://127.0.0.1:5000/chungus"
    if len(sys.argv) == 4 and sys.argv[1] != 'd' and sys.argv[1] != 'u':
        print("Proper Usage: python3 scrolldown.py d|u r# c#")
        exit(-1)
    down_col_row = 'Down c' + sys.argv[2] + 'r' + sys.argv[3]
    up_col_row = 'Up c' + sys.argv[2] + 'r' + sys.argv[3]
    data_down = {'scroll-action': down_col_row}
    data_up = {'scroll-action': up_col_row}

    if sys.argv[1] == 'd':
        for i in range(0, 10):
            requests.post(url, data_down)
        print("scrolled down")

    if sys.argv[1] == 'u':
        for i in range(0, 10):
            requests.post(url, data_up)
        print("scrolled up")

        