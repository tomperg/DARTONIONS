from machine import Pin, I2C
import time
import math
from functions import *
import socket 
import os 
import network 
import json

# MPU6050-Klasse importieren
from MPU6050 import MPU6050

# I²C initialisieren
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Zwei MPU6050-Sensoren initialisieren
try:
    mpu1 = MPU6050(i2c, addr=0x68) 
    mpu2 = MPU6050(i2c, addr=0x69) #AD0 auf vcc für andere Adresse
except Exception as e:
    print(f"Fehler bei der MPU6050-Initialisierung: {e}")
    raise

def get_content_type(filename):
    """Bestimmt den Content-Type basierend auf der Dateierweiterung"""
    if filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.css'):
        return 'text/css'
    elif filename.endswith('.js'):
        return 'application/javascript'
    elif filename.endswith('.json'):
        return 'application/json'
    else:
        return 'text/plain'

def load_file(filename):
    """Lädt eine Datei und gibt deren Inhalt zurück"""
    try:
        with open(filename, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Fehler beim Laden der Datei {filename}:", e)
        return None

def send_response(conn, content, content_type, status="200 OK"):
    """Sendet eine HTTP-Response"""
    try:
        response = f'HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nConnection: close\r\n\r\n'
        conn.sendall(response.encode())
        if content:
            conn.sendall(content.encode() if isinstance(content, str) else content)
    except Exception as e:
        print(f"Fehler beim Senden der Response: {e}")

def send_404(conn):
    """Sendet eine 404-Fehlermeldung"""
    send_response(conn, '<h1>404 - Datei nicht gefunden</h1>', 'text/html', "404 Not Found")

def send_sensor_data(conn):
    """Sendet die Sensordaten als JSON"""
    global measured_values
    try:
        # Verwende die gespeicherten Messwerte
        mpu_data = {
            "last_relative_roll": round(measured_values["angle"], 2) if measured_values["angle"] is not None else None,
            "velocity": {
                "x": round(measured_values["velocity"], 2) if measured_values["velocity"] is not None else 0,
                "y": 0,
                "z": 0,
                "total": round(measured_values["velocity"], 2) if measured_values["velocity"] is not None else 0
            }
        }
        measured_values["angle"] = None
        measured_values["velocity"] = None
        response = json.dumps(mpu_data)
        send_response(conn, response, "application/json")
    except Exception as e:
        print(f"Fehler beim Senden der Sensordaten: {e}")
        send_response(conn, json.dumps({"error": str(e)}), "application/json", "500 Internal Server Error")

def handle_client(conn, addr):
    """Behandelt eine einzelne Client-Verbindung"""
    try:
        conn.settimeout(5)  # 5 Sekunden Timeout für einzelne Verbindungen
        request = conn.recv(1024).decode()
        if not request:
            return
            
        request_line = request.split('\n')[0]
        path = request_line.split(' ')[1]
        
        if path == "/data":
            send_sensor_data(conn)
        else:
            if path == "/":
                filename = "webserver.html"
            else:
                filename = path[1:]
                
            content = load_file(filename)
            if content:
                content_type = get_content_type(filename)
                send_response(conn, content, content_type)
            else:
                send_404(conn)
                
    except Exception as e:
        print(f"Fehler bei Client {addr}: {e}")
    finally:
        try:
            conn.close()
        except:
            pass

# Globale Variablen
is_button_pressed = False  # Status des Schalters
last_interrupt_time = 0    # Für Entprellung
measured_values = {        # Gespeicherte Messwerte
    "angle": None,
    "velocity": None
}

def touch_interrupt_handler(pin):
    global is_button_pressed, last_interrupt_time, measured_values
    
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_interrupt_time) < 100:  # Entprellzeit
        return
    last_interrupt_time = current_time
    
    # Entprellen
    time.sleep(0.05)
    
    # Schalter wurde losgelassen (Pfeil wird geworfen)
    if pin.value() and is_button_pressed:
        print("Schalter losgelassen - Pfeil wird geworfen")
        is_button_pressed = False
        
        try:
            # Lese die finalen Werte beim Loslassen
            accel1 = mpu1.get_accel()
            gyro1 = mpu1.get_gyro()
            accel2 = mpu2.get_accel()
            
            # Berechne den Winkel
            roll1, _ = calculate_angles(accel1)
            roll2, _ = calculate_angles(accel2)
            relativer_roll = roll1 - roll2

            # Überprüfe, ob accel1["z"] <= 0 oder accel1["z"] > 0 um relativen roll richtig anzuwenden
            if accel1["z"] <= 0:
                final_angle = relativer_roll  # Verwende den relativen Rollwinkel
            else:
                final_angle = 180 - relativer_roll  # Verwende 180 - relativen Rollwinkel
            
            # Berechne die Winkelgeschwindigkeit von mpu1 bei einem Radius von 25 cm
            final_velocity = calculate_velocity_from_gyro(gyro1["x"], gyro1["y"], gyro1["z"], radius=0.25)
            
            # Speichere die Messwerte
            measured_values["angle"] = final_angle
            measured_values["velocity"] = final_velocity
            
            print(f"Wurf erfasst - Winkel: {final_angle:.2f}°, Geschwindigkeit: {final_velocity:.2f} m/s")
            
        except Exception as e:
            print(f"Fehler bei der Messung: {e}")
            measured_values["angle"] = None
            measured_values["velocity"] = None
    
    # Schalter wurde gedrückt (Pfeil wird gehalten)
    elif not pin.value() and not is_button_pressed:
        print("Schalter gedrückt - Pfeil wird gehalten")
        is_button_pressed = True

# GPIO für Schalter konfigurieren
try:
    touch_pin = Pin(15, Pin.IN, Pin.PULL_UP)
    touch_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=touch_interrupt_handler)
except Exception as e:
    print(f"Fehler bei der GPIO-Konfiguration: {e}")
    raise

# Socket erstellen und konfigurieren
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(30)  # 30 Sekunden Timeout für accept()
    s.bind(('', 80))
    s.listen(5)
except Exception as e:
    print(f"Fehler bei der Socket-Initialisierung: {e}")
    raise

# Hauptschleife
print("Server gestartet. Warte auf Verbindungen...")
try:
    while True:
        try:
            conn, addr = s.accept()
            print(f"Neue Verbindung von {addr}")
            handle_client(conn, addr)
        except OSError as e:
            if e.args[0] == 116:  # ETIMEDOUT
                print("Timeout bei accept(), versuche erneut...")
                continue
            else:
                print(f"Socket-Fehler: {e}")
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")
        finally:
            time.sleep(0.1)  # Kurze Pause zwischen Verbindungen

except KeyboardInterrupt:
    print("\nProgramm wird beendet...")
finally:
    try:
        s.close()
        print("Socket geschlossen.")
    except:
        pass