import matplotlib.pyplot as plt
import json

with open('metrics.json', 'r') as openfile:
    # Reading from json file
    metrics = json.load(openfile)
    openfile.close()


def plot_graphs_for_instances(type):

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
    plt.show()


plot_graphs_for_instances("m4_instances")
