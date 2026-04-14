import network
import time
import machine
from machine import Pin
from umqtt.simple import MQTTClient

# =========================
# WIFI
# =========================
WIFI_SSID = "Wifiwork"
WIFI_PASSWORD = "imbored!"

# =========================
# MQTT
# =========================
BROKER = "broker.hivemq.com"
PORT = 1883

# 🔥 FIXED CLIENT ID (CRITICAL)
CLIENT_ID = b"esp32_led_device"

NAME = "rulerofyou403"

TOPIC_CMD = b"wyohack/" + NAME.encode() + b"/led/command"
TOPIC_STATUS = b"wyohack/" + NAME.encode() + b"/led/status"

# =========================
# LED
# =========================
LED = Pin(12, Pin.OUT)

client = None


# =========================
# WIFI
# =========================
def wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print("Connecting WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wlan.isconnected():
        time.sleep(1)

    print("WiFi OK:", wlan.ifconfig()[0])


# =========================
# CALLBACK
# =========================
def callback(topic, msg):
    print("🔥 MESSAGE:", msg)

    cmd = msg.decode().strip().upper()

    if cmd == "ON":
        LED.value(1)
        client.publish(TOPIC_STATUS, b"ON")
        print("LED ON")

    elif cmd == "OFF":
        LED.value(0)
        client.publish(TOPIC_STATUS, b"OFF")
        print("LED OFF")


# =========================
# MQTT CONNECT
# =========================
def mqtt():
    global client

    print("Connecting MQTT...")

    client = MQTTClient(CLIENT_ID, BROKER, PORT)

    client.set_callback(callback)

    client.connect()

    client.subscribe(TOPIC_CMD)

    print("MQTT READY")


# =========================
# MAIN LOOP
# =========================
def main():
    wifi()
    mqtt()

    while True:
        client.check_msg()
        time.sleep(0.2)


main()
