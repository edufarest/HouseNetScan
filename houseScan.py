#!/bin/python

import csv, os, sys, time, requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from notify_run import Notify
from datetime import datetime


notify = Notify()

load_dotenv()

if len(sys.argv) > 0:
    if sys.argv[1] == "-h":
        print("-h: help\n" +
              "-f: fast, use default options")
        sys.exit()

    elif sys.argv[1] == "-f":
        SentryMode = True
        ScanType = 1
else:


    nmap = "sudo nmap -sn 192.168.1.1/24 | grep -o -E '([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])'"


    SentryMode = input("Sentry Mode? [y/N]") == "y"
    ScanType = input("nmap(0), router(1), both(2) - default: 1") or 1
rate = 15

# Get input

username = os.getenv('ROUTER_USERNAME')
password = os.getenv('ROUTER_PASSWORD')

cookies = {}

while True:

    print("Starting round - " + str(datetime.now()))

    if ScanType == 0 or ScanType == 2:

        with open('targets.csv') as targetsFile:
            targets = csv.reader(targetsFile, delimiter=',')

            connected = os.popen(nmap).read().split('\n')



            for target in targets:
                # print(device)
                for device in connected:
                    if str(device) == target[1]:
                        print(target[0])

    if ScanType == 1 or ScanType == 2:
        with open('targetsName.csv') as targetsFile:
            targets = csv.reader(targetsFile, delimiter=',')

            URL = "http://192.168.1.1"

            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=chrome_options)

            driver.get(URL)


            cookie_header = ""

            for cookie in driver.get_cookies():
                cookie_header += cookie['name'] + "=" + cookie['value'] + ";"


            # Fill login form

            driver.find_element_by_id("username").send_keys(username)
            driver.find_element_by_id("password").send_keys(password)

            elements = driver.find_element_by_class_name("btn")

            if elements:
                elements.click()

            driver.get(URL+"/connected_devices_computers.php")

            online_devices = driver.find_element_by_id("online-private")

            if online_devices:

                connected = online_devices.find_elements_by_tag_name("u")

                targets = list(targets)[0]

                for target in targets:

                    for device in connected:
                        if target == device.text:
                            notify.send(target)
                            print(target)

            driver.close()

    if not SentryMode:
        break

    time.sleep(rate)

