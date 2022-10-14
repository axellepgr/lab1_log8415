import json
import os
import time
import datetime
import boto3
from set_up_cloudwatch import CloudWatchWrapper

with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
    openfile.close()

m4_IDs = json_object["id_list_m4"]
t2_IDs = json_object["id_list_t2"]
lb_arn = json_object["lb_arn"]

print("\n############### CloudWatch ###############\n")
print("Activating detailed monitoring for all EC2 instances")

for id in m4_IDs + t2_IDs:
    os.system("aws ec2 monitor-instances --instance-ids " + id)

# print("Sending GET requests...")
# os.system("python send_requests.py")

# print("Waiting 1 minute before getting the CloudWatch metrics")
# time.sleep(60)


start = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
end = datetime.datetime.utcnow()
period = 60
cw_wrapper = CloudWatchWrapper(boto3.resource('cloudwatch'))

# Metrics for cluster 1 (m4.large)
for id_m4 in m4_IDs:
    cpu_utilization = cw_wrapper.get_metric_statistics('AWS/EC2', 'CPUUtilization', [{'Name': 'InstanceId', 'Value': id_m4}],
                                                       start, end, period, ['Minimum', 'Maximum', 'Average'])

    print(f"CPU Utilization for cluster 1, instance: {id_m4}")
    print(cpu_utilization['Datapoints'])

# Metrics for cluster 2 (t2.large)
for id_t2 in t2_IDs:
    cpu_utilization = cw_wrapper.get_metric_statistics('AWS/EC2', 'CPUUtilization', [{'Name': 'InstanceId', 'Value': id_t2}],
                                                       start, end, period, ['Minimum', 'Maximum', 'Average'])

    print(f"CPU Utilization for cluster 2, instance: {id_t2}")
    print(cpu_utilization['Datapoints'])

print(lb_arn)
ap_ELB = cw_wrapper.get_metric_statistics('AWS/ApplicationELB', 'ActiveConnectionCount', [{'Name': 'LoadBalancer', 'Value': str(lb_arn)}],
                                          start, end, period, ['Sum'])


print(ap_ELB['Datapoints'])
