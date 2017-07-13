import time
from pulp import *
import sys
sys.path.append("../")
# from load_data import *
from data_formatting import *

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def all_rootsinks_paths(graph):
    roots_list, sinks_list = rootsinks_filter(graph)
    paths = []
    for root in roots_list:
        for sink in sinks_list:
            paths.extend(find_all_paths(graph,root,sink))

    return paths

def pygraph_to_dictgraph(graph):
    dictgraph = {}
    for edge in graph.edges():
        if edge[0] not in dictgraph:
            dictgraph[edge[0]] = []
        dictgraph[edge[0]].append(edge[1])

    return dictgraph

def read_data(filename):
    f = open(filename,'r')
    data = f.read().split('\n')
    for i in range(len(data)):
        data[i] = data[i].split(' ')

    return data[:-1]    # Last line is empty

def data_to_dict(data):
    BBD_data = {}
    for line in data:
        if line[0] not in BBD_data:
            BBD_data[line[0]] = {}

        BBD_data[line[0]][float(line[1])] = {}
        BBD_data[line[0]][float(line[1])]['ibb'] = float(line[2])
        BBD_data[line[0]][float(line[1])]['latency'] = float(line[3])

    return BBD_data

def consumption_table(tasks,BBD_mapping,mapping,BBD_data):
    cons_table = {}
    for i in range(len(tasks)):
        cons_table[mapping[i]] = BBD_data[tasks[i]]
        cons_table[mapping[i]]['instr'] = tasks[i]

    for node in BBD_mapping:
        if node not in mapping:
            cons_table[node] = BBD_data['NOP']
            cons_table[node]['instr'] = 'NOP'

    return cons_table

def lower_upper_zero_bias_latency(all_paths,cleaned_tasks,BBD_data,BBD_voltages):
    min_Vbb = min(BBD_voltages)
    max_Vbb = max(BBD_voltages)
    LBs = []
    UBs = []
    MAX_LATs = [] # zero bias
    for path in all_paths:
        LB_lat = 0
        UB_lat = 0
        ML_lat = 0
        for task_ID in path:
            task = cleaned_tasks[task_ID]
            LB_lat += BBD_data[task][max_Vbb]["latency"]
            UB_lat += BBD_data[task][min_Vbb]["latency"]
            ML_lat += BBD_data[task][0.0]["latency"]    # zero bias

        LBs.append(LB_lat)
        UBs.append(UB_lat)
        MAX_LATs.append(ML_lat)

    # LB = max(LBs)
    # UB = max(UBs)
    MAX_LAT = max(MAX_LATs)

    return LBs, UBs, MAX_LAT

def latency_value(path,BBD_voltages,mapping,cleaned_tasks,BBD_assign,BBD_data):
    value = 0
    for task_ID in path:
        for j in BBD_voltages:
            node = mapping[task_ID]
            task = cleaned_tasks[task_ID]
            value += BBD_assign[node,j] * BBD_data[task][j]["latency"]

    return value

def subtiles(tile_size,mapping):
    tile_row, tile_col = tile_size[0], tile_size[1]
    min_x, max_x, min_y, max_y = mapping_extreme_coord(mapping)
    mapping_row, mapping_col = mapping_size(mapping)
    subtiles_group = []
    for i in range(min_x,min_x + mapping_col,tile_col):
        for j in range(min_y,min_y + mapping_row,tile_row):
            subtiles_group.append([])
            for k in range(tile_col):
                for l in range(tile_row):
                    subtiles_group[-1].append((i+k,j+l))

    return subtiles_group

def bbdlp(mapping, BBD_mapping, cons_table, BBD_data, BBD_voltages, all_paths, cleaned_tasks, LB, UB, MAX_LAT, tile_size, cgra_size):

    # Problem definition
    prob = LpProblem("BBD",LpMinimize)

    # Constants
    EPS = 1e-5
    # M = 1e16

    min_x, max_x, min_y, max_y = mapping_extreme_coord(mapping)
    mapping_row, mapping_col = mapping_size(mapping)
    tile_row, tile_col = tile_size[0], tile_size[1]
    BBD_comb = []
    for i in range(min_x,min_x + max(mapping_col,mapping_col + mapping_col % tile_col)):
        for j in range(min_y,min_y + max(mapping_row,mapping_row + mapping_row % tile_row)):
            for k in BBD_voltages:
                BBD_comb.append(((i,j),k))


    # Variables
    BBD_assign = LpVariable.dicts("BBD_assign",BBD_comb,cat="Binary")
    lat = LpVariable("Latency",lowBound = 0,cat="Continuous")
    d = LpVariable.dicts("d",range(len(all_paths)),cat="Binary")

    # Objective function
    prob += lpSum([[BBD_assign[i,j]*cons_table[i][j]['ibb'] for i in BBD_mapping] for j in BBD_voltages])

    # Constraints

    for i in mapping:
        prob += lpSum([BBD_assign[i,j] for j in BBD_voltages]) == 1

    # Max latency
    for i in range(len(all_paths)):
        # Linearization critical path (maximum function)
        prob += lat >= latency_value(all_paths[i],BBD_voltages,mapping,cleaned_tasks,BBD_assign,BBD_data)
        prob += lat <= latency_value(all_paths[i],BBD_voltages,mapping,cleaned_tasks,BBD_assign,BBD_data) + (max(UB)-LB[i])*(1-d[i])

    prob += lpSum(d) == 1
    prob += lat <= MAX_LAT

    # Tile body bias domain
    subtiles_group = subtiles(tile_size,mapping)
    max_tile_size = tile_row * tile_col

    for i in range(len(subtiles_group)):
        for j in BBD_voltages:
                prob += lpSum([BBD_assign[node,j] for node in subtiles_group[i]]) == max_tile_size*BBD_assign[subtiles_group[i][0],j]

    # prob.writeLP("bodybiaslp.lp")


    #print(prob)
    # try:
    #     prob.writeLP("generated_files/xp" + str(xp) + "/prominv.lp")
    # except:
    #     try:
    #         os.mkdir("generated_files")
    #     except:
    #         pass
    #     os.mkdir("generated_files/xp" + str(xp))
    #     prob.writeLP("generated_files/xp" + str(xp) + "/prominv.lp")

    prob.solve()
    # tic = time.time()
    # prob.solve(GUROBI())
    # toc = time.time() - tic
    # prob.solve(GLPK_CMD())
    # prob.writeLP("prominv.lp")
    # solvers.COIN_CMD(path="/opt/CoinMP/lib/")
    # prob.solve(COINMP_DLL())
    #
    # for v in prob.variables():
    #     if v.varValue != 0:
    #         print(v.name, "=", v.varValue,)
    # print("Zero bias latency:", MAX_LAT)
    # print("Status:", LpStatus[prob.status])
    # print("Objective function:", value(prob.objective))
    # print("Objective function (with NOP at -1.0V):", value(prob.objective)+(96-len(BBD_mapping))*BBD_data['NOP'][-1.0]['ibb'])
    # print("Time:", toc)

    return prob, BBD_assign
