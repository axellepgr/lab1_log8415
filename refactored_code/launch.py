import os

os.system("python set_up.py")
os.system("python deploy_flask_app.py")
os.system("cloudwatch/cloudwatch.py")
