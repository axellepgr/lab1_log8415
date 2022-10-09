import set_up_instances
import deploy_flask_app
import set_up_load_balancer
import time

# IMPORTANT before running the file download your private key

# Setting the instances
print("Let set up the instances")
instance = set_up_instances.Instance()
instance.run_instances()
security_group_id, subnet_id = instance.get_ids()
time.sleep(30)

print("Deploying the load_balancer")
loadBalancer = set_up_load_balancer.LoadBalancer(security_group_id, subnet_id)
loadBalancer.create_load_balancer()
time.sleep(30)

# Deploying flask in all of the running instances
print("Deploying the flask app")
deploy_flask_app.deploy_and_setup_app()