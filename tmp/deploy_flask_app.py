import helper_methods
import paramiko
import time
import os


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
                    username='ubuntu', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)


envsetup = """
#!/bin/bash
yes | sudo apt-get update
yes | sudo apt install python3-pip
yes | sudo apt install python3.10-venv
mkdir flask_application && cd flask_application
sudo python3 -m venv venv
sudo source venv/bin/activate
yes | sudo pip install Flask
cat <<EOF > app.py
from flask import Flask
app = Flask(__name__)
@app.route("/")
def my_app():
    return "Your small app is working"
EOF
"""

deploy = """
cd flask_application
export flask_application=app.py
nohup sudo flask run --host=0.0.0.0 --port=80 1>/dev/null 2>/dev/null &
"""


def deploy_and_setup_app():
    running_instances = helper_methods.get_running_instances()
    for instance in running_instances:
        ip_address = instance[1]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_connect_with_retry(ssh, ip_address, 0)
        stdin, stdout, stderr = ssh.exec_command(envsetup)
        print('env setup done \n stdout:', stdout.read())
        stdin, stdout, stderr = ssh.exec_command(deploy)
        print('deployment done \n')
        ssh.close()
        time.sleep(5)
