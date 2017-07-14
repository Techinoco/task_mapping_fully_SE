import random
import sys
import csv
import numpy
import itertools
import copy

from pygraph.classes.digraph import digraph
from pygraph.algorithms.critical import critical_path as pygraphcp

from collections import defaultdict

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

def generate_random_individuals(n,tasks_graph,platform_graph,method="random"):
    """
    Generates n random individuals (random placement)
    from the tasks_graph to the platform_graph
    3 possible methods: random (default), greedy or GRASP
    tasks_graph: pygraph digraph
    platform_graph: whatever?
    """
    # TODO: redo the doc
    if method == "random":
        pool = random_generator(tasks_graph,platform_graph)

    elif method == "greedy":
        pool = greedy_generator(n,tasks_graph,platform_graph)   # TODO: check if parameter n is relevant

    elif method == "grasp":
        pool = grasp_generator(n,tasks_graph,platform_graph)    # TODO: doc on GRASP...
    else:
        pass    # TODO: proper else raise error routine

    return pool

def random_generator(tasks_graph,platform_graph):
    """
    Totally random generator
    """
    task_nb = len(tasks_graph.nodes())
    platform_col_nb = len(platform_graph[0])    # only size required??
    platform_row_nb = len(platform_graph)
    coord_x_list = list(range(platform_col_nb))
    coord_y_list = list(range(platform_row_nb))
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

def objectives_eval(individual,tasks_graph):
    """
    Compute the objectives evaluation
    TODO: add more objectives
    """
    crit_value, crit_path, total_value = critical_path(individual,tasks_graph)
    return crit_value, total_value

def critical_path(tasks_graph,individual):
    """
    Compute the critical path of the mapping (individual) in L1 distance
    on basis on the tasks_graph information (routing)
    Uses the pygraph library (http://faculty.lagcc.cuny.edu/tnagano/research/DOT/docs/pygraphDocs/pygraph-module.html)
    """
    weighted_tasks_graph = copy.deepcopy(tasks_graph)
    for (node1,node2) in weighted_tasks_graph.edges():
        # TODO: Routing
        weight = abs(individual[node1][0]-individual[node2][0]) + abs(individual[node1][1]-individual[node2][1])
        weighted_tasks_graph.set_edge_weight((node1,node2),weight)

    crit_path = pygraphcp(weighted_tasks_graph)
    crit_value = path_evaluation(weighted_tasks_graph,crit_path)
    total_value = total_value_evaluation(weighted_tasks_graph)
    # rootsink_value = rootsink_value_evaluation(weighted_tasks_graph,individual)
    roots_value = roots_value_evaluation(weighted_tasks_graph,individual)
    crit_value += roots_value
    total_value += roots_value
    return crit_value, crit_path, total_value

def tasks_routing(tasks_graph,individual):
    roots_list, sinks_list = rootsinks_filter(tasks_graph)

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
    roots_list, sinks_list = rootsinks_filter(tasks_graph)
    value = 0
    for root in roots_list:
        value += mapping[root][1]

    for sink in sinks_list:
        value += mapping[sink][1]

    return value

def roots_value_evaluation(tasks_graph,mapping):
    roots_list = roots_filter(tasks_graph)
    value = 0
    for root in roots_list:
        value += mapping[root][1]

    return value

def roots_filter(tasks_graph):
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
        if ind2[i] not in ind1[:cx_point]:
            child1[i] = ind2[i]
        if ind1[i] not in ind2[:cx_point]:
            child2[i] = ind1[i]

    return child1, child2

def mutSet(platform_graph,individual):
    """
    Mutation operation: random change of one coordinate
    """
    platform_col_nb = len(platform_graph[0])    # only size required??
    platform_row_nb = len(platform_graph)
    coord_x_list = list(range(platform_col_nb))
    coord_y_list = list(range(platform_row_nb))
    possible_coordinates = list(itertools.product(coord_x_list,coord_y_list))
    mut_index = random.randint(0,len(individual)-1)
    new_coord = possible_coordinates[random.randint(0,len(possible_coordinates)-1)]
    while new_coord in individual:
        new_coord = possible_coordinates[random.randint(0,len(possible_coordinates)-1)]

    individual[mut_index] = new_coord

    return individual,

test_tasks_graph = digraph()
test_tasks_graph.add_nodes(list(range(8)))
test_tasks_graph.add_edge((0,1))
test_tasks_graph.add_edge((1,2))
test_tasks_graph.add_edge((1,3))
test_tasks_graph.add_edge((3,4))
test_tasks_graph.add_edge((4,5))
test_tasks_graph.add_edge((4,6))
test_tasks_graph.add_edge((5,7))
test_tasks_graph.add_edge((6,7))

test_platform_graph = [[0 for i in range(12)] for j in range(8)] # only size required?

# mapping1 = random_generator(test_tasks_graph,test_platform_graph)
# mapping2 = random_generator(test_tasks_graph,test_platform_graph)
# print(mapping1)
# print(mapping2)


# val, totval = objectives_eval(test_tasks_graph,mapping1)
# print(val)
# print(totval)

SEED = 324
random.seed(SEED)

creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_item",random_generator,test_tasks_graph,test_platform_graph)

# Structure initializers
toolbox.register("individual",tools.initIterate,creator.Individual,toolbox.attr_item)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)

toolbox.register("evaluate",objectives_eval,test_tasks_graph)
toolbox.register("mate",cxSet)
toolbox.register("mutate",mutSet,test_platform_graph)
toolbox.register("select",tools.selNSGA2)

def main():
    random.seed(SEED)
    NGEN = 50
    MU = 150
    LAMBDA = 300
    CXPB = 0.7
    MUTPB = 0.3

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)

    return pop, stats, hof

if __name__ == "__main__":
    main()
