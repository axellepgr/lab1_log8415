import set_up_instances
import deploy_flask_app
import set_up_load_balancer
import set_up_target_group
import time
import boto3

# IMPORTANT before running the file download your private key

TARGET_GROUP_NUMBER = [1,2]
ec2_resource = boto3.resource('ec2')


# Setting the instances
print("Let set up the instances")
instance = set_up_instances.Instance()
instance.run_instances()
security_group_id, subnet_id, vpc_id = instance.get_ids()
time.sleep(10)

         
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
                nb_running_instances +=1
                print(str(id) + ' : ' + str(instance_type)+ ' is running.   (' + str(nb_running_instances) + '/9)')
            time.sleep(5)
print(id_list_m4)
print(id_list_t2)
            
# Setting up the targets groups
# tg_arn = []
# for tg_nb in TARGET_GROUP_NUMBER:
#     print("\n Deploying the target group number " + str(tg_nb))
#     targetGroup = None
#     if (tg_nb == 1):
#         targetGroup = set_up_target_group.TargetGroup(tg_nb, vpc_id, id_list_m4)
#     else:
#         targetGroup = set_up_target_group.TargetGroup(tg_nb, vpc_id, id_list_t2)
#     targetGroup.create_target_group()
#     targetGroup.register_target()
#     tg_arn.append(targetGroup.get_tg_arn())
#     time.sleep(20)

# # Setting up the load balancer
# print("\nDeploying the load balancer")
# loadBalancer = set_up_load_balancer.LoadBalancer(security_group_id, subnet_id, tg_arn)
# loadBalancer.create_load_balancer()
# loadBalancer.create_listener()
# time.sleep(10)

# Deploying flask in all of the running instances
# print("\nDeploying the flask app")
# deploy_flask_app.deploy_and_setup_app()