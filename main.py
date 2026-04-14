import network
import time
import machine
import ubinascii
from machine import Pin
from umqtt.robust import MQTTClient

# --- CONFIGURATION ---
WIFI_SSID = "Wifiworks"
WIFI_PASSWORD = "imbored!"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# Your specific ID for topics
USER_ID = "rulerofyou403-web"

# MQTT topics
TOPIC_COMMAND = b"wyohack/" + USER_ID.encode() + b"/led/command"
TOPIC_STATUS = b"wyohack/" + USER_ID.encode() + b"/led/status"

# Your hardware Pin (GPIO 12)
LED_PIN = 12
led = Pin(LED_PIN, Pin.OUT)

# FIX FOR -202 ERROR: Using a more unique, randomized Client ID
# Adding a timestamp helps prevent the broker from rejecting the "duplicate" ID
unique_suffix = ubinascii.hexlify(machine.unique_id()).decode()
CLIENT_ID = f"ruler_{unique_suffix}_{int(time.time())}".encode()

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
        return True
    else:
        print("Wi-Fi failed. Check SSID/Password.")
        return False

def publish_status(state):
    global client
    try:
        client.publish(TOPIC_STATUS, state.encode())
        print("Published status:", state)
    except:
        print("Failed to publish status.")

def mqtt_callback(topic, msg):
    # .strip() removes hidden spaces or newlines that cause errors
    command = msg.decode().strip().upper()
    print(f"Received: {command} on {topic.decode()}")

    if command == "ON":
        led.value(1)
        print("LED is now ON")
        publish_status("ON")
    elif command == "OFF":
        led.value(0)
        print("LED is now OFF")
        publish_status("OFF")
    else:
        print(f"Invalid command ignored: {command}")

def connect_umqtt():
    global client
    # Removed 'keepalive' to ensure compatibility with all library versions
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    
    print(f"Connecting to broker with ID: {CLIENT_ID.decode()}...")
    client.connect()
    client.subscribe(TOPIC_COMMAND)
    
    print("MQTT Online.")
    print("Listening on:", TOPIC_COMMAND.decode())

def main():
    if connect_wifi():
        try:
            connect_umqtt()
            while True:
                # Check for new messages every 100ms
                client.check_msg()
                time.sleep(0.1)
        except Exception as e:
            print(f"MQTT Error: {e}")
            print("Rebooting in 5 seconds to clear connection...")
            time.sleep(5)
            machine.reset()

# Start the program
if __name__ == "__main__":
    main()
