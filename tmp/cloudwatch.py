import os
#from datetime import datetime
# from sqlite3 import Timestamp

# # datetime object containing current date and time
#now = datetime.now()
#timestamp_now = now.strftime("%Y-%m-%d" + "T" + "%H:%M:%S")
# minutes = now.minute - 1
# timestamp_now_1minbefore = now.strftime(
#     "%Y-%m-%d" + "T" + "%H:" + str(minutes)+":%S")
# print(timestamp_now)
# print(timestamp_now_1minbefore)


# enable detailed monitoring for the EC2 instances

os.system("aws ec2 unmonitor-instances --instance-ids i-09fb0f809f429f5d5")

# # list the available metrics for the EC2 instances
# #os.system("aws cloudwatch list-metrics --namespace AWS/EC2")

# # list the available metrics for a specifi EC2 instance
# #os.system("aws cloudwatch list-metrics --namespace AWS/EC2 --dimensions Name=InstanceId,Value=i-05b81223b60a5b5f5")

# # show CPU utilization of a specific EC2 instance
# os.system("aws cloudwatch list-metrics --namespace AWS/EC2 --metric-name CPUUtilization Name=InstanceId,Value=i-05b81223b60a5b5f5")

# show CPU utilization of a specific EC2 instance using the specified period and time interval
# os.system("aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization  --period 3600 \
# --statistics Maximum --dimensions Name=InstanceId,Value=i-05b81223b60a5b5f5 \
# --start-time "+timestamp_now_1minbefore + " --end-time " + timestamp_now)
