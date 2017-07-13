from pygraph.algorithms.heuristics.euclidean import euclidean
from pygraph.algorithms.heuristics.chow import chow
# from moga_taskmapping_bbdlp import *
import re
import copy

# from moga_taskmapping_bbdlp import *
import moga_taskmapping_bbdlp

def generate_config_file(tasks, tasks_graph, tasks_op, platform_graph, SE_graph, hof):
    """
    Generate configuration file for pipeline register optimization
    For ALU: N,E,SE,S,DS (Direct South),SW,W; 1 means receiving from input (REG_IN is sent to DS), 0 otherwise
    For SE: N,E,S,W; source input to output direction, 0 otherwise
    """
    ALU_config = []
    SE_config = []
    CONST_config = []
    REG_config = []

    for i in range(len(hof)):
        # filename = "data/" + "config_" + str(i+1) + ".map"
        # f = open(filename,'w')
        if (0,0) not in hof[i]:
            shift_mapping(hof[i],(0,0))
        weighted_tasks_graph, edges_list_sorted, paths_list, constants_path, constants_path_value, constants_map, reg_path, reg_path_value, reg_map, output_path = moga_taskmapping_bbdlp.astar_tasks_routing(tasks_graph,tasks_op,platform_graph,SE_graph,hof[i])
        CONST_conf = assignment_constants(constants_map)
        ALU_conf = ALU_instruction(tasks,hof[i])
        configure_ALU(hof[i], ALU_conf, CONST_conf, tasks_graph, paths_list, constants_path, reg_path, tasks, tasks_op)
        clean_instr_dict(ALU_conf)
        ALU_config.append(ALU_conf)
        SE_conf = configure_SE(paths_list, constants_path, reg_path)
        configure_output(output_path, SE_conf)
        SE_config.append(SE_conf)
        CONST_config.append(CONST_conf)
        REG_config.append(reg_map)
        
        # f.close()

    return ALU_config, SE_config, CONST_config, REG_config

def configure_output(output_path, SE_conf):
    for path in output_path:
        for i in range(len(path)):
            if 'SE' in path[i]:
                if path[i] not in SE_conf:
                    SE_conf[path[i]] = {}
                    SE_conf[path[i]]['N'] = 0
                    SE_conf[path[i]]['E'] = 0
                    SE_conf[path[i]]['S'] = 0
                    SE_conf[path[i]]['W'] = 0
                
                if i == len(path) -1 and path[i].split('_')[-1] == '0':
                    output_port = 'S'
                    SE_conf[path[i]][output_port] = path[i-1]
                else:
                    output_port = used_IO_port(path[i+1],path[i])
                    SE_conf[path[i]][output_port] = path[i-1]

def generate_map_file(coord, tasks, tasks_graph, filename):
    f = open(filename,'w')

    tasksonly_graph = copy.deepcopy(tasks_graph)
    tasksonly_graph.del_node(-1)
    cleaned_tasks = clean_tasks(tasks)
    roots, sinks = rootsinks_filter(tasksonly_graph)
    gath_end_buffer = ""

    for i in range(len(cleaned_tasks)):
        ID = str(i)
        task = cleaned_tasks[i]
        coord_X = str(coord[i][0])
        coord_Y = str(coord[i][1])
        target = list_target(i, tasksonly_graph)
        # print(ID,task,coord_X,coord_Y,target)
        if i not in sinks:
            f.write(ID + '\t' + task + '\t' + coord_X + '\t' + coord_Y + '\t' + target + '\n')
        else:
            sink_ID = sinks.index(i)
            target = str(len(tasks) -1 + 2 * sink_ID)
            gath_end_buffer = update_gath_end(gath_end_buffer, tasks, coord, sinks, sink_ID)
            f.write(ID + '\t' + task + '\t' + coord_X + '\t' + coord_Y + '\t' + target + '\n')

    f.write(gath_end_buffer)
    f.close()

def update_gath_end(gath_end_buffer, tasks, coord, sinks, sink_ID):
    i = len(tasks) -1 + 2 * sink_ID
    sink = sinks[sink_ID]
    GATH_ID = str(i)
    GATH = "GATH" + str(coord[sink][1]+1)
    GATH_X = str(coord[sink][0])
    GATH_Y = str(8)
    i += 1
    GATH_target = str(i)
    END_ID = str(i)
    END = "END"
    END_X = str(coord[sink][0])
    END_Y = str(9)
    END_target = '%'
    gath_end_buffer += GATH_ID + '\t' + GATH + '\t' + GATH_X + '\t' + GATH_Y + '\t' + GATH_target + '\n'
    gath_end_buffer += END_ID + '\t' + END + '\t' + END_X + '\t' + END_Y + '\t' + END_target + '\n'

    return gath_end_buffer
    

def list_target(node_id, tasks_graph):
    target = []
    for edge in tasks_graph.edges():
        if node_id == edge[0]:
            target.append(str(edge[1]))

    target = "\t".join(target)
    return target

def assignment_constants(constants_map):
    rev_constants_map = [{v: k for k, v in constants_map[i].items()} for i in range(len(constants_map))]
    CONST_config = {}
    for i in range(len(rev_constants_map)):
        for key in rev_constants_map[i]:
            if key == 'A' or key == 'B':
                new_key = 'C_' + str(i) + key
                CONST_config[new_key] = rev_constants_map[i][key]

    return CONST_config


def configure_SE(paths_list, constants_path, reg_path):
    SE_config = {}
    extended_paths_list = reg_path + paths_list
    for path in extended_paths_list:
        for i in range(len(path)):
            if 'SE' in path[i]:
                if path[i] not in SE_config:
                    SE_config[path[i]] = {}
                    SE_config[path[i]]['N'] = 0
                    SE_config[path[i]]['E'] = 0
                    SE_config[path[i]]['S'] = 0
                    SE_config[path[i]]['W'] = 0
                output_port = used_IO_port(path[i+1],path[i])
                SE_config[path[i]][output_port] = path[i-1]

    for path in constants_path:
        for i in range(len(path)):
            if 'SE' in path[i]:
                if path[i] not in SE_config:
                    SE_config[path[i]] = {}
                    SE_config[path[i]]['N'] = 0
                    SE_config[path[i]]['E'] = 0
                    SE_config[path[i]]['S'] = 0
                    SE_config[path[i]]['W'] = 0
                output_port = used_IO_port(path[i+1],path[i])
                SE_config[path[i]][output_port] = path[i-1]

    return SE_config

def ALU_instruction(tasks,mapping):
    # cleaned_tasks = clean_tasks(tasks)
    ALU_config = {}
    for i in range(len(mapping)):
        ALU_coord = 'ALU' + str(mapping[i][0]) + '_' + str(mapping[i][1])
        ALU_config[ALU_coord] = {}
        # ALU_config[ALU_coord]['instr'] = cleaned_tasks[i]
        ALU_config[ALU_coord]['instr'] = tasks[i]
        ALU_config[ALU_coord]['N'] = 0
        ALU_config[ALU_coord]['E'] = 0
        ALU_config[ALU_coord]['SE'] = 0
        ALU_config[ALU_coord]['S'] = 0
        ALU_config[ALU_coord]['DS'] = 0
        ALU_config[ALU_coord]['SW'] = 0
        ALU_config[ALU_coord]['W'] = 0
        ALU_config[ALU_coord]['CA'] = 'None'
        ALU_config[ALU_coord]['CB'] = 'None'

    return ALU_config

def configure_ALU(mapping, ALU_config, CONST_config, tasks_graph, paths_list, constants_path, reg_path, tasks,tasks_op):
    # roots_ALU, sinks_ALU = roots_sinks_ALU(mapping,tasks_graph)
    # for node in roots_ALU:
    #     ALU_config[node]['S'] = 1   # Receiving from REG_IN at S input
    extended_paths_list = reg_path + paths_list
    for path in extended_paths_list:
        target_node = path[-1]
        target_instr = ALU_config[target_node]['instr']
        target_instr_idx = tasks.index(target_instr)
        if 'REG_IN' in path[0] and 'ALU' in path[1]:
            reg_name = tasks_op[target_instr_idx]['IN'][[i for i, elem in enumerate(tasks_op[target_instr_idx]['IN']) if 'REG_IN' in str(elem)][0]]
            ALU_config[target_node]['S'] = convert_index_letter(tasks_op[target_instr_idx]['IN'].index(reg_name))
        else:
            source_node = path[0]
            if 'REG_IN' in source_node:
                source_instr = source_node
            else:
                source_instr = ALU_config[source_node]['instr']
            input_port = used_IO_port(path[-2],path[-1])
            if 'REG_IN' in source_instr:
                source_instr = tasks_op[target_instr_idx]['IN'][[i for i, elem in enumerate(tasks_op[target_instr_idx]['IN']) if 'REG_IN' in str(elem)][0]]
            ALU_config[target_node][input_port] = convert_index_letter(tasks_op[target_instr_idx]['IN'].index(source_instr))

    for path in constants_path:
        target_node = path[-1]
        target_instr = ALU_config[target_node]['instr']
        target_instr_idx = tasks.index(target_instr)
        source_node = path[0]
        if 'C_' in path[0] and 'ALU' in path[1]:
            register = path[0][-1]  # We consider one letter
            for key in ALU_config[target_node]:
                if key == 'C' + register:
                    ALU_config[target_node][key] = convert_index_letter(tasks_op[target_instr_idx]['IN'].index(CONST_config[source_node]))
        else:   # It goes through some SEs
            input_port = used_IO_port(path[-2],path[-1])
            ALU_config[target_node][input_port] = convert_index_letter(tasks_op[target_instr_idx]['IN'].index(CONST_config[source_node]))

def convert_index_letter(val):
    return chr(ord('A') + val)

def used_IO_port(source,target):
    source_node_coord = (int(re.sub('\D', '', source.split('_')[0])),int(source.split('_')[1]))
    target_node_coord = (int(re.sub('\D', '', target.split('_')[0])),int(target.split('_')[1]))
    if source_node_coord[0] == target_node_coord[0] and source_node_coord[1] == target_node_coord[1] + 1:
        return 'N'
    elif source_node_coord[0] == target_node_coord[0] + 1 and source_node_coord[1] == target_node_coord[1]:
        return 'E'
    elif source_node_coord[0] == target_node_coord[0] + 1 and source_node_coord[1] == target_node_coord[1] - 1:
        return 'SE'
    elif source_node_coord[0] == target_node_coord[0] and source_node_coord[1] == target_node_coord[1] - 1 and 'ALU' not in source:
        return 'S'
    elif source_node_coord[0] == target_node_coord[0] and source_node_coord[1] == target_node_coord[1] - 1 and 'ALU' in source:
        return 'DS'
    elif source_node_coord[0] == target_node_coord[0] - 1 and source_node_coord[1] == target_node_coord[1] - 1:
        return 'SW'
    elif source_node_coord[0] == target_node_coord[0] - 1 and source_node_coord[1] == target_node_coord[1]:
        return 'W'

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

def roots_sinks_ALU(mapping,tasks_graph):
    roots_list, sinks_list = rootsinks_filter(tasks_graph)
    roots_ALU = []
    sinks_ALU = []
    for node in roots_list:
        roots_ALU.append('ALU' + str(mapping[node][0]) + '_' + str(mapping[node][1]))

    for node in sinks_list:
        sinks_ALU.append('ALU' + str(mapping[node][0]) + '_' + str(mapping[node][1]))

    return roots_ALU, sinks_ALU

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

def shift_mapping(mapping,min_coord):
    min_x, max_x, min_y, max_y = mapping_extreme_coord(mapping)

    for i in range(len(mapping)):
        mapping[i] = (mapping[i][0] - min_x + min_coord[0], mapping[i][1] - min_y + min_coord[1])

def clean_tasks(tasks):
    return list(map(lambda x: x.split('_')[0], tasks))[:-1]

def clean_instr_dict(ALU_config):
    for key in ALU_config:
        instr = ALU_config[key]['instr']
        ALU_config[key]['instr'] = instr.split('_')[0]
