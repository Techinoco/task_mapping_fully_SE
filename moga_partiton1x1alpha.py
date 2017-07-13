#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import random
import sys
import csv
import numpy

from collections import defaultdict

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

IND_INIT_SIZE = 5
MAX_ITEM = 50
MAX_WEIGHT = 50
NBR_ITEMS = 20

# To assure reproductibility, the RNG seed is set prior to the items
# dict initialization. It is also seeded in main().
# SEED = 32
# random.seed(SEED)

creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Attribute generator
# toolbox.register("attr_item", random.randrange, NBR_ITEMS)

# Structure initializers
# toolbox.register("individual", tools.initRepeat, creator.Individual,
#     toolbox.attr_item, IND_INIT_SIZE)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def list_element_strtofloat(lname):
    result = []
    for e in lname:
        if e != '':
            if e.replace(".","", 1).replace("-","", 1).isdigit() == 1:
                result.append(float(e))
            else:
                result.append(e)
    return result

def mycsvread(arg):
    f = open(arg, 'r')
    try:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            #print  row
            yield(list_element_strtofloat(row))
    finally:
        f.close()

def main():
    if len(sys.argv) < 5:
        print("ga_renshu2.py EXPR_VALUES NUM_LATENCY NUM_SEED NGEN")
        exit(1)
    expr_values_filename = sys.argv[1]
#    apps_filename = sys.argv[2]
#    mapping_filename = sys.argv[3]
    num_latency = float(sys.argv[2])
    num_seed = int(sys.argv[3])
    NGEN = int(sys.argv[4])

    funcs = []
    Vbbs = []

    for f, v, i, l in mycsvread(expr_values_filename):
        if f not in funcs:
            funcs.append(f)
        if v not in Vbbs:
            Vbbs.append(v)

    expr_values_list = {}

    for i in funcs:
        if i not in expr_values_list.keys():
            expr_values_list[i] = {}
    for i in funcs:
        for j in Vbbs:
            if j not in expr_values_list[i].keys():
                expr_values_list[i][j] = defaultdict(lambda: 1000000000.0)

    for f, v, i, l in mycsvread(expr_values_filename):
        expr_values_list[f][v]["ibb"] = i
        expr_values_list[f][v]["latency"] = l

#    print expr_values_list

    for f in funcs:
        for v in Vbbs:
            print(f, v, expr_values_list[f][v])

    num_of_PEs = 16
    mappings = ['MULT', 'MULT', 'ADD', 'SR','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP']

    application_flows = [[0, 2, 3], [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]

    print(mappings)
    print(application_flows)

    GAContext = {}
    GAContext["funcs"] = funcs
    GAContext["Vbbs"] = Vbbs
    GAContext["expr_values_list"] = expr_values_list # expr_values_list[func][Vbbs] = [ibb, latency]
    GAContext["mappings"] = mappings # each values is an index of funcs
    GAContext["application_flows"] = application_flows # each elements is an index of mappings
    GAContext["num_latency"] = num_latency

    random.seed(num_seed)

    def _generateRandomIndividual():
        return [random.choice(GAContext["Vbbs"]) for x in mappings] # each values is an index of Vbbs, length is number of mappings

    toolbox.register("indices", _generateRandomIndividual)
    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def _get_max_latency(individual):
        max_latency = 0.0
        #print app_flows
        for flow in GAContext["application_flows"]:
            #print "flow:", flow
            # flow = [0, 1, 2] // index of mappings
            tmpflow_latency = 0.0
            for i_mappings in flow:
                #print GAContext["expr_values_list"][GAContext["mappings"][i_mappings]][individual[i_mappings]]["latency"]
                #print GAContext["mappings"][i_mappings], individual[i_mappings]
                tmp_latency = GAContext["expr_values_list"][GAContext["mappings"][i_mappings]][individual[i_mappings]]["latency"]

                tmpflow_latency += tmp_latency

            if max_latency < tmpflow_latency:
                max_latency = tmpflow_latency
        return max_latency

    def _get_sum_ibbs(individual):
        result = 0.0

        for i_mappings in range(len(individual)):
            tmp_ibbs = GAContext["expr_values_list"][GAContext["mappings"][i_mappings]][individual[i_mappings]]["ibb"]
            result += tmp_ibbs

        return result

    def _evalOneMax(individual):
        tmp_args = [individual]
        tmp_args.extend(GAContext.values())
        #print "tmp_args:", tmp_args
        ind_latency = _get_max_latency(individual)
        if ind_latency > GAContext["num_latency"]:          # WHY???
            return ind_latency, _get_sum_ibbs(individual),
        else:
            return 0.0, _get_sum_ibbs(individual),

    def cxSet(ind1, ind2):
        """Apply a crossover operation on input sets. The first child is the
        intersection of the two sets, the second child is the difference of the
        two sets.
        """
        toolbox.mate(ind1, ind2)
        return ind1, ind2

    def mutSet(individual):
        """Mutation that pops or add an element."""
        for i in range(len(individual)):
            individual[i] = random.choice(GAContext["Vbbs"])

        return individual,

    # toolbox.register("mate", tools.cxTwoPoints)
    toolbox.register("evaluate", _evalOneMax)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", mutSet)
    toolbox.register("select", tools.selNSGA2)

    # NGEN = 200
    MU = 200
    LAMBDA = 500
    CXPB = 0.7
    MUTPB = 0.3

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof)

    # maxLatencyHistory = []
    # for i in hof:
    #     maxLatencyHistory.append((i,_get_max_latency(i),_get_sum_ibbs(i)))
    # print(maxLatencyHistory)

    # print(min(maxLatencyHistory))
    # print(max(maxLatencyHistory))

    from matplotlib import pyplot as plt
    xseries = [i.fitness.values[0] for i in hof]
    yseries = [i.fitness.values[1] for i in hof]
    plt.plot(xseries,yseries,'.')
    plt.xlabel("latency")
    plt.ylabel("power")
    plt.grid(True)
    plt.show()

    return pop, stats, hof

if __name__ == "__main__":
    main()
