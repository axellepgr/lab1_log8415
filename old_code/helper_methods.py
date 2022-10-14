import boto3

AWS_REGION = "us-east-1"

# return the ids of the running instances
def get_running_instances():
    ec2_resource = boto3.resource('ec2')
    instances = (ec2_resource.instances).filter()
    nb_running_instances = 0
    id_list_m4 = []
    id_list_t2 = []
    for instance in instances:
        state = instance.state['Name']
        if (state == 'running'):
            id = instance.id
            instance_type = instance.instance_type
            if (instance_type == 'm4.large'):
                id_list_m4.append(id)
            else:
                id_list_t2.append(id)
            nb_running_instances += 1
            print(str(nb_running_instances) + '. ' + str(id) + ' : ' + str(instance_type) +
                ' is running.')
    instances_ids = id_list_m4 + id_list_t2
    return instances_ids, id_list_m4, id_list_t2
    
# return the ids of the running instances and their public IP    
def get_running_instances_and_ip():
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
