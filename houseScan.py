#!/bin/python

import csv
import os
import time
import requests
import paho.mqtt.client as paho
import paho.mqtt.publish as publish

from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

nmap = "sudo nmap -sn 192.168.1.1/24 | grep -o -E '([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])'"

# TODO Use TLS and user/pass for MQTT broker

topic = os.getenv('MQTT_TOPIC')
mqttc = paho.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with code " + str(rc))

    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqtt_broker = os.getenv('MQTT_BROKER')

mqttc.connect(mqtt_broker)

mqttc.loop_start()

with open('/home/eduardo/projects/HouseNetScan/targets.csv') as targetsFile:
    targets = csv.reader(targetsFile, delimiter=',')

    connected = os.popen(nmap).read().split('\n')



    for target in targets:
        # print(device)
        for device in connected:
            if str(device) == target[1]:

                # Device detected
                publish.single(topic, target[0], hostname=mqtt_broker)

                print(target[0])
    
with open('/home/eduardo/projects/HouseNetScan/targetsName.csv') as targetsFile:
    targets = csv.reader(targetsFile, delimiter=',')

    URL = "http://192.168.1.1"

    # TODO POST to login and GET actual devices page

    r = requests.get(url = URL)

    data = r.text

    root = BeautifulSoup(data, 'html.parser')

    for line in targets:
        for target in line:

            if data.find(target) >= 0:
                # Target found
                # Device detected
                publish.single(topic, target, hostname=mqtt_broker)
                print(target)