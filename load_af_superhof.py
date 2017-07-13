import pickle
import numpy as np
from moga_taskmapping_bbdlp import *
from paretofront import *

def load():
    tasks, tasks_graph, tasks_op = af_graph_reg()

    superhof = pickle.load( open("af_superhof.sav", "rb" ) )

    evaluations = []

    for mapping in superhof:
        evaluation = objectives_eval(tasks_graph,platform_graph,SE_graph,mapping)
        print(evaluation)
        evaluations.append(evaluation)

    crit_eval = np.array(evaluations)

    membership = member(crit_eval)

    pareto_hof = [[(i,j) for i,j in np.array(superhof)[np.nonzero(membership)[0],:][k]] for k in range(len(np.array(superhof)[np.nonzero(membership)[0],:]))]
    pareto_eval = [tuple(i) for i in crit_eval[np.nonzero(membership)[0],:]]

    # print(crit_eval[np.nonzero(membership)[0],:])

    ALU_config, SE_config, CONST_config, REG_config = generate_config_file(tasks, tasks_graph, tasks_op, platform_graph, SE_graph, pareto_hof)

    return pareto_hof, pareto_eval, ALU_config, SE_config, CONST_config, REG_config