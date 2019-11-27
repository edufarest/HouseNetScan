#!/bin/python

import csv, os, time, requests
from bs4 import BeautifulSoup


nmap = "sudo nmap -sn 192.168.1.1/24 | grep -o -E '([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])'"

with open('/home/eduardo/projects/HouseNetScan/targets.csv') as targetsFile:
    targets = csv.reader(targetsFile, delimiter=',')

    connected = os.popen(nmap).read().split('\n')



    for target in targets:
        # print(device)
        for device in connected:
            if str(device) == target[1]:
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
                print(target)