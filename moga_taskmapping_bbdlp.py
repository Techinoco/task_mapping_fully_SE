import random
import sys
import csv
import numpy
import itertools
import copy
import pickle
import time
import re
import datetime

from pygraph.classes.digraph import digraph
from pygraph.algorithms.critical import critical_path as pygraphcp
from pygraph.algorithms.sorting import topological_sorting
from pygraph.algorithms.heuristics.chow import chow
from pygraph.algorithms.heuristics.euclidean import euclidean
from pygraph.algorithms.minmax import *

from collections import defaultdict

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from cma import *
from tasks_graph_examples import *
# from data_formatting import *

# sys.path.append("Body bias LP")
from bodybiaslp import *

def clean_tasks(tasks):
    return list(map(lambda x: x.split('_')[0], tasks))[:-1]

# CMA size
PE_row = 8
PE_col = 12

# Simulation settings
APPLICATION = 'af'
if APPLICATION == 'af':
    tasks, tasks_graph, tasks_op = af_graph_reg()
elif APPLICATION == 'sf':
    tasks, tasks_graph, tasks_op = sf_graph_reg()
elif APPLICATION == 'gray':
    tasks, tasks_graph, tasks_op = gray_graph_reg()
NGEN = 200
MU = 50
INIT_POP_SIZE = MU * 3
LAMBDA = 100    # MU should be lower than LAMBDA
CXPB = 0.7
MUTPB = 0.3
LSPB = 0.5  # Local search probability (within mutation operation)
SHPB = 0.5
SHPB0 = 0.5
TIME = int(datetime.datetime.now().strftime('%y%m%d%H%M'))
FORCED_SEED = 0
if FORCED_SEED == 0:
    SEED = TIME
else:
    SEED = FORCED_SEED
DEPTH = 1
ROUTING_METHOD = "astar-routing"
GENERATOR_METHOD = "shortest-greedy"
CRITERIA = "(crit_value,total_value,width_value,bbd_value)"

BBD_VDD = [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4]
BBD_FILENAME = "renshu2.txt"
BBD_TILESIZE = (2,1)    # (row,col)
CGRA_SIZE = (8,12)  # for later use, not needed currently
data = read_data(BBD_FILENAME)
BBD_data = data_to_dict(data)
cleaned_tasks = clean_tasks(tasks)
tasksonly_graph = copy.deepcopy(tasks_graph)
tasksonly_graph.del_node(-1)
all_paths = all_rootsinks_paths(tasksonly_graph)

SAVE_FILE = "results/" + str(TIME) + "_SEED" + str(SEED) + "_" + APPLICATION + "_" + CRITERIA + "_" + ROUTING_METHOD + "_" + GENERATOR_METHOD + "_CXPB" + str(CXPB) + "_MUTPB" + str(MUTPB) + "_LSPB" + str(LSPB) + "_SHPB" + str(SHPB) + "_SHPB0" + str(SHPB0) +"_DEPTH" + str(DEPTH) + ".sav"
print(SAVE_FILE)

def generate_random_individuals(tasks_graph,platform_graph,method="random"):
    """
    Generates a random individual (random placement)
    from the tasks_graph to the platform_graph
    3 possible methods: random (default), greedy or GRASP
    tasks_graph: pygraph digraph
    platform_graph: whatever?
    """
    # TODO: redo the doc
    if method == "random":
        pool = random_generator(tasks_graph,platform_graph)

    elif method == "shortest_greedy":
        pool = shortest_greedy_generator(tasks_graph,tasks_op,platform_graph,SE_graph,ALU_graph)

    elif method == "grasp":
        pool = grasp_generator(tasks_graph,platform_graph)    # TODO: do it...
    else:
        pass    # TODO: proper else raise error routine
    
    return pool

def random_generator(tasks_graph,PE_row,PE_col):
    """
    Totally random generator
    """
    task_nb = len(tasks_graph.nodes()) - 1
    # platform_col_nb = len(platform_graph[0])    # only size required??
    # platform_row_nb = len(platform_graph)
    coord_x_list = list(range(PE_col))
    coord_y_list = list(range(PE_row))
    possible_coordinates = list(itertools.product(coord_x_list,coord_y_list))
    # pool = []
    # for i in range(n):
    possible_coordinates_copy = copy.deepcopy(possible_coordinates)
    mapping = []
    for i in range(task_nb):
        rand_coord = random.randint(0,len(possible_coordinates_copy)-1)
        coord = possible_coordinates_copy.pop(rand_coord)
        mapping.append(coord)

        # pool.append(mapping)

    # return pool
    return mapping

def shortest_greedy_generator(tasks_graph,tasks_op,platform_graph,SE_graph,ALU_graph):
    """
    Generator using a randomized greedy algorithm
    TODO: clean the code!!!
    """
    tasksonly_graph = copy.deepcopy(tasks_graph)
    tasksonly_graph.del_node(-1)
    task_nb = len(tasksonly_graph.nodes())
    topological_order = topological_sorting(tasksonly_graph)
    roots_list = roots_filter(tasksonly_graph)

    routed_platform_graph = copy.deepcopy(platform_graph)
    routed_SE_graph = copy.deepcopy(SE_graph)
    routed_ALU_graph = copy.deepcopy(ALU_graph)

    root_subgraphs = rootgraphs(topological_order,roots_list)
    random.shuffle(root_subgraphs)

    random_topological_order = [item for sublist in root_subgraphs for item in sublist] # flattening the list

    edges_list_sorted = []
    for node in random_topological_order:
        for edge in tasksonly_graph.edges():
            if edge[0] == node:
                edges_list_sorted.append(edge)

    mapping = [0 for i in range(task_nb)]
    placed = [False for i in range(len(random_topological_order))]
    used_nodes = []
    first_root_placed = []
    for (source_node, target_node) in edges_list_sorted:
        if placed[source_node] == False and placed[target_node] == False:
            if source_node in roots_list and first_root_placed == []:
                # DEPTH = 2
                local_depth = DEPTH + 1
                available_start_nodes = []
                while available_start_nodes == []:
                    for node in routed_platform_graph.nodes():
                        if 'ALU' in node and node not in used_nodes and int(node.split('_')[1]) < local_depth:
                            available_start_nodes.append(node)
                    local_depth += 1

                chosen_source_node = available_start_nodes[random.randint(0,len(available_start_nodes)-1)]
                used_nodes.append(chosen_source_node)
                mapping[source_node] = (int(re.sub('\D', '', chosen_source_node.split('_')[0])),int(chosen_source_node.split('_')[1]))
                placed[source_node] = True
                first_root_placed.append(source_node)
            # else:
                # source_node_location = 'ALU' + mapping[source_node][0] + '_' + mapping[source_node][1]
                closest_nodes = shortest_path(routed_platform_graph,chosen_source_node)[1]
                shortest_path_list = list(filter(lambda x: 'ALU' in x[0], sorted(closest_nodes.items(), key=lambda x: (x[1],x[0]))))[1:]
                # DEPTH = 2
                local_depth = DEPTH
                chosable_nodes = []
                while chosable_nodes == []:
                    for node, dist in shortest_path_list:
                        if node not in used_nodes and dist <= local_depth:
                            chosable_nodes.append(node)
                    local_depth += 1
                chosen_target_node = chosable_nodes[random.randint(0,len(chosable_nodes)-1)]
                used_nodes.append(chosen_target_node)
                mapping[target_node] = (int(re.sub('\D', '', chosen_target_node.split('_')[0])),int(chosen_target_node.split('_')[1]))    # coordinates
                placed[target_node] = True
                # routed_platform_graph.del_node(chosen_source_node)
                # routed_platform_graph.del_node(chosen_target_node)

            elif source_node in roots_list and first_root_placed != []:
                # DEPTH = 2
                local_depth = DEPTH #+ 1
                first_root_node = 'ALU' + str(mapping[first_root_placed[0]][0]) + '_' + str(mapping[first_root_placed[0]][1])
                available_start_nodes = []
                while available_start_nodes == []:
                    # for node in routed_platform_graph.nodes():
                    #     if 'ALU' in node and node not in used_nodes and int(node.split('_')[1]) < local_depth:
                    #         available_start_nodes.append(node)
                    for i in range(-local_depth,local_depth+1):
                        for j in range(-local_depth,local_depth+1):
                            x = mapping[first_root_placed[0]][0] + i
                            y = mapping[first_root_placed[0]][1] + j
                            node = 'ALU' + str(x) + '_' + str(y)
                            
                            if 0 <= x <= PE_col - 1 and 0 <= y <= PE_row -1 and node not in used_nodes:
                                available_start_nodes.append(node)
                            
                    local_depth += 1

                chosen_source_node = available_start_nodes[random.randint(0,len(available_start_nodes)-1)]
                used_nodes.append(chosen_source_node)
                mapping[source_node] = (int(re.sub('\D', '', chosen_source_node.split('_')[0])),int(chosen_source_node.split('_')[1]))
                placed[source_node] = True
            # else:
                # source_node_location = 'ALU' + mapping[source_node][0] + '_' + mapping[source_node][1]
                closest_nodes = shortest_path(routed_platform_graph,chosen_source_node)[1]
                shortest_path_list = list(filter(lambda x: 'ALU' in x[0], sorted(closest_nodes.items(), key=lambda x: (x[1],x[0]))))[1:]
                # DEPTH = 2
                local_depth = DEPTH
                chosable_nodes = []
                while chosable_nodes == []:
                    for node, dist in shortest_path_list:
                        if node not in used_nodes and dist <= local_depth:
                            chosable_nodes.append(node)
                    local_depth += 1
                chosen_target_node = chosable_nodes[random.randint(0,len(chosable_nodes)-1)]
                used_nodes.append(chosen_target_node)
                mapping[target_node] = (int(re.sub('\D', '', chosen_target_node.split('_')[0])),int(chosen_target_node.split('_')[1]))    # coordinates
                placed[target_node] = True
                # routed_platform_graph.del_node(chosen_source_node)
                # routed_platform_graph.del_node(chosen_target_node)

        elif placed[source_node] == True and placed[target_node] == False:
            source_node_location = 'ALU' + str(mapping[source_node][0]) + '_' + str(mapping[source_node][1])
            closest_nodes = shortest_path(routed_platform_graph,source_node_location)[1]
            shortest_path_list = list(filter(lambda x: 'ALU' in x[0], sorted(closest_nodes.items(), key=lambda x: (x[1],x[0]))))[1:]
            # DEPTH = 2
            local_depth = DEPTH
            chosable_nodes = []
            while chosable_nodes == []:
                for node, dist in shortest_path_list:
                    if node not in used_nodes and dist <= local_depth:
                        chosable_nodes.append(node)
                local_depth += 1
            chosen_target_node = chosable_nodes[random.randint(0,len(chosable_nodes)-1)]
            used_nodes.append(chosen_target_node)
            mapping[target_node] = (int(re.sub('\D', '', chosen_target_node.split('_')[0])),int(chosen_target_node.split('_')[1]))    # coordinates
            # routed_platform_graph.del_node()
            placed[target_node] = True

        elif placed[source_node] == False and placed[target_node] == True:
            (target_x, target_y) = (mapping[target_node][0], mapping[target_node][1])
            local_depth = DEPTH
            chosable_nodes = []
            while chosable_nodes == []:
                chosable_nodes_coord = []
                delta = list(range(-local_depth,local_depth+1))
                for i in delta:
                    for j in delta:
                        (new_x, new_y) = (target_x+i, target_y+j)
                        if 0 <= new_x <= PE_col-1 and 0 <= new_y <= PE_row-1:
                            chosable_nodes_coord.append((new_x,new_y))

                chosable_nodes_coord.remove((target_x,target_y))

                for x,y in chosable_nodes_coord:
                    node_location = 'ALU' + str(x) + '_' + str(y)
                    closest_nodes = shortest_path(routed_platform_graph,node_location)[1]
                    filtered_closest_nodes = list(filter(lambda x: 'ALU' in x[0] and x[1] <= local_depth, sorted(closest_nodes.items(), key=lambda x: (x[1],x[0]))))[1:]
                    for node, _ in filtered_closest_nodes:
                        if node not in used_nodes and node not in chosable_nodes:
                            chosable_nodes.append(node)

                local_depth += 1

            chosen_source_node = chosable_nodes[random.randint(0,len(chosable_nodes)-1)]
            used_nodes.append(chosen_source_node)
            mapping[source_node] = (int(re.sub('\D', '', chosen_target_node.split('_')[0])),int(chosen_target_node.split('_')[1]))
            placed[source_node] = True

    # shift_mapping(mapping)

    # if len(list(set(mapping))) != len(tasks):
        # print('WTF')

    # Constants mapping


    return mapping

def rootgraphs(topological_order,roots_list):
    root_subgraphs = []
    for node in topological_order:
        if node in roots_list:
            root_subgraphs.append([])
        root_subgraphs[-1].append(node)

    return root_subgraphs

def objectives_eval(tasks_graph,platform_graph,SE_graph,individual):
    """
    Compute the objectives evaluation
    TODO: add more objectives (width of the task mapping, pipeline performance, power consumption, latency, ...)
    """
    if "crit_value" in CRITERIA or "total_value" in CRITERIA:
        crit_value, crit_path, total_value = critical_path(tasks_graph,platform_graph,SE_graph,individual)
    if "width_value" in CRITERIA:
        width_value = mapping_width(individual)
    if "bbd_value" in CRITERIA:
        bbd_value = bbd_eval(individual,tasks,tasks_graph)
    # return crit_value, width_value
    return eval(CRITERIA)

def mapping_extreme_coord(mapping):
    min_x = mapping[0][0]
    max_x = mapping[0][0]
    min_y = mapping[0][1]
    max_y = mapping[0][1]
    for i in range(1,len(mapping)):
        if mapping[i][0] < min_x:
            min_x = mapping[i][0]
        elif mapping[i][0] > max_x:
            max_x = mapping[i][0]
        if mapping[i][1] < min_y:
            min_y = mapping[i][1]
        elif mapping[i][1] > max_y:
            max_y = mapping[i][1]

    return min_x, max_x, min_y, max_y    

def mapping_size(mapping):
    """
    Returns the size of the mapping (number of rows and columns used)
    """
    min_x, max_x, min_y, max_y = mapping_extreme_coord(mapping)

    return (max_y - min_y) + 1, (max_x - min_x) + 1

def bbd_eval(individual,tasks,tasks_graph):
    # data = read_data(BBD_FILENAME)
    # BBD_data = data_to_dict(data)
    # cleaned_tasks = clean_tasks(tasks)
    # all_paths = all_rootsinks_paths(tasks_graph)
    min_x, max_x, min_y, max_y = mapping_extreme_coord(individual)
    mapping_row, mapping_col = mapping_size(individual)
    tile_row, tile_col = BBD_TILESIZE[0], BBD_TILESIZE[1]
    BBD_mapping = []
    for i in range(min_x,min_x + max(mapping_col,mapping_col + mapping_col % tile_col)):
        for j in range(min_y,min_y + max(mapping_row,mapping_row + mapping_row % tile_row)):
            BBD_mapping.append((i,j))

    cons_table = consumption_table(cleaned_tasks,BBD_mapping,individual,BBD_data)
    LB, UB, MAX_LAT = lower_upper_zero_bias_latency(all_paths,cleaned_tasks,BBD_data,BBD_VDD)
    prob, BBD_assign = bbdlp(individual, BBD_mapping, cons_table, BBD_data, BBD_VDD, all_paths, cleaned_tasks, LB, UB, MAX_LAT, BBD_TILESIZE, CGRA_SIZE)
    # bbd_value = value(prob.objective)
    bbd_value = value(prob.objective)+(96-len(BBD_mapping))*BBD_data['NOP'][-1.0]['ibb']
    return bbd_value

def critical_path(tasks_graph,platform_graph,SE_graph,individual):
    """
    Compute the critical path of the mapping (individual) in L1 distance
    on basis on the tasks_graph information (routing)
    Uses the pygraph library (http://faculty.lagcc.cuny.edu/tnagano/research/DOT/docs/pygraphDocs/pygraph-module.html)
    """
    if ROUTING_METHOD == "astar-routing":
        weighted_tasks_graph, edges_list_sorted, paths_list, constants_path, constants_path_value, constants_map, reg_path, reg_path_value, reg_map, output_path = astar_tasks_routing(tasks_graph,tasks_op,platform_graph,SE_graph,individual)
    else:
        weighted_tasks_graph = simple_routing(tasks_graph,individual)

    crit_path = pygraphcp(weighted_tasks_graph)
    crit_value = path_evaluation(weighted_tasks_graph,crit_path)
    total_value = total_value_evaluation(weighted_tasks_graph)
    # rootsink_value = rootsink_value_evaluation(weighted_tasks_graph,individual)
    # crit_value += rootsink_value
    # total_value += rootsink_value
    roots_value = roots_value_evaluation(weighted_tasks_graph,individual)
    crit_value += roots_value
    # total_value += roots_value
    total_value += roots_value + constants_path_value + reg_path_value
    return crit_value, crit_path, total_value

def simple_routing(tasks_graph,individual):
    """
    Simple routing, no consideration for communication infrastructure
    """
    weighted_tasks_graph = copy.deepcopy(tasks_graph)
    for (node1,node2) in weighted_tasks_graph.edges():
        weight = abs(individual[node1][0]-individual[node2][0]) + abs(individual[node1][1]-individual[node2][1])
        weighted_tasks_graph.set_edge_weight((node1,node2),weight)

    return weighted_tasks_graph

def astar_tasks_routing(tasks_graph,tasks_op,platform_graph,SE_graph,individual):
    """
    Routing using a shortest path algorithm (A*) and some BFS
    """
    # roots_list, sinks_list = rootsinks_filter(tasks_graph)
    tasksonly_graph = copy.deepcopy(tasks_graph)
    tasksonly_graph.del_node(-1)
    roots_list = roots_filter(tasksonly_graph)
    topological_order = topological_sorting(tasks_graph)
    edges_list_sorted = []
    for node in topological_order:
        for edge in tasks_graph.edges():
            if edge[0] == node:
                edges_list_sorted.append(edge)

    weighted_tasks_graph = copy.deepcopy(tasksonly_graph)
    routed_platform_graph = copy.deepcopy(platform_graph)
    routed_SE_graph = copy.deepcopy(SE_graph)
    # SE_search_graph = euclidean()  # chow not working!?
    # platform_search_graph = euclidean()
    # # Optimizing all the original graphs
    # SE_search_graph.optimize(routed_SE_graph)
    # platform_search_graph.optimize(routed_platform_graph)
    # search_graph.optimize(routed_platform_graph)
    routable = True
    paths_list = []
    for edge in edges_list_sorted:
        if edge[0] == -1:
            continue
            # source_node = 'REG_IN_' + str(individual[edge[1]][0])
            # target_node = 'ALU' + str(individual[edge[1]][0]) + '_' + str(individual[edge[1]][1])

        else:
            source_node = 'ALU' + str(individual[edge[0]][0]) + '_' + str(individual[edge[0]][1])
            target_node = 'ALU' + str(individual[edge[1]][0]) + '_' + str(individual[edge[1]][1])

        # TODO: add stupid constraint for SE not routing west if coming from same ALU...

        if (source_node,target_node) not in routed_platform_graph.edges():
            routable_SE_graph = clean_unroutable_nodes(routed_SE_graph,source_node,target_node)
            # search_graph.optimize(routable_SE_graph)
            try:
                route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
                paths_list.append(route_path)
            except:
                routable = False
                weight = 10000  # high weight penalty to not consider this individual
                # TODO: some repair mechanism?
                weighted_tasks_graph.set_edge_weight(edge,weight)
                constants_path = []
                constants_path_value = 0
                constants_map = []
                reg_path = []
                reg_path_value = 0
                reg_map = []
                output_path = []
                return weighted_tasks_graph, edges_list_sorted, paths_list, constants_path, constants_path_value, constants_map, reg_path, reg_path_value, reg_map, output_path

        else:
            # search_graph.optimize(routed_platform_graph)
            try:
                route_path = heuristic_search(routed_platform_graph,source_node,target_node,platform_search_graph)
                # routed_platform_graph.del_edge((source_node,target_node))
                paths_list.append(route_path)
            except:
                routable = False
                weight = 10000  # high weight penalty to not consider this individual
                # TODO: some repair mechanism?
                weighted_tasks_graph.set_edge_weight(edge,weight)
                constants_path = []
                constants_path_value = 0
                constants_map = []
                reg_path = []
                reg_path_value = 0
                reg_map = []
                output_path = []
                return weighted_tasks_graph, edges_list_sorted, paths_list, constants_path, constants_path_value, constants_map, reg_path, reg_path_value, reg_map, output_path

        if routable:
            for i in range(len(route_path)-1):
                # print(route_path)
                # input()
                if ('ALU' in route_path[i] and 'ALU' in route_path[i+1]) or ('REG_IN' in route_path[i] and 'ALU' in route_path[i+1]):
                    routed_platform_graph.del_edge((route_path[i],route_path[i+1]))
                else:
                    # Should also remove the SE-SE edge (maybe)
                    if ('SE' in route_path[i] and 'ALU' in route_path[i+1]):
                        related_SE = route_path[i+1].replace('ALU','SE')
                        if (route_path[i],related_SE) in routed_platform_graph.edges():
                            routed_platform_graph.del_edge((route_path[i],related_SE))
                        if (route_path[i],related_SE) in routed_SE_graph.edges():
                            routed_SE_graph.del_edge((route_path[i],related_SE))

                    routed_platform_graph.del_edge((route_path[i],route_path[i+1]))
                    routed_SE_graph.del_edge((route_path[i],route_path[i+1]))

            weight = path_evaluation(platform_graph,route_path)
            weighted_tasks_graph.set_edge_weight(edge,weight)
            # TODO: constants routing here

        else:
            pass
            # weight = 10000  # high weight penalty to not consider this individual
            # # TODO: some repair mechanism?
            # weighted_tasks_graph.set_edge_weight(edge,weight)

    if routable:
        # constants_path = []
        # constants_path_value = 0
        # constants_map = []
        # reg_path = []
        # reg_path_value = 0
        # reg_map = []
        # output_path = []
        constants_path, constants_path_value, constants_map = constants_routing(tasks,tasks_op,tasks_graph,routed_platform_graph,routed_SE_graph,individual)
        reg_path, reg_path_value, reg_map = reg_in_mapping(tasks,tasks_op,tasks_graph,routed_platform_graph,routed_SE_graph,individual)
        output_path = output_routing(individual)

    return weighted_tasks_graph, edges_list_sorted, paths_list, constants_path, constants_path_value, constants_map, reg_path, reg_path_value, reg_map, output_path

def output_routing(individual):
    roots_list, sinks_list = rootsinks_filter(tasksonly_graph)
    route_path = []
    for sink in sinks_list:
        path = []
        x, y = individual[sink]
        ALU_node = 'ALU' + str(x) + '_' + str(y)
        path.append(ALU_node)
        for row in range(y,-1,-1):
            SE_node = 'SE' + str(x) + '_' + str(row)
            path.append(SE_node)

        route_path.append(path)

    return route_path

def constants_routing(tasks,tasks_op,tasks_graph,routed_platform_graph,routed_SE_graph,individual):
    constants_map, tasks_with_constant = constants_mapping(tasks,tasks_op,tasks_graph,routed_platform_graph,routed_SE_graph,individual)
    # print()
    # for line in constants_map:
    #     print(line)
    # if need_desperate_mapping(constants_map):
    #     print(need_desperate_mapping(constants_map))
    #     input()
    # else:
    #     print(need_desperate_mapping(constants_map))

    routable = True
    paths_list = []
    weight = 0
    for task in tasks_with_constant:
        row = task[2][1]
        constant = task[1]
        target_node = 'ALU' + str(task[2][0]) + '_' + str(task[2][1])
        if constants_map[row][constant] == 'A':
            source_node = 'C_'  + str(row) + 'A'
            route_path = [source_node, target_node]
        elif constants_map[row][constant] == 'B':
            source_node = 'C_'  + str(row) + 'B'
            route_path = [source_node, target_node]
        elif 'P' in constants_map[row][constant]:
            source_node = 'C_' + constants_map[row][constant].split('_')[-1] + 'A'
            try:
                routable_SE_graph = clean_unroutable_nodes_constants(routed_SE_graph,row)
                route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
            except:
                routable = False
                weight = 10000
                return paths_list, weight, constants_map
        if routable:
            paths_list.append(route_path)
            for i in range(len(route_path)-1):
                weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']

            # Removing used SE paths for constant
            for i in range(len(route_path) - 1):
                if 'SE' in route_path[i]:
                    routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
                    routed_platform_graph.del_edge((route_path[i], route_path[i+1]))

    return paths_list, weight, constants_map

def clean_unroutable_nodes_constants(routed_SE_graph,row):
    routable_SE_graph = copy.deepcopy(routed_SE_graph)
    for edge in routable_SE_graph.edges():
        if 'SE' in edge[0] and edge[0].split('_')[-1] == str(row) and 'SE' in edge[1] and edge[1].split('_')[-1] == str(row):
            routable_SE_graph.del_edge(edge)

    return routable_SE_graph


def constants_mapping(tasks,tasks_op,tasks_graph,routed_platform_graph,routed_SE_graph,individual):
    # c,cc = constants_mapping(tasks,tasks_op,tasks_graph,platform_graph,SE_graph,individual)
    constant_registers = sorted(list(filter(lambda x: 'C' in x, routed_platform_graph)))
    constant_registers = [(i,None) for i in constant_registers]
    tasks_with_constant = []
    for i in range(len(tasks_op)):
        for in_port in tasks_op[i]['IN']:
            if type(in_port) == int or type(in_port) == float:
                tasks_with_constant.append([i,in_port,individual[i]])

    constants_in_row = constants_per_row(tasks_with_constant)

    # mapped_values = []
    # flags = [[] for i in range(len(constants_in_row))]
    # Currently, only some simple constant mapping policy... (bottom up since CMA is pushing up)

    bottomup_mapping(constants_in_row)
    # clean_constants_mapping(constants_in_row)
    if need_desperate_mapping(constants_in_row):
        desperate_bottomup_mapping(constants_in_row)
        if need_desperate_mapping(constants_in_row):
            # really desperate
            desperate_topdown_mapping(constants_in_row)
            if need_desperate_mapping:
                desperate_bottomup_fill_mapping(constants_in_row)
                if need_desperate_mapping:
                    desperate_topdown_fill_mapping(constants_in_row)
    return constants_in_row, tasks_with_constant

def bottomup_mapping(constants_in_row):
    for i in range(len(constants_in_row)):
        if i == 0:
            if len(constants_in_row[i]) == 1:
                value = list(constants_in_row[i].keys())[0]
                if constants_in_row[i][value] == 'X':
                    map1constant(i,value,constants_in_row)

            elif len(constants_in_row[i]) == 2:
                value1, value2 = list(constants_in_row[i].keys())
                if constants_in_row[i][value1] == 'X' and constants_in_row[i][value2] == 'X':
                    map2constants(i,value1,value2,constants_in_row)

            elif len(constants_in_row[i]) > 2:
                to_map = []
                for val in constants_in_row[i]:
                    if constants_in_row[i][val] == 'X':
                        to_map.append(val)

                if len(to_map) == 1:
                    value = to_map[0]
                    if constants_in_row[i][value] == 'X':
                        map1constant(i,value,constants_in_row)

                elif len(to_map) == 2:
                    value1, value2 = to_map
                    if constants_in_row[i][value1] == 'X' and constants_in_row[i][value2] == 'X':
                        map2constants(i, value1, value2, constants_in_row)

                elif len(to_map) > 2:
                    # values = to_map
                    pass

        elif i == len(constants_in_row) - 1:
            # Last row, only look backward
            if len(constants_in_row[i]) == 1:
                value = list(constants_in_row[i].keys())[0]
                constants_in_row[i][value] = "A"

            elif len(constants_in_row[i]) == 2:
                value1, value2 = list(constants_in_row[i].keys())
                constants_in_row[i][value1] = "A"
                constants_in_row[i][value2] = "B"

            elif len(constants_in_row[i]) > 2:
                # Check if there are empty register in previous rows
                to_map = []
                for val in constants_in_row[i]:
                    if constants_in_row[i][val] == 'X':
                        to_map.append(val)

                if len(to_map) == 1:
                    value = to_map[0]
                    constants_in_row[i][value] = 'B'
                    # if constants_in_row[i][value] == 'X':
                    #     map1constant(i,value,constants_in_row)

                elif len(to_map) == 2:
                    value1, value2 = to_map
                    constants_in_row[i][value1] = 'A'
                    constants_in_row[i][value2] = 'B'
                    # if constants_in_row[i][value1] == 'X' and constants_in_row[i][value2] == 'X':
                    #     map2constants(i, value1, value2, constants_in_row)

                elif len(to_map) > 2:
                    # values = to_map
                    pass

        else:
            # Look forward and backward
            if len(constants_in_row[i]) == 1:
                value = list(constants_in_row[i].keys())[0]
                if constants_in_row[i][value] == 'X' or 'P' in constants_in_row[i][value]:
                    map1constant(i,value,constants_in_row)

            elif len(constants_in_row[i]) == 2:
                value1, value2 = list(constants_in_row[i].keys())
                if (constants_in_row[i][value1] == 'X' or 'P' in constants_in_row[i][value1]) and (constants_in_row[i][value2] == 'X' or 'P' in constants_in_row[i][value2]):
                    map2constants(i,value1,value2,constants_in_row)

            elif len(constants_in_row[i]) > 2:
                to_map = []
                for val in constants_in_row[i]:
                    if constants_in_row[i][val] == "X":
                        to_map.append(val)

                if len(to_map) == 1:
                    value = to_map[0]
                    # if constants_in_row[i][value] == 'X':
                    if constants_in_row[i][value] == 'X' or 'P' in constants_in_row[i][value]:
                        map1constant(i,value,constants_in_row)

                elif len(to_map) == 2:
                    value1, value2 = to_map
                    # if constants_in_row[i][value1] == 'X' and constants_in_row[i][value2] == 'X':
                    if (constants_in_row[i][value1] == 'X' or 'P' in constants_in_row[i][value1]) and (constants_in_row[i][value2] == 'X' or 'P' in constants_in_row[i][value2]):
                        map2constants(i, value1, value2, constants_in_row)

                elif len(to_map) > 2:
                    # We have probably a problem
                    pass

    clean_constants_mapping(constants_in_row)

def clean_constants_mapping(constants_in_row):
    for i in range(1,len(constants_in_row)):
        mapped = []
        previous_routed = []
        still_to_map = []
        for val in constants_in_row[i]:
            if constants_in_row[i][val] == 'A' or constants_in_row[i][val] == 'B':
                mapped.append(val)
            elif 'P' in constants_in_row[i][val]:
                previous_routed.append(val)
            elif constants_in_row[i][val] == 'X':
                still_to_map.append(val)
        if len(mapped) == 1 and len(previous_routed) != 0:
            hops = []
            for value in previous_routed:
                hops.append(count_hops(i, value, constants_in_row))
            for j in range(len(hops)):
                if hops[j] == None:
                    hops[j] = 10000

            index_to_move = hops.index(max(hops))
            if constants_in_row[i][mapped[0]] == 'A':
                constants_in_row[i][previous_routed[index_to_move]] = 'B'
            else:
                constants_in_row[i][previous_routed[index_to_move]] = 'A'

        if len(still_to_map) > 0:
            # TODO
            pass

def need_desperate_mapping(constants_in_row):
    flag = False
    i = 0
    while not flag and i < len(constants_in_row):
        if 'X' in constants_in_row[i].values():
            flag = True

        i += 1

    return flag

def desperate_bottomup_mapping(constants_in_row):
    for i in range(len(constants_in_row)):
        if 'X' in constants_in_row[i].values():
            for value in constants_in_row[i]:
                if constants_in_row[i][value] == 'X':
                    switch_mapping(i,constants_in_row,value)

    # Retry normal bottom up
    bottomup_mapping(constants_in_row)

def switch_mapping(i,constants_in_row,value):
    for j in range(i-1,-1,-1):
        if value in constants_in_row[j] and constants_in_row[j][value] == 'B' and switchable(j,constants_in_row,value):
            for val in constants_in_row[j]:
                if constants_in_row[j][val] == 'A':
                    valA = val
                elif constants_in_row[j][val] == 'B':
                    valB = val
            constants_in_row[j][valA], constants_in_row[j][valB] = constants_in_row[j][valB], constants_in_row[j][valA]
            constants_in_row[i][value] = 'P_' + str(j)

def switchable(j,constants_in_row,value):
    flag = True
    for valA in constants_in_row[j]:
        if constants_in_row[j][valA] == 'A':
            i = 0
            while flag and i < len(constants_in_row):
                if valA in constants_in_row[i] and constants_in_row[i][valA] == 'P_' + str(j):
                    flag = False
                i += 1

    return flag

def desperate_bottomup_fill_mapping(constants_in_row):
    for i in range(len(constants_in_row)):
        if 'X' in constants_in_row[i].values():
            for value in constants_in_row[i]:
                if constants_in_row[i][value] == 'X':
                    bottomup_fill_mapping(i,constants_in_row,value)

    bottomup_mapping(constants_in_row)

def bottomup_fill_mapping(i,constants_in_row,value):
    for j in range(i-1,-1,-1):
        if len(constants_in_row[j]) == 0:
            constants_in_row[j][value] = 'A'
            constants_in_row[i][value] = 'P_' + str(j)
        if len(constants_in_row[j]) == 1:
            for val in list(constants_in_row[j].keys()):
                if constants_in_row[j][val] == 'B':
                    constants_in_row[j][value] = 'A'
                    constants_in_row[i][value] = 'P_' + str(j)
                elif constants_in_row[j][val] == 'A' and switchable(j, constants_in_row, value):
                    constants_in_row[j][val] = 'B'
                    constants_in_row[j][value] = 'A'
                    constants_in_row[i][value] = 'P_' + str(j)

def desperate_topdown_mapping(constants_in_row):
    # In case there are still 'X' in the mapping (because more than 2 constants to map up)
    # Top down try
    for i in range(len(constants_in_row)-1,-1,-1):
        if len(constants_in_row[i]) != 0:
            value = list(constants_in_row[i].keys())[0]
            if len(constants_in_row[i]) == 1 and constants_in_row[i][value] == 'B':
                constants_in_row[i][value] = 'A'

            for val in constants_in_row[i]:
                if constants_in_row[i][val] == 'A':
                    map_down(i,constants_in_row,val)

    # Bottom up retry
    bottomup_mapping(constants_in_row)

def map_down(i,constants_in_row,val):
    for j in range(i-1,-1,-1):
        for cst in constants_in_row[j]:
            if cst == val and constants_in_row[j][cst] == 'X':
                constants_in_row[j][cst] = 'P_' + str(i)

def desperate_topdown_fill_mapping(constants_in_row):
    for i in range(len(constants_in_row)):
        if 'X' in constants_in_row[i].values():
            for value in constants_in_row[i]:
                if constants_in_row[i][value] == 'X':
                    topdown_fill_mapping(i,constants_in_row,value)

    bottomup_mapping(constants_in_row)

def topdown_fill_mapping(i,constants_in_row,value):
    for j in range(i+1,len(constants_in_row)):
        if len(constants_in_row[j]) == 0:
            constants_in_row[j][value] = 'A'
            constants_in_row[i][value] = 'P_' + str(j)
        if len(constants_in_row[j]) == 1:
            for val in list(constants_in_row[j].keys()):
                if constants_in_row[j][val] == 'B':
                    constants_in_row[j][value] = 'A'
                    constants_in_row[i][value] = 'P_' + str(j)
                elif constants_in_row[j][val] == 'A' and switchable(j, constants_in_row, value):
                    constants_in_row[j][val] = 'B'
                    constants_in_row[j][value] = 'A'
                    constants_in_row[i][value] = 'P_' + str(j)


def count_hops(i,value,constants_in_row):
    hops = 0
    for k in range(i-1,-1,-1):
        if value not in constants_in_row[k] or (value in constants_in_row[k] and constants_in_row[k][value] != 'A'):
            hops += 1
        if value in constants_in_row[k] and constants_in_row[k][value] == 'A':
            hops += 1
            return hops

def map1constant(i,value,constants_in_row):
    next_map = []
    for val in constants_in_row[i+1]:   # TODO: this may need to go further
        if constants_in_row[i+1][val] == "X":
            next_map.append(val)
    if value in next_map:
        constants_in_row[i][value] = "A"
        for k in range(i+1,len(constants_in_row)):
            if value in constants_in_row[k]:
                constants_in_row[k][value] = "P_" + str(i)
    else:
        constants_in_row[i][value] = "B"

def map2constants(i,value1,value2,constants_in_row):
    next_appearance1 = 0
    next_appearance2 = 0
    j = i + 1
    while next_appearance1 == next_appearance2 and j < len(constants_in_row):
        if value1 in constants_in_row[j]:
            next_appearance1 += 1
        if value2 in constants_in_row[j]:
            next_appearance2 += 1

        j += 1

    if next_appearance1 > next_appearance2:
        constants_in_row[i][value1] = "A"
        constants_in_row[i][value2] = "B"
        for k in range(i+1,len(constants_in_row)):
            if value1 in constants_in_row[k]:
                constants_in_row[k][value1] = "P_" + str(i)
    else:
        constants_in_row[i][value1] = "B"
        constants_in_row[i][value2] = "A"
        for k in range(i+1,len(constants_in_row)):
            if value2 in constants_in_row[k]:
                constants_in_row[k][value2] = "P_" + str(i)

def mapmoreconstants(i,values,constants_in_row):
    next_appearance = [0 for i in range(len(values))]
    j = i + 1
    while len(set(next_appearance)) == 1 and j < len(constants_in_row):
        for k in range(len(values)):
            if values[k] in constants_in_row[j]:
                next_appearance[k] += 1

        j += 1

def constants_per_row(tasks_with_constant):
    tasks_with_constant.sort(key=lambda x: x[2][1])
    constants_in_row = [{} for i in range(tasks_with_constant[-1][2][1] + 1)]
    for i in range(len(tasks_with_constant)):
        if tasks_with_constant[i][1] not in constants_in_row[tasks_with_constant[i][2][1]]:
            constants_in_row[tasks_with_constant[i][2][1]][tasks_with_constant[i][1]] = "X"

    return constants_in_row

def reg_in_col(tasks,tasks_op,tasks_graph,individual):
    roots_list = roots_filter(tasksonly_graph)
    col_list = {}
    to_route = 0
    for root in roots_list:
        reg_val = tasks_op[root]['IN'][[i for i, elem in enumerate(tasks_op[root]['IN']) if 'REG_IN' in str(elem)][0]]
        if individual[root][0] not in col_list:
            col_list[individual[root][0]] = []
        if individual[root][1] == 0:
            routing = 'D'   # direct routing
        else:
            routing = 'ALU' + str(individual[root][0]) + '_' + str(individual[root][1])   # SE routing
            to_route += 1
        col_list[individual[root][0]].append((reg_val,routing))

    return col_list, to_route

def reg_in_mapping(tasks,tasks_op,tasks_graph,routed_platform_graph,routed_SE_graph,individual):
    routed_platform_graph = copy.deepcopy(platform_graph)
    routed_SE_graph = copy.deepcopy(SE_graph)
    col_list, to_route = reg_in_col(tasks,tasks_op,tasks_graph,individual)
    reg_map = {}
    paths_list = []
    routable = True
    samecol = True
    prevcol = True
    mapcol = True
    weight = 0

    # Managing all direct routing first
    for col in col_list:
        for i in range(len(col_list[col])-1, -1, -1):
            if col_list[col][i][1] == 'D':
                reg_map['REG_IN_' + str(col)] = col_list[col][i][0]
                paths_list.append(['REG_IN_' + str(col), 'ALU' + str(col) + '_' + str(0)])
                col_list[col].pop(i)

    # Attempt to route with mapped value on same col or map value if same col empty
    if to_route > 0:
        for col in col_list:
            if col_list[col] != []:
                for i in range(len(col_list[col])-1, -1, -1):
                    if 'REG_IN_' + str(col) not in reg_map:
                        source_node = 'REG_IN_' + str(col)
                        target_node = col_list[col][i][1]
                        try:
                            routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
                            route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
                            reg_map[source_node] = col_list[col][i][0]
                            col_list[col].pop(i)
                            to_route -= 1
                            paths_list.append(route_path)
                            for i in range(len(route_path) - 1):
                                weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
                                if 'SE' in route_path[i]:
                                    routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
                                    routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
                        except:
                            samecol = False
                    elif 'REG_IN_' + str(col) in reg_map and col_list[col][i][0] == reg_map['REG_IN_' + str(col)]:
                        source_node = 'REG_IN_' + str(col)
                        target_node = col_list[col][i][1]
                        try:
                            routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
                            route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
                            col_list[col].pop(i)
                            to_route -= 1
                            paths_list.append(route_path)
                            for i in range(len(route_path) - 1):
                                weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
                                if 'SE' in route_path[i]:
                                    routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
                                    routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
                        except:
                            samecol = False
                            # weight = 10000
                            # return paths_list, weight, reg_map

    # Attempt to route with value mapped on previous col or map/route in previous col
    if to_route > 0:
        for col in sorted(col_list.keys()):
            if col_list[col] != []:
                for i in range(len(col_list[col])-1, -1, -1):
                    local_routable = True
                    target_node = col_list[col][i][1]
                    for j in range(col-1,-1,-1):
                        local_routable = False
                        source_node = 'REG_IN_' + str(j)
                        if source_node in reg_map and reg_map[source_node] == col_list[col][i][0]:
                            try:
                                routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
                                route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
                                col_list[col].pop(i)
                                to_route -= 1
                                paths_list.append(route_path)
                                for i in range(len(route_path) - 1):
                                    weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
                                    if 'SE' in route_path[i]:
                                        routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
                                        routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
                                break
                            except:
                                prevcol = False

                        elif source_node not in reg_map:
                            try:
                                routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
                                route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
                                reg_map[source_node] = col_list[col][i][0]
                                col_list[col].pop(i)
                                to_route -= 1
                                paths_list.append(route_path)
                                for i in range(len(route_path) - 1):
                                    weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
                                    if 'SE' in route_path[i]:
                                        routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
                                        routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
                                break
                            except:
                                mapcol = False

    # Attempt to map/route on previous col
    # if to_route > 0:
    #     for col in sorted(col_list.keys()):
    #         if col_list[col] != []:
    #             for i in range(len(col_list[col])-1, -1, -1):
    #                 local_routable = True
    #                 target_node = col_list[col][i][1]
    #                 for j in range(col):
    #                     source_node = "REG_IN_" + str(j)
    #                     if source_node not in reg_map:
    #                         try:
    #                             routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
    #                             route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
    #                             reg_map[source_node] = col_list[col][i][0]
    #                             col_list[col].pop(i)
    #                             to_route -= 1
    #                             paths_list.append(route_path)
    #                             for i in range(len(route_path) - 1):
    #                                 weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
    #                                 if 'SE' in route_path[i]:
    #                                     routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
    #                                     routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
    #                             break
    #                         except:
    #                             mapcol = False

    # Attempt to route with value mapped on next col or map/route in next col
    if to_route > 0:
        for col in sorted(col_list.keys()):
            if col_list[col] != []:
                for i in range(len(col_list[col])-1, -1, -1):
                    local_routable = True
                    target_node = col_list[col][i][1]
                    for j in range(col+1, PE_col):
                        source_node = 'REG_IN_' + str(j)
                        if source_node in reg_map and reg_map[source_node] == col_list[col][i][0]:
                            try:
                                routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
                                route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
                                col_list[col].pop(i)
                                to_route -= 1
                                paths_list.append(route_path)
                                for i in range(len(route_path) - 1):
                                    weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
                                    if 'SE' in route_path[i]:
                                        routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
                                        routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
                                break
                            except:
                                prevcol = False

                        elif source_node not in reg_map:
                            try:
                                routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
                                route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
                                reg_map[source_node] = col_list[col][i][0]
                                col_list[col].pop(i)
                                to_route -= 1
                                paths_list.append(route_path)
                                for i in range(len(route_path) - 1):
                                    weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
                                    if 'SE' in route_path[i]:
                                        routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
                                        routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
                                break
                            except:
                                mapcol = False

    # Attempt to map/route on next col
    # if to_route > 0:
    #     for col in sorted(col_list.keys()):
    #         if col_list[col] != []:
    #             for i in range(len(col_list[col])-1, -1, -1):
    #                 local_routable = True
    #                 target_node = col_list[col][i][1]
    #                 for j in range(col+1, PE_col):
    #                     source_node = "REG_IN_" + str(j)
    #                     if source_node not in reg_map:
    #                         try:
    #                             routable_SE_graph = clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node)
    #                             route_path = heuristic_search(routable_SE_graph,source_node,target_node,SE_search_graph)
    #                             reg_map[source_node] = col_list[col][i][0]
    #                             col_list[col].pop(i)
    #                             to_route -= 1
    #                             paths_list.append(route_path)
    #                             for i in range(len(route_path) - 1):
    #                                 weight += routed_platform_graph.get_edge_properties((route_path[i],route_path[i+1]))['weight']
    #                                 if 'SE' in route_path[i]:
    #                                     routed_SE_graph.del_edge((route_path[i], route_path[i+1]))
    #                                     routed_platform_graph.del_edge((route_path[i], route_path[i+1]))
    #                             break
    #                         except:
    #                             mapcol = False

    if to_route > 0:
        weight = 10000
        return paths_list, weight, reg_map


    return paths_list, weight, reg_map

def clean_unroutable_nodes_reg(routed_SE_graph, source_node, target_node):
    routable_SE_graph = copy.deepcopy(routed_SE_graph)
    for node in routable_SE_graph.nodes():
        if 'ALU' in node and node != target_node:
            routable_SE_graph.del_node(node)

    # for edge in routable_SE_graph.edges():
    #     if edge[0] == source_node and 'ALU' in edge[1]:
    #         routable_SE_graph.del_edge(edge)

    return routable_SE_graph


def clean_unroutable_nodes(routed_SE_graph,source_node,target_node):
    routable_SE_graph = copy.deepcopy(routed_SE_graph)
    for node in routable_SE_graph.nodes():
        if 'ALU' in node and node != source_node and node != target_node:
            routable_SE_graph.del_node(node)

    ### Stupid constraint for SE not able to route West if coming from same ALU
    if 'ALU' in source_node:    # stupid check just to be sure
        associated_SE = source_node.replace('ALU','SE')
        source_node_coord = (int(re.sub('\D', '', source_node.split('_')[0])),int(source_node.split('_')[1]))
        west_coord = (source_node_coord[0]-1, source_node_coord[1])
        west_SE = 'SE' + str(west_coord[0]) + '_' + str(west_coord[1])
        west_ALU = 'ALU' + str(west_coord[0]) + '_' + str(west_coord[1])
        if (associated_SE,west_SE) in routable_SE_graph.edges():
            routable_SE_graph.del_edge((associated_SE,west_SE))
        if (associated_SE,west_ALU) in routable_SE_graph.edges():
            routable_SE_graph.del_edge((associated_SE,west_ALU))
    ###

    return routable_SE_graph

def path_evaluation(weighted_tasks_graph,path):
    """
    Compute the value of a path in a weighted_tasks_graph
    """
    value = 0
    for i in range(len(path)-1):
        value += weighted_tasks_graph.edge_weight((path[i],path[i+1]))

    return value

def total_value_evaluation(weighted_tasks_graph):
    """
    Compute the total value of a weighted_tasks_graph
    """
    value = 0
    for edge in weighted_tasks_graph.edges():
        value += weighted_tasks_graph.edge_weight(edge)

    return value

def rootsink_value_evaluation(tasks_graph,mapping):
    """
    Compute the distance from the register to the roots and from the sinks to the register
    """
    roots_list, sinks_list = rootsinks_filter(tasks_graph)
    value = 0
    for root in roots_list:
        value += mapping[root][1]

    for sink in sinks_list:
        value += mapping[sink][1]

    return value

def roots_value_evaluation(tasks_graph,mapping):
    """
    Compute the distance from the register to the roots
    """
    roots_list = roots_filter(tasks_graph)
    value = 0
    for root in roots_list:
        value += mapping[root][1] + mapping[root][0]

    return value

def roots_filter(tasks_graph):
    """
    Returns the list of roots from a tasks_graph (acyclic)
    """
    roots_list = []
    for node in tasks_graph.nodes():
        is_root = True
        i = 0
        while i < len(tasks_graph.edges()) and (is_root):
            if node == tasks_graph.edges()[i][1]:
                is_root = False

            i += 1

        if is_root:
            roots_list.append(node)

    return roots_list

def rootsinks_filter(tasks_graph):
    """
    Returns the list of roots and sinks from a tasks_graph (acyclic)
    """
    roots_list = []
    sinks_list = []
    for node in tasks_graph.nodes():
        is_root = True
        is_sink = True
        i = 0
        while i < len(tasks_graph.edges()) and (is_root or is_sink):
            if node == tasks_graph.edges()[i][1]:
                is_root = False

            if node == tasks_graph.edges()[i][0]:
                is_sink = False

            i += 1

        if is_root:
            roots_list.append(node)

        if is_sink:
            sinks_list.append(node)

    return roots_list, sinks_list

def intersect_filter(tasks_graph):
    """
    Returns the list of intersecting nodes
    """
    roots_list, sinks_list = rootsinks_filter(tasks_graph)
    inter_list = []
    target_nodes = [j for i,j in tasks_graph.edges()]
    for node in target_nodes:
        if target_nodes.count(node) > 1 and node not in inter_list and node not in sinks_list:
            inter_list.append(node)

    return inter_list


def mapping_width(individual):
    """
    Returns the width of the mapping (number of columns used)
    """
    min_x = individual[0][0]
    max_x = individual[0][0]
    for i in range(1,len(individual)):
        if individual[i][0] < min_x:
            min_x = individual[i][0]
        elif individual[i][0] > max_x:
            max_x = individual[i][0]
    return (max_x - min_x) + 1

def cxSet(ind1,ind2):
    """
    Crossover operation (single point)
    """
    # Check similar placement between ind1 and ind2 (children should inherit)
    # similar = []
    # for i in range(len(ind1)):
    #     if ind1[i] == ind2[i]:
    #         similar.append((i,ind1[i]))

    child1 = copy.deepcopy(ind1)
    child2 = copy.deepcopy(ind2)
    cx_point = random.randint(0,len(ind1)-1)
    for i in range(cx_point,len(ind1)):
        if ind2[i] not in ind1:
            child1[i] = ind2[i]
        if ind1[i] not in ind2:
            child2[i] = ind1[i]

    # shift_mapping(child1)
    # shift_mapping(child2)

    # if len(list(set(child1))) != len(child1) or len(list(set(child2))) != len(child2):
        # print('WTFcx')

    return child1, child2

def mutSet(PE_row,PE_col,individual):
    """
    Mutation operation: random change of one coordinate
    """
    # platform_col_nb = len(platform_graph[0])    # only size required??
    # platform_row_nb = len(platform_graph)
    if random.random() <= LSPB:  # Possibility of local search instead of random mutation
        # mut_index = random.randint(0,len(individual)-1)
        # cur_coord = individual[mut_index]
        # local_depth = DEPTH
        # possible_coordinates = []
        # while possible_coordinates == []:
        #     delta = list(range(-local_depth,local_depth+1))
        #     for i in delta:
        #         for j in delta:
        #             (new_x, new_y) = (cur_coord[0]+i, cur_coord[1]+j)
        #             if 0 <= new_x <= PE_col-1 and 0 <= new_y <= PE_row-1 and (new_x, new_y) not in individual:
        #                 possible_coordinates.append((new_x,new_y))

        #     local_depth += 1

        # new_coord = possible_coordinates[random.randint(0,len(possible_coordinates)-1)]
        # # while new_coord in individual:
        # #     new_coord = possible_coordinates[random.randint(0,len(possible_coordinates)-1)]

        # individual[mut_index] = new_coord

	# Possibility of swap mutation instead of random mutation
        mut_index1, mut_index2 = random.sample(range(len(individual)),2)
        individual[mut_index1], individual[mut_index2] = individual[mut_index2], individual[mut_index1]

    else:
        coord_x_list = list(range(PE_col))
        coord_y_list = list(range(PE_row))
        possible_coordinates = list(itertools.product(coord_x_list,coord_y_list))
        mut_index = random.randint(0,len(individual)-1)
        new_coord = possible_coordinates[random.randint(0,len(possible_coordinates)-1)]
        while new_coord in individual:
            new_coord = possible_coordinates[random.randint(0,len(possible_coordinates)-1)]

        individual[mut_index] = new_coord

        # if len(list(set(individual))) != len(individual):
        #     print('WTFmx')

    if random.random() <= SHPB:
        if random.random() <= SHPB0:
            shift_mapping(individual,(0,0))
        else:
            min_x, max_x, min_y, max_y = mapping_extreme_coord(individual)
            shift_x = random.randint(0,PE_col - max_x - 1)
            shift_y = random.randint(0,PE_row - max_y - 1)
            shift_mapping(individual,(shift_x,shift_y))

    return individual,

def shift_mapping(mapping,min_coord):
    min_x, max_x, min_y, max_y = mapping_extreme_coord(mapping)

    for i in range(len(mapping)):
        mapping[i] = (mapping[i][0] - min_x + min_coord[0], mapping[i][1] - min_y + min_coord[1])

# tasks_graph = digraph()
# tasks_graph.add_nodes(list(range(8)))
# tasks_graph.add_edge((0,1))
# tasks_graph.add_edge((1,2))
# tasks_graph.add_edge((1,3))
# tasks_graph.add_edge((3,4))
# tasks_graph.add_edge((4,5))
# tasks_graph.add_edge((4,6))
# tasks_graph.add_edge((5,7))
# tasks_graph.add_edge((6,7))
# tasks, tasks_graph = af_graph()


# test_platform_graph = [[0 for i in range(12)] for j in range(8)] # only size required?
platform_graph, SE_graph, ALU_graph = generate_cma_reg_graph(PE_row, PE_col) # CMA graph
platform_search_graph = euclidean()
SE_search_graph = euclidean()
ALU_search_graph = euclidean()
platform_search_graph.optimize(platform_graph)
SE_search_graph.optimize(SE_graph)
ALU_search_graph.optimize(ALU_graph)
# mapping1 = random_generator(tasks_graph,test_platform_graph)
# mapping2 = random_generator(tasks_graph,test_platform_graph)
# print(mapping1)
# print(mapping2)


# val, totval = objectives_eval(tasks_graph,mapping1)
# print(val)
# print(totval)

# SEED = 324
random.seed(SEED)

creator.create("Fitness", base.Fitness, weights=tuple([-1 for i in range(len(CRITERIA.split(',')))]))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Attribute generator
if GENERATOR_METHOD == "shortest-greedy":
    toolbox.register("attr_item",shortest_greedy_generator,tasks_graph,tasks_op,platform_graph,SE_graph,ALU_graph)
else:
    toolbox.register("attr_item",random_generator,tasks_graph,PE_row,PE_col)

# Structure initializers
toolbox.register("individual",tools.initIterate,creator.Individual,toolbox.attr_item)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)

toolbox.register("evaluate",objectives_eval,tasks_graph,platform_graph,SE_graph)
toolbox.register("mate",cxSet)
toolbox.register("mutate",mutSet,PE_row,PE_col)
toolbox.register("select",tools.selNSGA2)

def main():
    random.seed(SEED)
    # NGEN = 100
    # MU = 50
    # LAMBDA = 50
    # CXPB = 0.7
    # MUTPB = 0.3

    pop = toolbox.population(n=INIT_POP_SIZE)
    ref_sf_mapping = mapping = [(0,0),(1,0),(2,1),(0,1),(1,1),(1,2),(0,3),(0,2),(1,3),(2,3),(0,4),(1,4),(2,5),(0,5),(1,5),(2,6),(0,6),(1,6),(0,7),(1,7)]
    ref_gray_mapping = [(0,0),(1,0),(1,1),(0,1),(0,2),(0,3),(1,3),(0,4),(1,4),(0,5),(1,5),(0,6),(1,6)]
    if APPLICATION == 'sf':
        pop.append(creator.Individual(ref_sf_mapping))
    elif APPLICATION == 'gray':
        pop.append(creator.Individual(ref_gray_mapping))
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    tic = time.time()
    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)
    toc = time.time() - tic
    print(toc/3600,'h')
    if SAVE_FILE != "":
        pickle.dump([tasks_graph, platform_graph, SE_graph, pop, hof, toc], open(SAVE_FILE,'wb'),pickle.HIGHEST_PROTOCOL)
        # import pickle
        # from deap import creator
        # from deap import base
        # creator.create("Fitness", base.Fitness, weights=(-1, -1, -1))
        # creator.create("Individual", list, fitness=creator.Fitness)
        # tasks_graph, platform_graph, SE_graph, pop, hof, toc = pickle.load(open('greedy_astar3.sav','rb'))
    return pop, stats, hof

if __name__ == "__main__":
    main()
