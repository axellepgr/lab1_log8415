import set_up_instances
import deploy_flask_app
import time

# IMPORTANT before running the file download your private key

# Setting the instances
# print("Let set up the instances")
# set_up_instances.run_instances()
# time.sleep(30)
# Deploying flask in all of the running instances
print("Deplying the flask app")
deploy_flask_app.deploy_and_setup_app()
