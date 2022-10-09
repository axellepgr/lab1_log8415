import boto3

AWS_REGION = "us-east-1"


def get_running_instances():
    ec2_client = boto3.client("ec2", region_name=AWS_REGION)
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")
    ids = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            ids.append((instance_id, public_ip))
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

    return ids


def terminate_instace():
    ec2_client = boto3.client("ec2", region_name=AWS_REGION)
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["stopped", "running"],
        }
    ]).get("Reservations")
    ids = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            ids.append(instance_id)
            print(f"{instance_id}, {instance_type}")
    if len(ids) > 0:
        response = ec2_client.terminate_instances(InstanceIds=ids)
        print(response)
    else:
        print("no instance to terminate")
