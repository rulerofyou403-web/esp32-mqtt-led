import network
import time
import machine
import ubinascii
import random
from machine import Pin
from umqtt.robust import MQTTClient

# --- CONFIGURATION ---
WIFI_SSID = "Wifiworks"
WIFI_PASS = "imbored!"
MQTT_BROKER = "broker.hivemq.com"
USER_ID = "rulerofyou403-web"

# Topics
TOPIC_COMMAND = f"wyohack/{USER_ID}/led/command".encode()
TOPIC_STATUS = f"wyohack/{USER_ID}/led/status".encode()

# Hardware Setup (GPIO 12)
led = Pin(12, Pin.OUT)

# GENERATE A TOTALLY UNIQUE CLIENT ID TO FIX -202 ERROR
# This adds a random number and a timestamp to avoid "duplicate ID" kicks
unique_id = ubinascii.hexlify(machine.unique_id()).decode()
CLIENT_ID = f"ruler_{unique_id}_{random.getrandbits(10)}_{int(time.time())}".encode()

def sub_cb(topic, msg):
    command = msg.decode().strip().upper()
    print(f"Received Command: {command}")
    
    if command == "ON":
        led.value(1)
        print("LED: ON")
        client.publish(TOPIC_STATUS, b"ON")
    elif command == "OFF":
        led.value(0)
        print("LED: OFF")
        client.publish(TOPIC_STATUS, b"OFF")

# Wi-Fi Connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)

print("Connecting Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)
print("Wi-Fi Connected!", wlan.ifconfig()[0])

# MQTT Connection
client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(sub_cb)

print(f"Connecting to broker with ID: {CLIENT_ID.decode()}...")
try:
    client.connect()
    client.subscribe(TOPIC_COMMAND)
    print("--- ONLINE! ---")
    print(f"Listening on: {TOPIC_COMMAND.decode()}")
except Exception as e:
    print(f"Connection Failed: {e}")
    print("Wait 10 seconds and try again.")

# Main Loop
while True:
    try:
        client.check_msg()
        time.sleep(0.1)
    except:
        machine.reset() # Reboot if connection drops
