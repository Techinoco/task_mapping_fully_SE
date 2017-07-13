from sys import platform as _platform
# Workaround for Mac
if _platform == "darwin":
    import matplotlib
    matplotlib.use("macosx")

from matplotlib import pyplot as plt
from moga_taskmapping_bbdlp import *
from data_formatting import *
import numpy

def plot_mapping(mapping_coord,tasks_graph):
    mapping = mapping_coord[:]
    shift_mapping(mapping,(0,0))
    tasksonly_graph = copy.deepcopy(tasks_graph)
    tasksonly_graph.del_node(-1)
    roots_list, sinks_list = rootsinks_filter(tasksonly_graph)
    plt.hold(True)
    for i in range(len(mapping)):
        if i in roots_list:
            plt.plot(mapping[i][0],mapping[i][1],'go')
        elif i in sinks_list:
            plt.plot(mapping[i][0],mapping[i][1],'ro')
        else:
            plt.plot(mapping[i][0],mapping[i][1],'bo')

    head_w = 0.15
    head_l = 0.2
    for (node1,node2) in tasksonly_graph.edges():
        # plt.plot((mapping[node1][0],mapping[node2][0]),(mapping[node1][1],mapping[node2][1]),'k-')
        offset_x = 0
        offset_y = 0
        if mapping[node2][0]-mapping[node1][0] > 0:
            offset_x = -head_l
        elif mapping[node2][0]-mapping[node1][0] < 0:
            offset_x = head_l

        if mapping[node2][1]-mapping[node1][1] > 0:
            offset_y = -head_l
        elif mapping[node2][1]-mapping[node1][1] < 0:
            offset_y = head_l

        plt.arrow(mapping[node1][0],mapping[node1][1],mapping[node2][0]-mapping[node1][0]+offset_x,mapping[node2][1]-mapping[node1][1]+offset_y,fc="k", ec="k",head_width=head_w, head_length=head_l)

    ticks = numpy.arange(0,12,1)
    plt.xticks(ticks)
    plt.yticks(ticks)
    h,w = mapping_size(mapping_coord)
    plt.axis([-0.5, w-0.5, -0.5, 7.5])
    plt.axis('scaled')
    plt.grid(True)
    plt.show()
