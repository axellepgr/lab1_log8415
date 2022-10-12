import json
import requests
from threading import Thread
import time

with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

lb_dns = json_object["lb_dns"]


def call_endpoint_http(nbr):
    url = "http://" + lb_dns
    headers = {'content-type': 'application'}
    print("starting to send requests using thread" + str(nbr))
    if nbr == 1:
        for i in range(0, 1000):
            r = requests.get(url, headers=headers)
            print("status code: " + r.status_code + "response:" + r.text)
        print("thread1 completed")
    else:
        for i in range(0, 500):
            r = requests.get(url, headers=headers)
            print("status code: " + r.status_code + "response:" + r.text)
        time.sleep(60)
        for i in range(0, 1000):
            r = requests.get(url, headers=headers)
            print("status code: " + r.status_code + "response:" + r.text)
        print("thread2 completed")


#thread1 = Thread(target=call_endpoint_http(1))
#thread2 = Thread(target=call_endpoint_http(2))
