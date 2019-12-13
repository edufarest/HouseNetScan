#!/bin/python

import csv, os, time, requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

nmap = "echo ''" #"sudo nmap -sn 192.168.1.1/24 | grep -o -E '([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])'"


SentryMode = input("Sentry Mode? [y/N]") == "y"
rate = 15

# Get input

username = os.getenv('ROUTER_USERNAME')
password = os.getenv('ROUTER_PASSWORD')

cookies = {}

while True:

    with open('targets.csv') as targetsFile:
        targets = csv.reader(targetsFile, delimiter=',')

        connected = os.popen(nmap).read().split('\n')



        for target in targets:
            # print(device)
            for device in connected:
                if str(device) == target[1]:
                    print(target[0])
        
    with open('targetsName.csv') as targetsFile:
        targets = csv.reader(targetsFile, delimiter=',')

        URL = "http://192.168.1.1"

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(URL)

        print(driver.get_cookies())

        cookie_header = ""

        for cookie in driver.get_cookies():
            cookie_header += cookie['name'] + "=" + cookie['value'] + ";"

        # POST to login
        post = requests.post(
            URL+"/check.php",
            data={'username':username, 'password':password},
            headers={"Host": "192.168.1.1",
                     "Accept": "*/*",
                     "Content-Type": "application/x-www-form-urlencoded",
                     "Referer": "http://192.168.1.1/check.php",
                     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
                     "Cache-Control": "no-cache",
                     "Accept-Encoding": "gzip, deflate",
                     "Connection": "keep-alive",
                     "Cookie": cookie_header}
        )

        print("Response: " + str(post.status_code))

        print(post.text)

        for cookie in post.cookies:
            print("Cookie" + str(cookie))
            cookies[cookie.name] = cookie.value

        # if 'PHPSESSID' in cookies:
        #     print(cookies['PHPSESSID'])          # <- find python equivalent to default a dict
        # else:
        #     print(cookies)

        # connected_devices = requests.get(
        #     URL + "/connected_devices_computers.php"
        # )
        #
        # resText = connected_devices.text
        #
        # resHtml = BeautifulSoup(resText, 'html.parser')


        driver.get(URL+"/connected_devices_computers.php")

        online_devices = driver.find_element_by_id("online-private")
        print(online_devices)
        # online_devices = resHtml.findAll(id="online-private")

        # print(online_devices)



        r = requests.get(url = URL)

        data = r.text

        root = BeautifulSoup(data, 'html.parser')

        for line in targets:
            for target in line:

                name = re.compile(target+'([\s]|$)') # Match name ending with , or eof

                if name.search(data):
                    print(target)

    if not SentryMode:
        break
    
    time.sleep(rate)

