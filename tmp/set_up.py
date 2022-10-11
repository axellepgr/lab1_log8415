import set_up_instances
import deploy_flask_app
import set_up_load_balancer
import set_up_target_group
import time

# IMPORTANT before running the file download your private key

TARGET_GROUP_NUMBER = [1, 2]

# Setting the instances
print("Let set up the instances")
instance = set_up_instances.Instance()
instance.run_instances()
security_group_id, subnet_id, vpc_id = instance.get_ids()
instances_details = instance.get_instance_infos()
time.sleep(30)

# Setting up the targets groups
tg_arn = []
for tg_nb in TARGET_GROUP_NUMBER:
    print("\n Deploying the target group number " + str(tg_nb))
    targetGroup = set_up_target_group.TargetGroup(
        tg_nb, vpc_id, instances_details['id'][tg_nb-1])
    targetGroup.create_target_group()
    targetGroup.register_target()
    tg_arn.append(targetGroup.get_tg_arn())
    time.sleep(20)

# Setting up the load balancer
print("\nDeploying the load balancer")
loadBalancer = set_up_load_balancer.LoadBalancer(
    security_group_id, subnet_id, tg_arn)
loadBalancer.create_load_balancer()
loadBalancer.create_listener()
time.sleep(10)

# Deploying flask in all of the running instances
print("\nDeploying the flask app")
deploy_flask_app.deploy_and_setup_app()
