import pickle
import os
import re
from deap import creator
from deap import base
from deap import tools
from moga_taskmapping_bbdlp import *
from data_formatting import *

files = ["/home/anhvu/Documents/Keio/Task mapping/Server/1701181734_SEED1701180845_af_(crit_value,total_value,width_value)_astar-routing_shortest-greedy_CXPB0.65_MUTPB0.35_LSPB0.5_SHPB0.5_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1701201722_SEED1701201722_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1701231132_SEED1701231132_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1701301353_SEED1701301353_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1701311238_SEED1701311238_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1702041120_SEED1702041120_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1702041122_SEED1702041122_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1702041123_SEED1702041123_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1702041941_SEED1702041941_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1702042221_SEED1702042221_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav",
"/home/anhvu/Documents/Keio/Task mapping/Server/1702042222_SEED1702042222_af_(crit_value,total_value,width_value,bbd_value)_astar-routing_shortest-greedy_CXPB0.7_MUTPB0.3_LSPB0.5_SHPB0.5_SHPB00.8_DEPTH1.sav"]

superhof = []
evaluations = []
for file_path in files:
    filename = os.path.basename(file_path)
    if '(' in filename:
        CRITERIA = re.split("\(|\)", filename)[1]
        print(CRITERIA)
        crit_nb = len(CRITERIA.split(','))
        w = tuple([-1 for i in range(crit_nb)])
    else:
        CRITERIA = "(crit_value,total_value,width_value)"
        w = (-1, -1, -1)

    creator.create("Fitness", base.Fitness, weights=w)
    creator.create("Individual", list, fitness=creator.Fitness)
    tasks_graph, platform_graph, SE_graph, pop, hof, toc = pickle.load(open(file_path,'rb'))
    tasks, tasks_graph, tasks_op = af_graph_reg()
    platform_graph, SE_graph, ALU_graph = generate_cma_reg_graph(PE_row, PE_col)

    for elem in hof:
        evaluation = objectives_eval(tasks_graph,platform_graph,SE_graph,elem)
        if evaluation[1] < 10000:
            superhof.append(list(elem))
            evaluations.append(evaluation)

