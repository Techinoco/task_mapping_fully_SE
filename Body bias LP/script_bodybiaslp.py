from bodybiaslp import *
import csv
from collections import defaultdict
import sys
sys.path.append("../")
from load_data import *

from data_formatting import *

# def find_all_paths(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return [path]
#     if start not in graph:
#         return []
#     paths = []
#     for node in graph[start]:
#         if node not in path:
#             newpaths = find_all_paths(graph, node, end, path)
#             for newpath in newpaths:
#                 paths.append(newpath)
#     return paths
#
# def all_rootsinks_paths(graph):
#     roots_list, sinks_list = rootsinks_filter(graph)
#     paths = []
#     for root in roots_list:
#         for sink in sinks_list:
#             paths.extend(find_all_paths(graph,root,sink))
#
#     return paths
#
# def pygraph_to_dictgraph(graph):
#     dictgraph = {}
#     for edge in graph.edges():
#         if edge[0] not in dictgraph:
#             dictgraph[edge[0]] = []
#         dictgraph[edge[0]].append(edge[1])
#
#     return dictgraph
#
def read_data(BBD_FILENAME):
    f = open(BBD_FILENAME,'r')
    data = f.read().split('\n')
    for i in range(len(data)):
        data[i] = data[i].split(' ')

    return data[:-1]    # Last line is empty
#
# def data_to_dict(data):
#     BBD_data = {}
#     for line in data:
#         if line[0] not in BBD_data:
#             BBD_data[line[0]] = {}
#
#         BBD_data[line[0]][float(line[1])] = {}
#         BBD_data[line[0]][float(line[1])]['ibb'] = float(line[2])
#         BBD_data[line[0]][float(line[1])]['latency'] = float(line[3])
#
#     return BBD_data
#
# def consumption_table(tasks,BBD_mapping,mapping,BBD_data):
#     cons_table = {}
#     for i in range(len(tasks)):
#         cons_table[mapping[i]] = BBD_data[tasks[i]]
#         cons_table[mapping[i]]['instr'] = tasks[i]
#
#     for node in BBD_mapping:
#         if node not in mapping:
#             cons_table[node] = BBD_data['NOP']
#             cons_table[node]['instr'] = 'NOP'
#
#     return cons_table
#
# def lower_upper_zero_bias_latency(all_paths,cleaned_tasks,BBD_data,BBD_VDD):
#     min_Vbb = min(BBD_VDD)
#     max_Vbb = max(BBD_VDD)
#     LBs = []
#     UBs = []
#     MAX_LATs = [] # zero bias
#     for path in all_paths:
#         LB_lat = 0
#         UB_lat = 0
#         ML_lat = 0
#         for task_ID in path:
#             task = cleaned_tasks[task_ID]
#             LB_lat += BBD_data[task][max_Vbb]["latency"]
#             UB_lat += BBD_data[task][min_Vbb]["latency"]
#             ML_lat += BBD_data[task][0.0]["latency"]    # zero bias
#
#         LBs.append(LB_lat)
#         UBs.append(UB_lat)
#         MAX_LATs.append(ML_lat)
#
#     # LB = max(LBs)
#     # UB = max(UBs)
#     MAX_LAT = max(MAX_LATs)
#
#     return LBs, UBs, MAX_LAT


BBD_VDD = [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4]
BBD_FILENAME = "renshu2.txt"
BBD_TILESIZE = (1,2)
CGRA_SIZE = (8,12)  # for later use, not needed currently
af_bd_mapping = [(0,0),(2,0),(0,1),(2,1),(1,0),(1,1),(3,0),(3,1),(0,3),(2,3),(0,2),(1,2),(2,2),(3,2),(0,4),(1,3),(3,3),(3,4),(1,4),(2,4),(1,5),(2,5),(2,6),(3,6)]

data = read_data(BBD_FILENAME)
BBD_data = data_to_dict(data)
selected_mapping = int(input("Select mapping: "))
if selected_mapping != -1:
    mapping = hof[selected_mapping]
    cleaned_tasks = clean_tasks(tasks)
    crit_value, crit_path, total_value = critical_path(tasks_graph,platform_graph,SE_graph,mapping)
    bd_crit_value, bd_crit_path, bd_total_value = critical_path(tasks_graph,platform_graph,SE_graph,af_bd_mapping)
    all_paths = all_rootsinks_paths(tasks_graph)

    mapping_row, mapping_col = mapping_size(mapping)
    bd_mapping_row, bd_mapping_col = mapping_size(af_bd_mapping)
    tile_row, tile_col = BBD_TILESIZE[0], BBD_TILESIZE[1]
    BBD_mapping = []
    for i in range(max(mapping_col,mapping_col + mapping_col % tile_col)):
        for j in range(max(mapping_row,mapping_row + mapping_row % tile_row)):
            BBD_mapping.append((i,j))

    bd_BBD_mapping = []
    for i in range(max(bd_mapping_col,bd_mapping_col + bd_mapping_col % tile_col)):
        for j in range(max(bd_mapping_row,bd_mapping_row + bd_mapping_row % tile_row)):
            bd_BBD_mapping.append((i,j))

    cons_table = consumption_table(cleaned_tasks,BBD_mapping,af_bd_mapping,BBD_data)
    bd_cons_table = consumption_table(cleaned_tasks,bd_BBD_mapping,mapping,BBD_data)
    LB, UB, MAX_LAT = lower_upper_zero_bias_latency(all_paths,cleaned_tasks,BBD_data,BBD_VDD)
    prob, BBD_assign = bbdlp(mapping, BBD_mapping, cons_table, BBD_data, BBD_VDD, all_paths, cleaned_tasks, LB, UB, MAX_LAT, BBD_TILESIZE, CGRA_SIZE)
    bd_prob, bd_BBD_assign = bbdlp(af_bd_mapping, bd_BBD_mapping, bd_cons_table, BBD_data, BBD_VDD, all_paths, cleaned_tasks, LB, UB, MAX_LAT, BBD_TILESIZE, CGRA_SIZE)
