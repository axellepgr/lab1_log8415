import boto3
import json
import sys


def get_running_instances():
    """
    This function returns the ids of the running instances.
    returns a list containing the IDs of the instances.
    """
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
    return instances_ids

def terminate_instance(id_list):
    for instanceID in id_list:
        boto3.resource('ec2').instances.filter(
            InstanceIds=[instanceID]).terminate()
        print('Instance ' + str(instanceID) + ' shutting down.')
        
def wait_for_instance_terminated(ids):
    print('Waiting for the instances to terminate...')
    waiter = boto3.client('ec2').get_waiter('instance_terminated')
    waiter.wait(
        InstanceIds=ids
    )
    print('Instances terminated.')
        
def delete_listener(listener_arn):
    boto3.client('elbv2').delete_listener(ListenerArn=listener_arn)
    print('Listener deleted.')
    
def delete_load_balancer(load_balancer_arn):
    boto3.client('elbv2').delete_load_balancer(
        LoadBalancerArn=load_balancer_arn)
    print('Load balancer deleted.')
    
def delete_target_group(tg_arn):
    boto3.client('elbv2').delete_target_group(TargetGroupArn=tg_arn)
    print('Target group '+ str(tg_arn) +' deleted.')
        
def shutdown_system(instances_ids, tg_arn, listener_arn, lb_arn):
    print('Shutting down system...')
    terminate_instance(instances_ids)
    delete_listener(listener_arn)
    delete_load_balancer(lb_arn)
    for arn in tg_arn:
        delete_target_group(arn)
    wait_for_instance_terminated(instances_ids)
    print('\n!!! Don\'t forget to delete the VPC !!!')
    # instanceClass.delete_vpc()
    # instanceClass.delete_security_group()
    
with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

lb_dns = json_object["lb_dns"]
id_list_m4 = json_object["id_list_m4"]
id_list_t2 = json_object["id_list_t2"]
tg_arns = json_object["tg_arns"]
listener_arn = json_object["listener_arn"]
lb_arn = json_object["lb_arn"]


while True:
    print('\nMenu :')
    print('    press \'i\' to get informations. ')
    print('    press \'q\' to quit. ')
    print('    press \'s\' to shutdown everything. ')
    line = input('> ')
    if (line == 'i'):
        print('\nRunning instances :')
        get_running_instances()
        print('\nLoad Balancer DNS address : ' + str(lb_dns))
    elif (line == 'q'):
        sys.exit()
    elif (line == 's'):
        shutdown_system(id_list_m4 + id_list_t2, tg_arns, listener_arn, lb_arn)
    elif (line == ''):
        continue
    else:
        print('Unknown commad.')