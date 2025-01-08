import gc
import network
import esp
import time
esp.osdebug(None)
gc.collect()

ssid = 'A1-Mesh-WLAN-a9de7'
password = '54114678025427959546'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)
#'Animation'
print('Connecting to network...')
while not station.isconnected():
    print('.', end='')
    time.sleep(1)

print('Connection successful')
print(station.ifconfig())