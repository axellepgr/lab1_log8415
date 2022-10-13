from logging import shutdown
import set_up_instances
import deploy_flask_app
import set_up_load_balancer
import set_up_target_group
import helper_methods
import time
import boto3
import sys
import json

# IMPORTANT before running the file download your private key

TARGET_GROUP_NUMBER = [1, 2]

# Setting the instances


def setup_instance():
    print("Let set up the instances")
    instanceClass = set_up_instances.Instance()
    instanceClass.run_instances()
    time.sleep(10)
    security_group_id, subnet_id, vpc_id = instanceClass.get_ids()
    return security_group_id, subnet_id, vpc_id, instanceClass

# Wait for every instance to be running


def wait_instances():
    instances = (boto3.resource('ec2').instances).filter()
    nb_running_instances = 0
    id_list_m4 = []
    id_list_t2 = []
    while (nb_running_instances < 9):
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

# Setting up the targets groups


def setup_tagret_group(vpc_id, id_list_m4, id_list_t2):
    targetGroupClass = None
    tg_arn = []
    for tg_nb in TARGET_GROUP_NUMBER:
        print("\nDeploying the target group number " + str(tg_nb))
        if (tg_nb == 1):
            targetGroupClass = set_up_target_group.TargetGroup(
                tg_nb, vpc_id, id_list_m4)
        else:
            targetGroupClass = set_up_target_group.TargetGroup(
                tg_nb, vpc_id, id_list_t2)
        tg_arn.append(targetGroupClass.setup())
    return tg_arn, targetGroupClass

# Setting up the load balancer


def setup_load_balancer(security_group_id, subnet_id, tg_arn):
    print("\nDeploying the load balancer")
    loadBalancerClass = set_up_load_balancer.LoadBalancer(
        security_group_id, subnet_id, tg_arn)
    lb_dns = loadBalancerClass.setup()
    return lb_dns, loadBalancerClass

# Deploying flask in all of the running instances


def deploy_flask():
    print("\nDeploying the flask app")
    deploy_flask_app.deploy_and_setup_app()


def shutdown_system(instances_ids, tg_arn, instanceClass, loadBalancerClass, targetGroupClass):
    print('Shutting down system...')
    instanceClass.terminate_instance(instances_ids)
    loadBalancerClass.delete_listener()
    loadBalancerClass.delete_load_balancer()
    for arn in tg_arn:
        targetGroupClass.delete_target_group(arn)
    instanceClass.wait_for_instance_terminated(instances_ids)
    instanceClass.delete_security_group()
    print('\n!!! Don\'t forget to delete the VPC !!!')


# START
security_group_id, subnet_id, vpc_id, instanceClass = setup_instance()
id_list_m4, id_list_t2 = wait_instances()
tg_arn, targetGroupClass = setup_tagret_group(vpc_id, id_list_m4, id_list_t2)
lb_dns, loadBalancerClass = setup_load_balancer(
    security_group_id, subnet_id, tg_arn)

# Data to be written
dictionary = {
    "vpc_id": vpc_id,
    "id_list_m4": id_list_m4,
    "id_list_t2": id_list_t2,
    "lb_dns": lb_dns
}

# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("collected_data.json", "w") as outfile:
    outfile.write(json_object)

deploy_flask()

print("Flask app deployed on all instance!")


while True:
    print('\nMenu :')
    print('    press \'i\' to get informations. ')
    print('    press \'q\' to quit. ')
    print('    press \'s\' to shutdown everything. ')
    line = input('> ')
    if (line == 'i'):
        print('\nRunning instances :')
        helper_methods.get_running_instances()
        print('\nLoad Balancer DNS address : ' + str(lb_dns))
    elif (line == 'q'):
        sys.exit()
    elif (line == 's'):
        shutdown_system(id_list_m4 + id_list_t2, tg_arn,
                        instanceClass, loadBalancerClass, targetGroupClass)
    elif (line == ''):
        continue
    else:
        print('Unknown commad.')
