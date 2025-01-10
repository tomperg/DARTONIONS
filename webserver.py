
import socket
from ADXL345 import ADXL345_I2C
from functions import calculate_angles
import math
import time


def web_page():
    f = open('webserver.html')
    html = f.read()
    f.close()
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn, addr = s.accept()
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

    time.sleep(0.01)