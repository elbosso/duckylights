import time
import os
import duckylights
import random
from duckylights import device_path
import paho.mqtt.client as mqtt

MQTT_SERVER = os.getenv("MQTT_SERVER", 'mqtt.pi-docker.lab')
MQTT_PORT = os.getenv("MQTT_PORT", 1883)
MQTT_TOPIC = os.getenv("MQTT_TOPIC",'home/tichy/temps/')
INTERVAL = int(os.getenv("MQTT_INTERVAL", 1))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

def random_color():
    return hex(random.randint(0, 256**3 - 1))[2:].rjust(6, '0')

def on_message(client, userdata, message):
    if 'Core ' in message.topic:
        print("received message =",str(message.payload.decode("utf-8")))
        print(message.topic)
        print(message.topic[-1:])
        s=message.topic[-1:]
        index=int(s)
        if(index<5):
            temp[index]=float(message.payload.decode("utf-8"))

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")
        client.subscribe('home/tichy/temps/#')  # subscribe

    else:

        print("Connection failed")

temp=[30.0,40.0,50.0,60.0,70.0]

next_reading = time.time()

client = mqtt.Client()
#client.username_pw_set(USERNAME, PASSWORD)

client.on_message=on_message
client.on_connect=on_connect

print("==== Connecting to %s ====" % MQTT_SERVER)
client.connect(MQTT_SERVER, MQTT_PORT)

client.loop_start()

with duckylights.keyboard(path=device_path(vendor=0x04d9, product=0x0356)) as dev, dev.programming() as ducky:
    try:
        while True:
            now = time.time()
            print(now)
            colors = ['000000'] * (6 * 22)
            for x in range(10):
                for y in range(5):
                    if(temp[y]/10<x):
                        colors[x*6+y]='a0a0a0'
                    else:
                        if(x<5):
                            colors[x*6+y]='00ff00'
                        else:
                            colors[x*6+y]='ff0000'
            ducky.custom_mode(colors)
            next_reading += INTERVAL
            sleep_time = next_reading - now
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass

client.loop_stop()
client.disconnect()