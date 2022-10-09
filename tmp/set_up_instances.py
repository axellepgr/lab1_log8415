import boto3
from botocore.exceptions import ClientError
import os
import paramiko
import time

AWS_REGION = "us-east-1"
KEY_PAIR_NAME = "vockey"
AMI_ID = "ami-08c40ec9ead489470"
BASH_DEPLOY_APP = """
#!/bin/bash
sudo apt-get update -y
sudo apt-get install python3-pip -y
sudo apt install python3-venv -y
mkdir flask_application && cd flask_application
sudo python3 -m venv venv
source venv/bin/activate
yes | sudo pip install Flask
cat <<EOF > app.py
from flask import Flask
app = Flask(__name__)
@app.route("/")
def my_app():
    return "Your small app is working"
EOF
export flask_application=app.py
nohup sudo flask run --host=0.0.0.0 --port=80 &
exit
"""


def create_key_pair():
    print("Generating a key pair")
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    key_pair = ec2_client.create_key_pair(KeyName=KEY_PAIR_NAME)

    private_key = key_pair["KeyMaterial"]

    # write private key to file with 400 permissions
    with os.fdopen(os.open("aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(private_key)


def security_group():

    sg_name = "TP1"
    ec2 = boto3.client("ec2", region_name=AWS_REGION)
    ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)

    # Creating a new vpc
    vpc_response = ec2.create_vpc(CidrBlock='172.31.0.0/20')
    vpc = ec2_resource.Vpc(vpc_response["Vpc"]["VpcId"])
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc2"}])
    vpc.wait_until_available()
    ec2.modify_vpc_attribute(
        VpcId=vpc_response["Vpc"]["VpcId"], EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(
        VpcId=vpc_response["Vpc"]["VpcId"], EnableDnsHostnames={'Value': True})
    print(vpc_response["Vpc"]["VpcId"])

    # Create and Attach the Internet Gateway
    ig_response = ec2.create_internet_gateway()
    ig_id = ig_response["InternetGateway"]["InternetGatewayId"]
    vpc.attach_internet_gateway(InternetGatewayId=ig_id)
    print(ig_id)

    # create a route table and a public route table linked to Gateway
    routetable = vpc.create_route_table()
    routetable.create_route(
        DestinationCidrBlock='0.0.0.0/0', GatewayId=ig_id)

    # Create a Subnet with public IP on launch
    subnet = vpc.create_subnet(CidrBlock='172.31.0.0/20')
    ec2.modify_subnet_attribute(
        SubnetId=subnet.id,
        MapPublicIpOnLaunch={'Value': True},
    )
    print(subnet.id)
    routetable.associate_with_subnet(SubnetId=subnet.id)

    # create a secutrity groupe with the new vpc
    response = ec2.create_security_group(GroupName=sg_name,
                                         Description='SG_basic',
                                         VpcId=vpc.id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc.id))

    # setting ingress to allow http/https and ssh connections
    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)
    # we return the new sg and the subnet associated to the new vpc
    return security_group_id, subnet.id


def run_instances():
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    security_group_id, subnet_id = security_group()
    instances = ec2_client.run_instances(
        MinCount=1,
        MaxCount=1,
        ImageId=AMI_ID,
        InstanceType="m4.large",
        KeyName=KEY_PAIR_NAME,
        NetworkInterfaces=[{
            "DeviceIndex": 0,
            "Groups": [security_group_id],
            "AssociatePublicIpAddress": True,
            "SubnetId": subnet_id
        }]
    )

    for instance in instances:
        print(f'EC2 instance "{instance}" has been launched')
