# ESP32 MQTT LED Controller

This project uses an ESP32 with MicroPython to control an LED through MQTT.

Broker: broker.hivemq.com  
Command topic: wyohack/YOUR_NAME/led/command  
Status topic: wyohack/YOUR_NAME/led/status  

The ESP32 connects to Wi-Fi and then connects to the MQTT broker. 
It listens for ON and OFF messages on the command topic. 
When it receives a command, it changes the LED state and 
   publishes the new status to the status topic.
