import pickle
import os
import re
from deap import creator
from deap import base
from deap import tools
from moga_taskmapping_bbdlp import *
from data_formatting import *

pm = input("Import plot_mapping? ([y]/n) ")
if pm.lower() == 'y' or pm.lower() == '':
    print("Loading plot_mapping")
    from plot_mapping import *

import tkinter as tk
from tkinter import filedialog

def clean_hof(hof):
    cleaned_hof = tools.support.ParetoFront()
    for i in range(len(hof)):
        if hof.keys[i].values[0] < 10000:
            cleaned_hof.insert(hof[len(hof)-i-1])

    return cleaned_hof


def load_savefile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    filename = os.path.basename(file_path)
    print("Loading file: " + filename)

    ref_mapping = [(0,0),(1,0),(2,1),(0,1),(1,1),(1,2),(0,3),(0,2),(1,3),(2,3),(0,4),(1,4),(2,5),(0,5),(1,5),(2,6),(0,6),(1,6),(0,7),(1,7)]

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

    cleaned_hof = clean_hof(hof)
    # individual = cleaned_hof[23]
    # routed_platform_graph = platform_graph
    # objectives_eval(tasks_graph,platform_graph,SE_graph,cleaned_hof[11])
    # c = constants_mapping(tasks,tasks_op,tasks_graph,platform_graph,SE_graph,cleaned_hof[11])
    for i in range(len(cleaned_hof)):
        # print(i,objectives_eval(tasks_graph,platform_graph,SE_graph,cleaned_hof[i]),len(list(set(cleaned_hof[i]))))
        print(i,objectives_eval(tasks_graph,platform_graph,SE_graph,cleaned_hof[i]),mapping_size(cleaned_hof[i]))
        # crit_value, total_value, width_value, bbd_value = objectives_eval(tasks_graph,platform_graph,SE_graph,cleaned_hof[i])
        # print(crit_value,width_value,bbd_value,mapping_size(cleaned_hof[i]))
        # print(crit_value,mapping_size(cleaned_hof[i])[1],mapping_size(cleaned_hof[i])[0])

    ALU_config, SE_config, CONST_config, REG_config = generate_config_file(tasks, tasks_graph, tasks_op, platform_graph, SE_graph, cleaned_hof)
    # individual = hof[30]
    # c = constants_mapping(tasks,tasks_op,tasks_graph,platform_graph,SE_graph,individual)

    return cleaned_hof, ALU_config, SE_config, CONST_config, REG_config


loadsav = input("What do you want to load? (sav/af/...) ")
if loadsav.lower() == "sav":
    hof, ALU_config, SE_config, CONST_config, REG_config = load_savefile()
elif loadsav.lower() == "af":
    import load_af_superhof
    hof, evaluations, ALU_config, SE_config, CONST_config, REG_config = load_af_superhof.load()