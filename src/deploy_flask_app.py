import paramiko
import time
import sys
import threading
import boto3

AWS_REGION = 'us-east-1'


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


def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
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


def get_id_ips():
    ec2_client = boto3.client("ec2", region_name=AWS_REGION)
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")
    ids = []
    print("Found the following instances: \n")
    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            ids.append((instance_id, public_ip))
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")
    print("\n")
    return ids


class myThread (threading.Thread):
    def __init__(self, id_ip, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.id_ip = id_ip

    def run(self):
        print("Deploying using Thread " + str(self.threadID))
        deploy_using_threads(self.id_ip, self.threadID)


def deploy_using_threads(id_ip, instance_nb):
    ip_address = id_ip[1]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip_address, 0)
    stdin, stdout, stderr = ssh.exec_command(envsetup(id_ip[0]))
    old_stdout = sys.stdout
    log_file = open("logfile.log", "w")
    print('env setup done \n stdout:', stdout.read(), file=log_file)
    log_file.close()
    #print('env setup done \n stdout:', stdout.read())
    stdin, stdout, stderr = ssh.exec_command(deploy)
    print('Deployment done for instance number ' + str(instance_nb) + '\n')
    ssh.close()


def deploy_app():
    instances_IDs_IPs = get_id_ips()
    instance_count = 0
    t = {}
    for id_ip in instances_IDs_IPs:
        instance_count += 1
        t["thread" + str(instance_count)] = myThread(id_ip, instance_count)
        t["thread" + str(instance_count)].start()
    t["thread1"].join()
    t["thread2"].join()


print("\n############### Deploying Flask App ###############\n")

deploy_app()

print("Flask App Deployed On All EC2 Instances!")
