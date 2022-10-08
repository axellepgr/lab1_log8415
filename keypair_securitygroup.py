# Create new key-pair or use existing one
# Create new security-group or using existing one
import boto3

def key_pair():

    answer = input('Do you have a key_pair : (Yes/No)    ')
    ec2_client = boto3.client("ec2")
    keypairs = ec2_client.describe_key_pairs()
    keypairs_name = [keypairs["KeyPairs"][i]['KeyName'] for i in range(len(keypairs["KeyPairs"]))]
    print('The key_pair already exist in your account AWS:', keypairs_name)

    if answer == 'No':
        name = input('Input the name of your new key_pair : (Yes/No)    ')
        if name in keypairs_name:
            return print("This name has already exist create new one !")
        else:
            key_pair_1 = ec2_client.create_key_pair(KeyName=name)
            return key_pair_1["KeyName"]

    else:
        existante_key = input('input key-pair: ')
        if existante_key in keypairs_name:
            print("Yes it's done !")
            return existante_key
        else:
            return print("This key_pair doesnt exist")

def security_group():

    answer = input('Do you have a security group: (Yes/No)   ')
    if answer == 'No':
        name = input('Input the name of your new key_pair : (Yes/No)    ')
        description = input('Add a brief description:    ')
        ec2_client = boto3.client("ec2")
        security_group_name = ec2_client.create_security_group(GroupName=name, Description=description)
        return security_group_name

    else: security_group_name = input('input security_group:   ')
    return security_group_name


