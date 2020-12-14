#inspired by:
# https://github.com/timopb/rpi-cputemp-mqtt/blob/master/main.py
# https://stackoverflow.com/questions/2440511/getting-cpu-temperature-using-python/16256136#16256136

from __future__ import division
import os
from collections import namedtuple
import glob
import time
import datetime
import sys
import paho.mqtt.client as mqtt

MQTT_SERVER = os.getenv("MQTT_SERVER", 'mqtt.pi-docker.lab')
MQTT_PORT = os.getenv("MQTT_PORT", 1883)
MQTT_TOPIC = os.getenv("MQTT_TOPIC",'home/tichy/temps/')
INTERVAL = int(os.getenv("MQTT_INTERVAL", 2))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

_nt_cpu_temp = namedtuple('cputemp', 'name temp max critical')



def get_cpu_temp(fahrenheit=False):
    """Return temperatures expressed in Celsius for each physical CPU
    installed on the system as a list of namedtuples as in:

    >>> get_cpu_temp()
    [cputemp(name='atk0110', temp=32.0, max=60.0, critical=95.0)]
    """
    # http://www.mjmwired.net/kernel/Documentation/hwmon/sysfs-interface
    cat = lambda file: open(file, 'r').read().strip()
    base = '/sys/class/hwmon/'
    ls = sorted(os.listdir(base))
    assert ls, "%r is empty" % base
    ret = []
    for hwmon in ls:
        hwmon = os.path.join(base, hwmon)
        #print(hwmon)
        try:
            innerbase = os.path.join(hwmon, 'temp*_label')
            #print(innerbase)
            ib=str(innerbase)
            #print(ib)
            innerls = glob.glob(ib)
            #print("huhu")
            #print(innerls)
            assert innerls, "%r is empty" % innerbase
            for labelfile in innerls:
                #print(labelfile)
                label = cat(labelfile)
                #print(label)
                #assert 'Core 0' in label.lower(), label
                #print(label)
                name = cat(os.path.join(hwmon, 'name'))
                #print(name)
                assert 'coretemp' in name.lower(), name
                #print(os.path.join(hwmon, 'temp'+labelfile[-7:-6]+'_input'))
                temp = int(cat(os.path.join(hwmon, 'temp'+labelfile[-7:-6]+'_input'))) / 1000
                max_ = int(cat(os.path.join(hwmon, 'temp'+labelfile[-7:-6]+'_max'))) / 1000
                crit = int(cat(os.path.join(hwmon, 'temp'+labelfile[-7:-6]+'_crit'))) / 1000
                digits = (temp, max_, crit)
                if fahrenheit:
                    digits = [(x * 1.8) + 32 for x in digits]
                ret.append(_nt_cpu_temp(label, *digits))
        except:
            pass
    return ret

next_reading = time.time()

client = mqtt.Client()
#client.username_pw_set(USERNAME, PASSWORD)

print("==== Connecting to %s ====" % MQTT_SERVER)
client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()

# test with:
# mosquitto_sub -h mqtt.pi-docker.lab -t 'home/tichy/#' -v

try:
    while True:
        now = time.time()
        nt=get_cpu_temp()
        #print(nt)
        for tupel in nt:
            print(tupel.name+' '+str(tupel.temp))
            client.publish(MQTT_TOPIC+tupel.name, tupel.temp, 1)
        next_reading += INTERVAL
        sleep_time = next_reading - now
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()