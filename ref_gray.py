from moga_taskmapping_bbdlp import *

mapping = [(0,0),(1,0),(1,1),(0,1),(0,2),(0,3),(1,3),(0,4),(1,4),(0,5),(1,5),(0,6),(1,6)]

hof = [mapping]

for i in range(len(hof)):
    weighted_tasks_graph, edges_list_sorted, paths_list, constants_path, constants_path_value, constants_map, reg_path, reg_path_value, reg_map, output_path = astar_tasks_routing(tasks_graph,tasks_op,platform_graph,SE_graph,hof[i])
    print(i,objectives_eval(tasks_graph,platform_graph,SE_graph,hof[i]),mapping_size(hof[i]))

ALU_config, SE_config, CONST_config, REG_config = generate_config_file(tasks, tasks_graph, tasks_op, platform_graph, SE_graph, hof)
