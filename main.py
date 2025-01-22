from machine import Pin, I2C
import time
import math

# MPU6050-Klasse importieren
from MPU6050 import MPU6050

# I²C initialisieren
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Zwei MPU6050-Sensoren initialisieren
mpu1 = MPU6050(i2c, addr=0x68)
mpu2 = MPU6050(i2c, addr=0x69)

# Globale Variable für den letzten relativen Roll
last_relative_roll = None

# Funktion zur Winkelberechnung
def calculate_angles(accel):
    x, y, z = accel['x'], accel['y'], accel['z']
    pitch = math.degrees(math.atan2(x, math.sqrt(y**2 + z**2)))
    roll = math.degrees(math.atan2(y, math.sqrt(x**2 + z**2)))
    return roll, pitch

# Funktion, um relative Winkel zu berechnen
def calculate_relative_angles():
    global last_relative_roll

    # Werte von beiden Sensoren lesen
    accel1 = mpu1.get_accel()
    roll1, _ = calculate_angles(accel1)

    accel2 = mpu2.get_accel()
    roll2, _ = calculate_angles(accel2)

    # Relative Werte berechnen
    relativeroll = roll1 - roll2

    # Letzten relativen Roll speichern
    last_relative_roll = relativeroll

# Interrupt-Handler
def touch_interrupt_handler(pin):
    global last_relative_roll

    print("Kontakt erkannt! Schleife gestartet.")
    
    # Solange der Schalter geschlossen ist, Schleife ausführen
    while not pin.value():  # Prüfen, ob der Schalter geschlossen ist (LOW bei Pull-Up)
        calculate_relative_angles()
        time.sleep(0.1)  # Verzögerung, um die CPU nicht zu überlasten

    # Wenn der Schalter geöffnet wird
    print("Schalter geöffnet. Schleife beendet.")
    if last_relative_roll is not None:
        print("Letzter relativer Roll: {:.2f}°".format(last_relative_roll))
    time.sleep(0.2)  # Entprellzeit

# GPIO für Fingerkontakt konfigurieren
touch_pin = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO 15 mit internem Pull-Up-Widerstand
touch_pin.irq(trigger=Pin.IRQ_FALLING, handler=touch_interrupt_handler)

# Hauptschleife (optional)
try:
    while True:
        time.sleep(1)  # Programm bleibt aktiv
except KeyboardInterrupt:
    print("Programm beendet.")
