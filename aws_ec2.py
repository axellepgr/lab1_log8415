# Create EC2 instances using Python BOTO3
import boto3
import keypair_securitygroup as confi

confi.key_pair()

"""
def create_key_pair():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    key_pair = ec2_client.create_key_pair(KeyName="ec2-key-pair")

    private_key = key_pair["KeyMaterial"]

    # write private key to file with 400 permissions
    with os.fdopen(os.open("/tmp/aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(private_key)
create_key_pair()

"""
availabilityZone = 'us-east-1b'
resource_ec2 = boto3.resource('ec2')
data_instances = []
def create_ec2_instance():
        print("Creating EC2 instance")
        resource_ec2 = boto3.client('ec2')
        """
        resource_ec2.run_instances(
            ImageId="ami-0f1ee03d06c4c659c",
            MinCount=1,
            MaxCount=2,
            InstanceType="m4.large",
            KeyName="vockey",
            Placement={
                'AvailabilityZone': availabilityZone,
            }

        )
        """

        instanceIDs = resource_ec2.describe_instances()

        print(classic_address_iterator)

        return instanceIDs
classic_address_iterator = resource_ec2.classic_addresses.all()
instanceIDs = create_ec2_instance()
#print(instanceIDs.keys())
data = instanceIDs["Reservations"][0]
#print('data', data)
data1 = data["Instances"]
#print('data1', data1)
#print(len(data1))
for i in range(len(data1)):
    print(f"Istances Id is :{data1[i]['InstanceId']}")
    data_instances.append(data1[i]['InstanceId'])
print(data_instances)


# Terminate instances
#instanceIDs = ['i-05687a9ebbfbe2856']
def terminate(instanceIDs):
    print('Terminate instance...')
    resource_ec2.instances.filter(InstanceIds=instanceIDs).terminate()
#terminate(instanceIDs)

