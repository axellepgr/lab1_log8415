# Create EC2 instances using Python BOTO3
import boto3
import keypair_securitygroup as ks
resource_ec2 = boto3.resource('ec2')

key_pair_name = ks.key_pair()
while key_pair_name == None:
    key_pair_name = ks.key_pair()
security_group = ks.security_group()

availabilityZone = ['us-east-1a', 'us-east-1b']
instance_type = ["m4.large", "t2.large"]
image_id = ["ami-026b57f3c383c2eec", "ami-0f1ee03d06c4c659c"]

def create_ec2_instance(
        key_pair=key_pair_name,
        security_group=security_group,
        availabilityZone= availabilityZone[0],
        instance_type = instance_type[0],
        num_instances = 1,
        image_id = image_id[0]):

    print("Creating EC2 instance")

    resource_ec2 = boto3.client('ec2')
    resource_ec2.run_instances(
        ImageId=image_id,
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType=instance_type,
        KeyName=key_pair,
        SecurityGroupIds=[security_group],
        Placement={
                    'AvailabilityZone': availabilityZone,
                }
        )

    instanceIDs = resource_ec2.describe_instances()
    return instanceIDs



# First call
create_ec2_instance(key_pair=key_pair_name,
        security_group=security_group,
        availabilityZone= availabilityZone[0],
        instance_type = instance_type[0],
        num_instances = 5,
        image_id = image_id[0])

# Second call
instanceIDs = create_ec2_instance(key_pair=key_pair_name,
        security_group=security_group,
        availabilityZone= availabilityZone[1],
        instance_type = instance_type[1],
        num_instances = 4,
        image_id = image_id[0])



data = instanceIDs["Reservations"]
print(data[1]["Instances"])
data_instances = []
for i in range(len(data)):
    data1 = data[i]["Instances"]
    print(f"Istances Id is :{data1[0]['InstanceId']}")
    data_instances.append(data1[0]['InstanceId'])

# Terminate instances
def terminate(data_instances):
    print('Terminate instance...')
    for instanceIDs in data_instances:
        resource_ec2.instances.filter(InstanceIds=[instanceIDs]).terminate()
#terminate(data_instances)

