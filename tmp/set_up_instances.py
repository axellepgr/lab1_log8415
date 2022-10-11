import boto3
from botocore.exceptions import ClientError
import os
import paramiko
import time

AWS_REGION = 'us-east-1'
AVAILABILITY_ZONE = ['us-east-1a', 'us-east-1b']
INSTANCE_TYPE = ["m4.large", "t2.large"]
KEY_PAIR_NAME = "vockey"
# AMI_ID = ["ami-08c40ec9ead489470", "ami-0f1ee03d06c4c659c"]
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
class Instance:
    
    def __init__(self):
        self.ec2_client = boto3.client("ec2", region_name=AWS_REGION)
        self.ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)
        self.security_group_id = None 
        self.subnet_id = None
        self.vpc_id = None

    def create_key_pair(self):
        print("Generating a key pair")
        key_pair = self.ec2_client.create_key_pair(KeyName=KEY_PAIR_NAME)

        private_key = key_pair["KeyMaterial"]

        # write private key to file with 400 permissions
        with os.fdopen(os.open("aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)

    def security_group(self):

        sg_name = "TP1"

        # Creating a new vpc
        vpc_response = self.ec2_client.create_vpc(CidrBlock='172.31.0.0/20')
        vpc = self.ec2_resource.Vpc(vpc_response["Vpc"]["VpcId"])
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc2"}])
        vpc.wait_until_available()
        self.ec2_client.modify_vpc_attribute(
            VpcId=vpc_response["Vpc"]["VpcId"], EnableDnsSupport={'Value': True})
        self.ec2_client.modify_vpc_attribute(
            VpcId=vpc_response["Vpc"]["VpcId"], EnableDnsHostnames={'Value': True})
        self.vpc_id = vpc.id

        # Create and Attach the Internet Gateway
        ig_response = self.ec2_client.create_internet_gateway()
        ig_id = ig_response["InternetGateway"]["InternetGatewayId"]
        vpc.attach_internet_gateway(InternetGatewayId=ig_id)
        print(ig_id)

        # create a route table and a public route table linked to Gateway
        routetable = vpc.create_route_table()
        routetable.create_route(
            DestinationCidrBlock='0.0.0.0/0', GatewayId=ig_id)

        # Create a Subnet with public IP on launch
        subnet = vpc.create_subnet( AvailabilityZone=AVAILABILITY_ZONE[0], CidrBlock='172.31.0.0/24')
        self.ec2_client.modify_subnet_attribute(
            SubnetId=subnet.id,
            MapPublicIpOnLaunch={'Value': True},
        )
        self.subnet_id=[subnet.id]
        routetable.associate_with_subnet(SubnetId=self.subnet_id[0])
        
        # Create a second Subnet with public IP on launch
        subnet = vpc.create_subnet( AvailabilityZone=AVAILABILITY_ZONE[1], CidrBlock='172.31.1.0/24')
        self.ec2_client.modify_subnet_attribute(
            SubnetId=subnet.id,
            MapPublicIpOnLaunch={'Value': True},
        )
        self.subnet_id.append(subnet.id)
        routetable.associate_with_subnet(SubnetId=self.subnet_id[1])
        
        # create a secutrity group with the new vpc
        response = self.ec2_client.create_security_group(GroupName=sg_name,
                                            Description='SG_basic',
                                            VpcId=vpc.id)
        self.security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (self.security_group_id, vpc.id))

        # setting ingress to allow http/https and ssh connections
        data = self.ec2_client.authorize_security_group_ingress(
            GroupId=self.security_group_id,
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
        print('Ingress Successfully Set.')


    def run_instances(self):
        self.security_group()
        instances = self.ec2_client.run_instances(
            MinCount=5,
            MaxCount=5,
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE[0],
            KeyName=KEY_PAIR_NAME,
            NetworkInterfaces=[{
                "DeviceIndex": 0,
                "Groups": [self.security_group_id],
                "AssociatePublicIpAddress": True,
                "SubnetId": self.subnet_id[0]
            }]
        )

        # 2nd instance
        instances = self.ec2_client.run_instances(
            MinCount=4,
            MaxCount=4,
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE[1],
            KeyName=KEY_PAIR_NAME,
            NetworkInterfaces=[{
                "DeviceIndex": 0,
                "Groups": [self.security_group_id],
                "AssociatePublicIpAddress": True,
                "SubnetId": self.subnet_id[1]
            }]
        )
        
    def terminate_instance(self, id_list):
        for instanceID in id_list:
            self.ec2_resource.instances.filter(InstanceIds=[instanceID]).terminate()
            print('Instance '+ str(instanceID) +' terminated.')

    def get_ids(self):
        return self.security_group_id, self.subnet_id, self.vpc_id