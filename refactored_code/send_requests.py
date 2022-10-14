import json
import requests
import threading
import time

with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
    openfile.close()

lb_dns = json_object["lb_dns"]


class myThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("Starting Thread " + str(self.threadID))
        call_endpoint_http(self.threadID)


def call_endpoint_http(nbr):
    url = "http://" + lb_dns
    headers = {'content-type': 'application'}
    print("starting to send requests using thread" + str(nbr))
    if nbr == 1:
        for i in range(0, 1000):
            r = requests.get(url, headers=headers)
            print("THREAD 1 : status code: " +
                  str(r.status_code) + ", response:" + r.text)
        print("thread1 completed")
    else:
        for i in range(0, 500):
            r = requests.get(url, headers=headers)
            print("THREAD 2 : status code: " +
                  str(r.status_code) + ", response:" + r.text)
        time.sleep(60)
        for i in range(0, 1000):
            r = requests.get(url, headers=headers)
            print("THREAD 2 : status code: " +
                  str(r.status_code) + ", response:" + r.text)
        print("thread2 completed")


thread1 = myThread(1)
thread2 = myThread(2)

thread1.start()
thread2.start()
