import network
import time
import machine
from machine import Pin
from umqtt.robust import MQTTClient

# --- YOUR UPDATED CONFIGURATION ---
WIFI_SSID = "Wifiworks"
WIFI_PASSWORD = "imbored!"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# Your specific ID from the previous attempts
USER_ID = "rulerofyou403-web"

# MQTT topics
TOPIC_COMMAND = b"wyohack/" + USER_ID.encode() + b"/led/command"
TOPIC_STATUS = b"wyohack/" + USER_ID.encode() + b"/led/status"

# Your specific GPIO pin (from your working blink test)
LED_PIN = 12
led = Pin(LED_PIN, Pin.OUT)

# Unique MQTT client ID (added randomization to prevent kicks)
CLIENT_ID = b"rulerofyou_esp32_" + machine.unique_id()

client = None

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("Wi-Fi connected. IP:", wlan.ifconfig()[0])
        return wlan
    else:
        print("Wi-Fi failed. Check SSID/Password.")
        return None

def publish_status(state):
    global client
    client.publish(TOPIC_STATUS, state.encode())
    print("Published status:", state)

def mqtt_callback(topic, msg):
    # .strip() is key here to remove any hidden spaces/newlines
    command = msg.decode().strip().upper()
    print(f"Received: {command}")

    if command == "ON":
        led.value(1)
        publish_status("ON")
    elif command == "OFF":
        led.value(0)
        publish_status("OFF")
    else:
        print("Invalid command received.")

def connect_umqtt():
    global client
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=60)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(TOPIC_COMMAND)
    print("MQTT Online.")
    print("Command Topic:", TOPIC_COMMAND.decode())

def main():
    if connect_wifi():
        connect_umqtt()
        while True:
            try:
                client.check_msg()
                time.sleep(0.1)
            except Exception as e:
                print("Connection lost, reconnecting...")
                time.sleep(5)
                machine.reset()

main()
