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
from data_formatting import *

# CMA size
PE_row = 8
PE_col = 12

# Simulation settings
APPLICATION = 'af'
if APPLICATION == 'af':
    tasks, tasks_graph = af_graph()
elif APPLICATION == 'sf':
    tasks, tasks_graph = sf_graph()
NGEN = 250
MU = 100
INIT_POP_SIZE = MU * 3
LAMBDA = 200    # MU should be lower than LAMBDA
CXPB = 0.7
MUTPB = 0.3
LSPB = 0.5  # Local search probability (within mutation operation)
SHPB = 0.5
SHPB0 = 0.8
TIME = int(datetime.datetime.now().strftime('%y%m%d%H%M'))
FORCED_SEED = 0
if FORCED_SEED == 0:
    SEED = TIME
else:
    SEED = FORCED_SEED
DEPTH = 1
ROUTING_METHOD = "astar-routing"
GENERATOR_METHOD = "shortest-greedy"
CRITERIA = "(crit_value,total_value,width_value)"
SAVE_FILE = "results/" + str(TIME) + "_SEED" + str(SEED) + "_" + APPLICATION + "_" + CRITERIA + "_" + ROUTING_METHOD + "_" + GENERATOR_METHOD + "_CXPB" + str(CXPB) + "_MUTPB" + str(MUTPB) + "_LSPB" + str(LSPB) + "_SHPB" + str(SHPB) + "_SHPB0" + str(SHPB0) +"_DEPTH" + str(DEPTH) + ".sav"

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
        pool = shortest_greedy_generator(tasks_graph,platform_graph,SE_graph,ALU_graph)

    elif method == "grasp":
        pool = grasp_generator(tasks_graph,platform_graph)    # TODO: do it...
    else:
        pass    # TODO: proper else raise error routine

    return pool

def random_generator(tasks_graph,PE_row,PE_col):
    """
    Totally random generator
    """
    task_nb = len(tasks_graph.nodes())
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

def shortest_greedy_generator(tasks_graph,platform_graph,SE_graph,ALU_graph):
    """
    Generator using a randomized greedy algorithm
    TODO: clean the code!!!
    """
    task_nb = len(tasks_graph.nodes())
    topological_order = topological_sorting(tasks_graph)
    roots_list = roots_filter(tasks_graph)

    routed_platform_graph = copy.deepcopy(platform_graph)
    routed_SE_graph = copy.deepcopy(SE_graph)
    routed_ALU_graph = copy.deepcopy(ALU_graph)

    root_subgraphs = rootgraphs(topological_order,roots_list)
    random.shuffle(root_subgraphs)

    random_topological_order = [item for sublist in root_subgraphs for item in sublist] # flattening the list

    edges_list_sorted = []
    for node in random_topological_order:
        for edge in tasks_graph.edges():
            if edge[0] == node:
                edges_list_sorted.append(edge)

    mapping = [0 for i in range(task_nb)]
    placed = [False for i in range(len(random_topological_order))]
    used_nodes = []
    for (source_node, target_node) in edges_list_sorted:
        if placed[source_node] == False and placed[target_node] == False:
            if source_node in roots_list:
                # DEPTH = 2
                local_depth = DEPTH+1
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
    crit_value, crit_path, total_value = critical_path(tasks_graph,platform_graph,SE_graph,individual)
    width_value = mapping_width(individual)
    # return crit_value, width_value
    return eval(CRITERIA)

def critical_path(tasks_graph,platform_graph,SE_graph,individual):
    """
    Compute the critical path of the mapping (individual) in L1 distance
    on basis on the tasks_graph information (routing)
    Uses the pygraph library (http://faculty.lagcc.cuny.edu/tnagano/research/DOT/docs/pygraphDocs/pygraph-module.html)
    """
    if ROUTING_METHOD == "astar-routing":
        weighted_tasks_graph, _, _ = astar_tasks_routing(tasks_graph,platform_graph,SE_graph,individual)
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
    total_value += roots_value
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

def astar_tasks_routing(tasks_graph,platform_graph,SE_graph,individual):
    """
    Routing using a shortest path algorithm (A*) and some BFS
    """
    # roots_list, sinks_list = rootsinks_filter(tasks_graph)
    topological_order = topological_sorting(tasks_graph)
    edges_list_sorted = []
    for node in topological_order:
        for edge in tasks_graph.edges():
            if edge[0] == node:
                edges_list_sorted.append(edge)

    weighted_tasks_graph = copy.deepcopy(tasks_graph)
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
                return weighted_tasks_graph, edges_list_sorted, paths_list

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
                return weighted_tasks_graph, edges_list_sorted, paths_list

        if routable:
            for i in range(len(route_path)-1):
                if 'ALU' in route_path[i] and 'ALU' in route_path[i+1]:
                    routed_platform_graph.del_edge((route_path[i],route_path[i+1]))
                else:
                    routed_platform_graph.del_edge((route_path[i],route_path[i+1]))
                    routed_SE_graph.del_edge((route_path[i],route_path[i+1]))

            weight = path_evaluation(platform_graph,route_path)
            weighted_tasks_graph.set_edge_weight(edge,weight)
        else:
            pass
            # weight = 10000  # high weight penalty to not consider this individual
            # # TODO: some repair mechanism?
            # weighted_tasks_graph.set_edge_weight(edge,weight)

    return weighted_tasks_graph, edges_list_sorted, paths_list

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
platform_graph, SE_graph, ALU_graph = generate_cma_graph(PE_row, PE_col) # CMA graph
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
    toolbox.register("attr_item",shortest_greedy_generator,tasks_graph,platform_graph,SE_graph,ALU_graph)
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
