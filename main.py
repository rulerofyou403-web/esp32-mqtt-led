import machine
import network
import time
import ubinascii
from umqtt.robust import MQTTClient

# --- Configuration ---
WIFI_SSID = "Wifiworks"
WIFI_PASS = "imbored!"
MQTT_BROKER = "://hivemq.com"
GITHUB_USER = "rulerofyou403-web"

# Topics
TOPIC_COMMAND = f"wyohack/{GITHUB_USER}/led/command"
TOPIC_STATUS = f"wyohack/{GITHUB_USER}/led/status"

# Hardware Setup (GPIO 12)
led = machine.Pin(12, machine.Pin.OUT)

# Unique Client ID
CLIENT_ID = b"esp32_" + ubinascii.hexlify(machine.unique_id())

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("WiFi Connected!", wlan.ifconfig())

def sub_cb(topic, msg):
    command = msg.decode().strip().upper()
    print(f"Received: {command}")
    if command == "ON":
        led.value(1)
        client.publish(TOPIC_STATUS, "ON")
    elif command == "OFF":
        led.value(0)
        client.publish(TOPIC_STATUS, "OFF")

# --- Main ---
connect_wifi()
client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(sub_cb)

try:
    client.connect()
    client.subscribe(TOPIC_COMMAND)
    print(f"Online! Command topic: {TOPIC_COMMAND}")
    while True:
        client.check_msg()
        time.sleep(0.1)
except Exception as e:
    print("Error:", e)
    machine.reset()
