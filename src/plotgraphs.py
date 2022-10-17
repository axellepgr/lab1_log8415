import matplotlib.pyplot as plt
import json

with open('metrics.json', 'r') as openfile:
    # Reading from json file
    metrics = json.load(openfile)
    openfile.close()


def plot_graphs_for_instances(type):

    print("Plotting graphs ...")

    # json object containing metrics
    m4_instances_CPU = metrics[type]

    # metric is a list containing json objects (on object for each instance)
    for metric in m4_instances_CPU:

        # instance is a json object with one key (instanceID) and its value is the datapoints
        for instance in m4_instances_CPU[metric]:
            x = []
            y = []

            # retreive the id of the instance
            id = ""
            for key in instance:
                id = key
            for point in instance[id]:
                point[0] = point[0].split()[1]
                x.append(point[0])
                y.append(point[1])
            plt.figure(id)
            if metric == "CPU_Utilization":
                plt.subplot(211)
            elif metric == "NetworkIn":
                plt.subplot(212)
            plt.plot(x, y, label=metric)
            plt.xlabel('timestamp')
            plt.ylabel('Percent')
            if metric == "NetworkIn":
                plt.ylabel('Bytes')
            plt.title(id)
    plt.savefig(f"${id}_1.png")
    plt.show()


def plot_graphs_for_load_balancer():
    # json object containing metrics
    lb_metrics = metrics["load_balancer"]

    print(lb_metrics)
    for metric in lb_metrics:
        x = []
        y = []
        print(metric)
        for point in lb_metrics[metric]:
            point[0] = point[0].split()[1]
            x.append(point[0])
            y.append(point[1])

        plt.figure("Load Balancer")
        if metric == "active_cc":
            plt.subplot(211)
            plt.ylabel('ACC Count')
        elif metric == "request_count":
            plt.subplot(212)
            plt.ylabel('Request Count')
        plt.plot(x, y, label=metric)
        plt.xlabel('timestamp')
        plt.title("Load Balancer")
    plt.savefig(f"${id}_2.png")
    plt.show()


plot_graphs_for_instances("m4_instances")
plot_graphs_for_instances("t2_instances")

# plot_graphs_for_load_balancer()
