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
import csv
import sys
from   deap import base
from   deap import creator
from   deap import tools
from collections import defaultdict

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

    if len(sys.argv) < 4:
        print "ga_renshu2.py EXPR_VALUES NUM_LATENCY NUM_SEED"
        exit(1)
    expr_values_filename = sys.argv[1]
#    apps_filename = sys.argv[2]
#    mapping_filename = sys.argv[3]
    num_latency = float(sys.argv[2])
    num_seed = int(sys.argv[3])

    print expr_values_filename, num_latency, num_seed

    funcs = []
    Vbbs = []

    for f, v, i, l in mycsvread(expr_values_filename):
        if f not in funcs:
            funcs.append(f)
        if v not in Vbbs:
            Vbbs.append(v)

    expr_values_list = {} #expr_values_list["ADD"][0.2]["ibb"] = ibb


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
            print f, v, expr_values_list[f][v]

    random.seed(6)

    num_of_PEs = 16
    mappings = ['MULT', 'MULT', 'ADD', 'SR','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP','NOP']

#    num_PEs_in_flows1, num_PEs_in_flows2 = 3, 5

#    application_flows = [[random.randint(0, num_of_PEs - 1) for i in xrange(num_PEs_in_flows1)], [random.randint(0, num_of_PEs - 1) for i in xrange(num_PEs_in_flows2)]]

    application_flows = [[0, 2, 3], [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]

    print mappings
    print application_flows

    random.seed(num_seed)

#    exit(1)

#    pathsInH_indices = [12,12,12,12,12,12]

    GAContext = {}
    GAContext["funcs"] = funcs
    GAContext["Vbbs"] = Vbbs
    GAContext["expr_values_list"] = expr_values_list # expr_values_list[func][Vbbs] = [ibb, latency]
    GAContext["mappings"] = mappings # each values is an index of funcs
    GAContext["application_flows"] = application_flows # each elements is an index of mappings
    GAContext["num_latency"] = num_latency

#    print GAContext
#    print GAContext.values()

#    print "default_value?:", GAContext["expr_values_list"]["MULT"][-1.2]["ibb"]
#    exit(1)

    creator.create("FitnessMax", base.Fitness, weights=(-1.0, -1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    def _generateRandomIndividual():
        return [random.choice(GAContext["Vbbs"]) for x in mappings] # each values is an index of Vbbs, length is number of mappings

    toolbox = base.Toolbox()
    # Attribute generator
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

        for i_mappings in xrange(len(individual)):
            tmp_ibbs = GAContext["expr_values_list"][GAContext["mappings"][i_mappings]][individual[i_mappings]]["ibb"]
            result += tmp_ibbs

        return result

    def _evalOneMax(individual):
        tmp_args = [individual]
        tmp_args.extend(GAContext.values())
        #print "tmp_args:", tmp_args
        ind_latency = _get_max_latency(individual)
        if ind_latency > GAContext["num_latency"]:
            return ind_latency, _get_sum_ibbs(individual),
        else:
            return 0.0, _get_sum_ibbs(individual),

    def _myMutate(individual, mutnpb):
#        print mutnpb
        for i in xrange(len(individual)):
            if random.random() < mutnpb:
#                print "mutation occurs"
                individual[i] = random.choice(GAContext["Vbbs"])

    # Operator registering
    toolbox.register("evaluate", _evalOneMax)
    toolbox.register("mate", tools.cxTwoPoints)
    #toolbox.register("mate", tools.cxOnePoint)
    #toolbox.register("mate", tools.cxUniform, indpb = 0.05)
    toolbox.register("mutate", _myMutate)
    toolbox.register("select", tools.selTournament, tournsize=3)


    pop = toolbox.population(n=1400)
    CXPB, MUTPB, NGEN = 0.7, 0.3, 1400
    MUTNPB = 0.3

    print "Start of evolution"

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print "  Evaluated %i individuals" % len(pop)

    # Begin the evolution
    maxFitnessHistory = []
    for g in range(NGEN):
        print "-- Generation %i --" % g

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
#                print "before:", mutant
                toolbox.mutate(mutant, MUTNPB)
#                print "after:", mutant
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print "  Evaluated %i individuals" % len(invalid_ind)

        # The population is entirely replaced by the offspring
        # pop[:] = offspring
        pop = pop + offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [sum(ind.fitness.values) for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print "  Min %s" % min(fits)
        print "  Max %s" % max(fits)
        print "  Avg %s" % mean
        print "  Std %s" % std
        best_ind = tools.selBest(pop, 1)[0]
        print "Best individual is %s, %s, %s" % (best_ind, best_ind.fitness.values, _get_max_latency(best_ind))

        pop = tools.selBest(pop, 1400)

        # Stop when the last 90 generations have led to no improvements
        if g == 0:
            previous_best = max(fits)
            maxFitnessHistory.append(max(fits))
        elif previous_best > max(fits):
            maxFitnessHistory.append(maxFitnessHistory[-1])
        else:
            previous_best = max(fits)
            maxFitnessHistory.append(max(fits))
        print maxFitnessHistory

        if ((len(maxFitnessHistory) > 100) and (len(set(maxFitnessHistory[(len(maxFitnessHistory)-90):])) == 1)):
            break

    print "-- End of (successful) evolution --"

    best_ind = tools.selBest(pop, 1)[0]
    print "Best individual is %s, %s, %s" % (best_ind, best_ind.fitness.values, _get_max_latency(best_ind))

if __name__ == "__main__":
    main()
