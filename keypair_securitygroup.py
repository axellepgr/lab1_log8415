# Create new key-pair or use existing one
# Create new security-group or using existing one
import boto3

def key_pair():

    answer = input('Have you a key_pair : (Yes/No)    ')
    if answer == 'No':
        name = input('Input name of your new key_pair : (Yes/No)    ')
        ec2_client = boto3.client("ec2")
        key_pair = ec2_client.create_key_pair(KeyName=name)
        return key_pair

    else: key_pair = input('input key-pair: ')
    return key_pair

def security_group():

    answer = input('Have you a security group: (Yes/No)   ')
    description = input('Add a brief description:    ')
    if answer == 'No':
        name = input('Input name of your new key_pair : (Yes/No)    ')
        ec2_client = boto3.client("ec2")
        security_group_name = ec2_client.create_security_group(GroupName=name, Description = description)
        return security_group_name

    else: security_group_name = input('input security_group:   ')
    return security_group_name

