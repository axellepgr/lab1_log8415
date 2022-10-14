import matplotlib.pyplot as plt
import json

with open('metrics.json', 'r') as openfile:
    # Reading from json file
    metrics = json.load(openfile)
    openfile.close()


def plot_graphs_for_instances(type, metric):
    m4_instances_CPU = metrics["m4_instances"]["CPU_Utilization"]
    print(m4_instances_CPU)
    for instance in m4_instances_CPU:
        x = []
        y = []
        id = ""
        for key in instance:
            id = key
        for point in instance[id]:
            x.append(point[0])
            y.append(point[1])
        plt.figure()
        plt.plot(x, y)
        plt.xlabel('timestamp')
        plt.ylabel('Percent')
        if metric == "NetworkIn":
            plt.ylabel('Bytes')
        plt.title(id)
    plt.show()


plot_graphs_for_instances("m4_instances", 'CPUUtilization')
