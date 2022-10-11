import set_up_instances
import deploy_flask_app
import set_up_load_balancer
import set_up_target_group
import time
import boto3
import sys

# IMPORTANT before running the file download your private key

TARGET_GROUP_NUMBER = [1, 2]
ec2_resource = boto3.resource('ec2')
instances_ids = []

# Setting the instances
print("Let set up the instances")
instanceClass = set_up_instances.Instance()
instanceClass.run_instances()
security_group_id, subnet_id, vpc_id = instanceClass.get_ids()
time.sleep(10)

# Get the ids of the running instances
instances = (ec2_resource.instances).filter()
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
instances_ids = id_list_m4 + id_list_t2

# Setting up the targets groups
tg_arn = []
targetGroupClass = None
for tg_nb in TARGET_GROUP_NUMBER:
    print("\nDeploying the target group number " + str(tg_nb))
    if (tg_nb == 1):
        targetGroupClass = set_up_target_group.TargetGroup(
            tg_nb, vpc_id, id_list_m4)
    else:
        targetGroupClass = set_up_target_group.TargetGroup(
            tg_nb, vpc_id, id_list_t2)
    targetGroupClass.create_target_group()
    targetGroupClass.register_target()
    tg_arn.append(targetGroupClass.get_tg_arn())
    time.sleep(5)

# Setting up the load balancer
print("\nDeploying the load balancer")
loadBalancerClass = set_up_load_balancer.LoadBalancer(
    security_group_id, subnet_id, tg_arn)
loadBalancerClass.create_load_balancer()
loadBalancerClass.create_listener()
lb_arn = loadBalancerClass.get_lb_arn()
lb_dns = loadBalancerClass.get_lb_dns()
time.sleep(10)

# Deploying flask in all of the running instances
print("\nDeploying the flask app")
deploy_flask_app.deploy_and_setup_app()


while True:
    print('\nMenu :')
    print('    press \'i\' to get informations. ')
    print('    press \'q\' to quit. ')
    print('    press \'s\' to shutdown everything. ')
    line = input('> ')
    if (line == 'i'):
        print('Running instances :')
        print('m4.large :')
        print(id_list_m4)
        print('t2.large :')
        print(id_list_t2)
        print('\nLoad Balancer DNS address : ' + str(lb_dns))
    elif (line == 'q'):
        sys.exit()
    elif (line == 's'):
        print('Shutting down system...')
        instanceClass.terminate_instance(instances_ids)
        loadBalancerClass.delete_listener()
        loadBalancerClass.delete_load_balancer()
        for arn in tg_arn:
            targetGroupClass.delete_target_group(arn)
        print('\n!!! Don\'t forget to delete the VPC !!!')
    elif (line == ''):
        continue
    else:
        print ('Unknown commad.')
