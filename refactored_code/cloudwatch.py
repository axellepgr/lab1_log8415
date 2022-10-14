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

# print("Activating detailed monitoring for all EC2 instances")
# for id in m4_IDs + t2_IDs:
#     os.system("aws ec2 monitor-instances --instance-ids " + id)

# print("Sending GET requests...")
# os.system("python send_requests.py")

# print("Waiting 1 minute before getting the CloudWatch metrics")
# time.sleep(60)


start = datetime.datetime.utcnow() - datetime.timedelta(seconds=300)
end = datetime.datetime.utcnow()
period = 60
cw_wrapper = CloudWatchWrapper(boto3.resource('cloudwatch'))

# Metrics for cluster 1 (m4.large)
for id_m4 in m4_IDs:

    ######### CPU METRICS #########
    cpu_utilization = cw_wrapper.get_metric_statistics('AWS/EC2', 'CPUUtilization', [{'Name': 'InstanceId', 'Value': id_m4}],
                                                       start, end, period, ['Minimum', 'Maximum', 'Average'])

    print(f"CPU Utilization for cluster 1, instance: {id_m4}")
    print(str(len(cpu_utilization['Datapoints'])) + " datapoint available")

    cpu_metrics = []

    for datapoint in cpu_utilization['Datapoints']:
        cpu_metrics.append([datapoint["Timestamp"], datapoint["Average"]])

    cpu_metrics.sort()

    for metric in cpu_metrics:
        print("date" + str(metric[0]) + " : " + str(metric[1]))

    ######### NETWORK IN METRICS #########
    network_in = cw_wrapper.get_metric_statistics('AWS/EC2', 'NetworkIn', [{'Name': 'InstanceId', 'Value': id_m4}],
                                                  start, end, period, ['Minimum', 'Maximum', 'Average'])

    print(f"Network In for cluster 1, instance: {id_m4}")
    print(str(len(network_in['Datapoints'])) + " datapoint available")

    network_in_metrics = []

    for datapoint in network_in['Datapoints']:
        network_in_metrics.append(
            [datapoint["Timestamp"], datapoint["Average"]])

    network_in_metrics.sort()

    for metric in network_in_metrics:
        print("date" + str(metric[0]) + " : " + str(metric[1]))

# Metrics for cluster 2 (t2.large)
for id_t2 in t2_IDs:
    cpu_utilization = cw_wrapper.get_metric_statistics('AWS/EC2', 'CPUUtilization', [{'Name': 'InstanceId', 'Value': id_t2}],
                                                       start, end, period, ['Minimum', 'Maximum', 'Average'])

    print(f"CPU Utilization for cluster 2, instance: {id_t2}")
    print(str(len(cpu_utilization['Datapoints'])) + " datapoint available")

    cpu_metrics = []

    for datapoint in cpu_utilization['Datapoints']:
        cpu_metrics.append([datapoint["Timestamp"], datapoint["Average"]])

    cpu_metrics.sort()

    for metric in cpu_metrics:
        print("date" + str(metric[0]) + " : " + str(metric[1]))

    network_in = cw_wrapper.get_metric_statistics('AWS/EC2', 'NetworkIn', [{'Name': 'InstanceId', 'Value': id_t2}],
                                                  start, end, period, ['Minimum', 'Maximum', 'Average'])

    print(f"Network In for cluster 1, instance: {id_t2}")
    print(str(len(network_in['Datapoints'])) + " datapoint available")

    network_in_metrics = []

    for datapoint in network_in['Datapoints']:
        network_in_metrics.append(
            [datapoint["Timestamp"], datapoint["Average"]])

    network_in_metrics.sort()

    for metric in network_in_metrics:
        print("date" + str(metric[0]) + " : " + str(metric[1]))

print("\nLoad Balancer Statistics...\n")

active_cc = cw_wrapper.get_metric_statistics('AWS/ApplicationELB', 'ActiveConnectionCount', [{'Name': 'LoadBalancer', 'Value': "app/Load-balancer-1/71292dcce222ad8c"}],
                                             start, end, period, ['Sum'])

print(str(len(active_cc['Datapoints'])) +
      " datapoint available for the Active Connection Count metric")

active_cc_metrics = []

for datapoint in active_cc['Datapoints']:
    active_cc_metrics.append(
        [datapoint["Timestamp"], datapoint["Sum"]])

active_cc_metrics.sort()

for metric in active_cc_metrics:
    print("date" + str(metric[0]) + " : " + str(metric[1]))

RequestCount = cw_wrapper.get_metric_statistics('AWS/ApplicationELB', 'RequestCount', [{'Name': 'LoadBalancer', 'Value': "app/Load-balancer-1/71292dcce222ad8c"}],
                                                start, end, period, ['Sum'])

print("\n\n")
print(str(len(RequestCount['Datapoints'])) +
      " datapoint available for the RequestCount metric")

RequestCount_metrics = []

for datapoint in RequestCount['Datapoints']:
    RequestCount_metrics.append(
        [datapoint["Timestamp"], datapoint["Sum"]])

RequestCount_metrics.sort()

for metric in RequestCount_metrics:
    print("date" + str(metric[0]) + " : " + str(metric[1]))
