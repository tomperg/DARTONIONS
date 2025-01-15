# boot.py -- run on boot-up
'''import gc
import network
import esp
import time
esp.osdebug(None)
gc.collect()

ssid = 'iPhone von Amelie'
password =""

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)
#'Animation'
print('Connecting to network...')
while not station.isconnected():
    print('.', end='')
    time.sleep(1)

print('Connection successful')
print(station.ifconfig())'''