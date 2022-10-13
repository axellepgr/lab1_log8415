import os
import json

# retreive instance IDs
with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

IDs = json_object["id_list_m4"] + json_object["id_list_t2"]

# enable detailed monitoring for the EC2 instances
for id in IDs:
    os.system("aws ec2 monitor-instances --instance-ids " + id)

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
