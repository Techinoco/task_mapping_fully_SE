from copy import *
from moga_taskmapping_bbdlp import *

reg_inputs = {'REG_IN_VAL_0': 66309,
              'REG_IN_VAL_2': 527374}

def simulate(tasks, tasks_op, reg_inputs):
    roots_list, sinks_list = rootsinks_filter(tasksonly_graph)
    tasks_out = copy.deepcopy(tasks_op)
    for i in range(len(tasks)-1):
        tasks_out[i]['instr'] = tasks[i]
        if 'REG' in tasks_out[i]['IN'][0]:
            tasks_out[i]['IN'][0] = reg_inputs[tasks_out[i]['IN'][0]]

    for path in all_paths:
        for node in path:
            inputs = tasks_out[node]['IN']
            if check_inputs(inputs):
                operation = tasks_out[node]['instr']
                result = execute_operation(operation, inputs)
                tasks_out[node]['OUT'] = result
                update_tasks_out(tasks_out, operation, result)
    
    answer = []
    for sink in sinks_list:
        answer.append(tasks_out[sink]['OUT'])

    return tasks_out, answer

def update_tasks_out(tasks_out, inp, value):
    for node in tasks_out:
        if inp in node['IN']:
            node['IN'][node['IN'].index(inp)] = value

def check_inputs(inputs):
    for inp in inputs:
        if not isinstance(inp,(int,float)): # and type(inp) != 'float':
            return False

    return True

def execute_operation(operation, inputs):
    # ADD, SUB, MULT, PASS, NOP, AND, OR, SL, SR
    if 'ADD' in operation:
        result = inputs[0] + inputs[1]
    elif 'SUB' in operation:
        result = inputs[0] - inputs[1]
    elif 'MULT' in operation:
        result = inputs[0] * inputs[1]
    elif 'PASS' in operation:
        pass
    elif 'NOP' in operation:
        pass
    elif 'AND' in operation:
        result = inputs[0] & inputs[1]
    elif 'OR' in operation:
        result = inputs[0] | inputs[1]
    elif 'SL' in operation:
        result = inputs[0] << inputs[1]
    elif 'SR' in operation:
        result = inputs[0] >> inputs[1]

    return result
