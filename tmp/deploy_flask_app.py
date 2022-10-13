import helper_methods
import paramiko
import time
import os
import sys
import threading


def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    current_directory = os.getcwd()
    privkey = paramiko.RSAKey.from_private_key_file(
        'labsuser.pem')
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username="ubuntu", pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)


def envsetup(instanceID):
    str_instanceID = str(instanceID)
    return """
#!/bin/bash
yes | sudo apt-get update
yes | sudo apt install python3-pip
yes | sudo apt install python3.10-venv
mkdir flask_application && cd flask_application
sudo python3 -m venv venv
sudo source venv/bin/activate
yes | sudo pip install Flask
yes | pip install requests
cat <<EOF > app.py
from flask import Flask
import requests
app = Flask(__name__)
@app.route("/")
def my_app():
    return "Your small app is working on instande id:" + " """ + str_instanceID + """ "
EOF
"""


deploy = """
cd flask_application
export flask_application=app.py
nohup sudo flask run --host=0.0.0.0 --port=80 1>/dev/null 2>/dev/null &
"""


class myThread (threading.Thread):
    def __init__(self, instance, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.instance = instance

    def run(self):
        print("Deploying using Thread " + str(self.threadID))
        deploy_using_threads(self.instance, self.threadID)


def deploy_using_threads(instance, instance_nb):
    ip_address = instance[1]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip_address, 0)
    stdin, stdout, stderr = ssh.exec_command(envsetup(instance[0]))
    old_stdout = sys.stdout
    log_file = open("logfile.log", "w")
    print('env setup done \n stdout:', stdout.read(), file=log_file)
    log_file.close()
    #print('env setup done \n stdout:', stdout.read())
    stdin, stdout, stderr = ssh.exec_command(deploy)
    print('Deployment done for instance number ' + str(instance_nb) + '\n')
    ssh.close()


def deploy_and_setup_app():
    running_instances = helper_methods.get_running_instances_and_ip()
    instance_nb = 0
    t = {}
    for instance in running_instances:
        instance_nb += 1
        t["thread" + str(instance_nb)] = myThread(instance, instance_nb)
        t["thread" + str(instance_nb)].start()
    t["thread1"].join()
    t["thread1"].join()
