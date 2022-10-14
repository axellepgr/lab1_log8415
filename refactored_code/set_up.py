import boto3
import time
import json

TARGET_GROUP_NUMBER = [1, 2]
AWS_REGION = 'us-east-1'
AVAILABILITY_ZONE = ['us-east-1a', 'us-east-1b']
INSTANCE_TYPE = ["m4.large", "t2.large"]
NB_INSTANCES = 2
KEY_PAIR_NAME = "vockey"
AMI_ID = "ami-08c40ec9ead489470"


ec2_client = boto3.client("ec2", region_name=AWS_REGION)
elbv2_client = boto3.client('elbv2')
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)


# create VPC


def create_vpc(ec2_client, ec2_resource):
    """
    Creates a new VPC
    """
    vpc_response = ec2_client.create_vpc(CidrBlock='172.31.0.0/20')
    vpc = ec2_resource.Vpc(vpc_response["Vpc"]["VpcId"])
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "VPC_LAB1"}])
    vpc.wait_until_available()
    ec2_client.modify_vpc_attribute(
        VpcId=vpc_response["Vpc"]["VpcId"], EnableDnsSupport={'Value': True})
    ec2_client.modify_vpc_attribute(
        VpcId=vpc_response["Vpc"]["VpcId"], EnableDnsHostnames={'Value': True})

    return vpc, vpc.id


def create_and_attach_igw(vpc):
    """
    Creates and attaches an internet gateway to the vpc
    Returns the gateway ID
    """
    ig_response = ec2_client.create_internet_gateway()
    igw_id = ig_response["InternetGateway"]["InternetGatewayId"]

    print("created internet gateway with id: " + igw_id)

    vpc.attach_internet_gateway(InternetGatewayId=igw_id)

    return igw_id


def create_route_table(vpc, igw_id):
    """
    Creates a route table for the VPC
    """
    routetable = vpc.create_route_table()
    routetable.create_route(
        DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
    return routetable


def create_subnets(vpc, routetable, cidrblock, AZ):
    """
    Creates a subnet for the VPC and adds it to its route table.
    cidrblock : is the desired subnet in the CIDR notation.
    AZ : is the desired availability zone (needs to be different for each subnet).
    Returns the subnet ID
    """
    subnet = vpc.create_subnet(
        AvailabilityZone=AZ, CidrBlock=cidrblock)
    ec2_client.modify_subnet_attribute(
        SubnetId=subnet.id,
        MapPublicIpOnLaunch={'Value': True},
    )
    routetable.associate_with_subnet(SubnetId=subnet.id)
    return subnet.id


def create_sg(vpcID):
    """
    This function creates a new security group for the VPC.
    vpcID : is the ID of the concerned VPC.
    Returns the security group ID.
    """
    response = ec2_client.create_security_group(GroupName="LAB1",
                                                Description='SG_basic',
                                                VpcId=vpcID)
    security_group_id = response['GroupId']
    ec2_client.authorize_security_group_ingress(
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
    print('Ingress rules successfully set!')
    return security_group_id


def create_ec2_instances(nbr, type, sg_id, subnet_id):
    """
    This function creates EC2 instances.
    nbr : is the desired number of instances to be created.
    type : is either 0 for m4.large instances ot 1 for t2.large instances.
    sg_id : is the ID of the security group that you wish your instaces to follow.
    subnet_id : is the subnet where you instances will reside.
    """
    ec2_client.run_instances(
        MinCount=nbr,
        MaxCount=nbr,
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE[type],
        KeyName=KEY_PAIR_NAME,
        NetworkInterfaces=[{
            "DeviceIndex": 0,
            "Groups": [sg_id],
            "AssociatePublicIpAddress": True,
            "SubnetId": subnet_id
        }]
    )


def wait_instances():
    """
    This function waits for the EC2 instances to become available.
    returns two lists containing the IDs of the instances for each type.
    """
    instances = (boto3.resource('ec2').instances).filter()
    nb_running_instances = 0
    id_list_m4 = []
    id_list_t2 = []
    while (nb_running_instances < NB_INSTANCES):
        for instance in instances:
            state = instance.state['Name']
            if (state == 'running'):
                id = instance.id
                if id not in id_list_m4 and id not in id_list_t2:
                    instance_type = instance.instance_type
                    if (instance_type == 'm4.large'):
                        id_list_m4.append(id)
                    else:
                        id_list_t2.append(id)
                    nb_running_instances += 1
                    print(str(id) + ' : ' + str(instance_type) +
                          ' is running.   (' + str(nb_running_instances) + '/9)')
        time.sleep(5)
    return id_list_m4, id_list_t2


def setup_target_groups(vpc_id):
    """
    This function creates target groups.
    vpc_id : is the IDs of the VPC concerned.
    """
    tg_arns = []
    for tg_nb in TARGET_GROUP_NUMBER:
        print("\nDeploying the target group number " + str(tg_nb))
        print('Creating target group ' + str(tg_nb) + '...')
        response = elbv2_client.create_target_group(
            Name=f'target-group-{tg_nb}',
            Protocol='HTTP',
            ProtocolVersion='HTTP1',
            Port=80,
            VpcId=vpc_id,
            HealthCheckEnabled=True,
            HealthCheckPath='/',
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=6,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            TargetType='instance',
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            IpAddressType='ipv4'
        )
        target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
        tg_arns.append(target_group_arn)
        print('Target group ' + str(tg_nb) + ' created.')
    return tg_arns


def register_targets(tg_arn, instances_ids):
    """
    This function registers the targets (EC2 instaces) with the desired target group.
    tg_arn : is the ARN of the desired target group.
    instances_ids : is a list which contains the IDs of the targets (EC2 instances).
    """
    elbv2_client.register_targets(
        TargetGroupArn=tg_arn,
        Targets=[
            {
                'Id': id,
                'Port': 80
            } for id in instances_ids
        ]
    )
    print('Instance targets ' + str(instances_ids) +
          ' are registered in target group with arn ' + str(tg_arn) + '.')


def setup_load_balancer(sg_id, subnets_id, tg_arns):
    """
    This function sets up the load balancer.
    sg_id : is the ID of the desired security group,
    subnets_id : is a list which contains at least to subnet IDs,
    tg_arns : is a list which contains at least two ARNs of the target groups
    """
    response = elbv2_client.create_load_balancer(
        Name='Load-balancer-1',
        Subnets=subnets_id,
        SecurityGroups=[sg_id],
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4',
    )
    lb_dns = response['LoadBalancers'][0]['DNSName']
    lb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    print('Load balancer created at : ' + lb_dns)
    print("Creating listener for the load balancer...")
    response = elbv2_client.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'ForwardConfig': {
                        'TargetGroups': [
                            {
                                'TargetGroupArn': str(tg_arns[0]),
                                'Weight': 2
                            },
                            {
                                'TargetGroupArn': str(tg_arns[1]),
                                'Weight': 1
                            }
                        ],
                }
            },
        ],
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
    )
    listener_arn = response['Listeners'][0]['ListenerArn']
    print("Listener created!")
    return lb_dns, lb_arn, listener_arn

# START


print("\n############### SETTING UP THE SYSTEM ###############\n")

print("Creating the VPC...")
vpc, vpc_id = create_vpc(ec2_client, ec2_resource)
print("VPC created!\n")

print("Creating the Internet Gateway and attaching it to the VPC...")
igw_id = create_and_attach_igw(vpc)
print("Internet Gateway created!\n")

print("Creating a route table for the VPC...")
routetable = create_route_table(vpc, igw_id)
print("Route table created!\n")

print("Creating the subnets...")
subnets_id = []
subnet_id1 = create_subnets(
    vpc, routetable, "172.31.0.0/24", AVAILABILITY_ZONE[0])
subnet_id2 = create_subnets(
    vpc, routetable, "172.31.1.0/24", AVAILABILITY_ZONE[1])
subnets_id.append(subnet_id1)
subnets_id.append(subnet_id2)
print("Subnets created!\n")

print("Creating the security group for the vpc...")
sg_id = create_sg(vpc_id)
print("Security group created!\n")

print("Creating the EC2 instances...")
create_ec2_instances(1, 0, sg_id, subnets_id[0])
create_ec2_instances(1, 1, sg_id, subnets_id[1])
print("EC2 instances created!\n")

print("Waiting for the EC2 instaces to become available...")
m4_IDs, t2_IDs = wait_instances()
print("EC2 instances are available!\n")

print("Creating the target groups and registering the instances...")
tg_arns = setup_target_groups(vpc_id)
register_targets(tg_arns[0], m4_IDs)
register_targets(tg_arns[1], t2_IDs)
print("Instances registered with the target groups!\n")

print("Setting up the load balancer...")
lb_dns, lb_arn, listener_arn = setup_load_balancer(sg_id, subnets_id, tg_arns)
print("Load balancer set up!\n")

# A dictionary to hold the resources IDs to store in a .json file for the other scripts to use

dictionary = {
    "vpc_id": vpc_id,
    "igw_id": igw_id,
    "subnets_id": subnets_id,
    "sg_id": sg_id,
    "id_list_m4": m4_IDs,
    "id_list_t2": t2_IDs,
    "tg_arns": tg_arns,
    "lb_dns": lb_dns,
    "lb_arn": lb_arn,
    "listener_arn": listener_arn
}

# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to collected_data.json
with open("collected_data.json", "w") as outfile:
    outfile.write(json_object)

print("Waiting for the load balancer to become in the active status...")
time.sleep(180)
print("Finished waiting.\n")
print("\n############### DONE SETTING UP THE SYSTEM ###############\n")
