from pygraph.classes.digraph import digraph

def sf_graph():
    tasks = ['SR_1','SR_2','AND_1','MULT_1','AND_2','MULT_2','ADD_1','MULT_3','ADD_2','SR_3','MULT_4','MULT_5','MULT_6','SR_4','SR_5','SR_6','SL_1','SL_2','OR_1','OR_2']
    # TODO: consider REG_IN and REG_OUT
    tasks_graph = digraph()
    tasks_graph.add_nodes(list(range(len(tasks))))
    tasks_graph.add_edge((0,3))
    tasks_graph.add_edge((1,4))
    tasks_graph.add_edge((2,5))
    tasks_graph.add_edge((3,6))
    tasks_graph.add_edge((4,7))
    tasks_graph.add_edge((7,6))
    tasks_graph.add_edge((6,8))
    tasks_graph.add_edge((5,8))
    tasks_graph.add_edge((8,9))
    tasks_graph.add_edge((9,10))
    tasks_graph.add_edge((9,11))
    tasks_graph.add_edge((9,12))
    tasks_graph.add_edge((10,13))
    tasks_graph.add_edge((11,14))
    tasks_graph.add_edge((12,15))
    tasks_graph.add_edge((13,16))
    tasks_graph.add_edge((14,17))
    tasks_graph.add_edge((16,18))
    tasks_graph.add_edge((17,18))
    tasks_graph.add_edge((18,19))
    tasks_graph.add_edge((15,19))

    return tasks, tasks_graph

def sf_graph_reg():
    SR_1 = {'IN': ['REG_IN_VAL_0',16]}
    SR_2 = {'IN': ['REG_IN_VAL_0',8]}
    AND_1 = {'IN': ['REG_IN_VAL_0',255]}
    MULT_1 = {'IN': ['SR_1',306]}
    AND_2 = {'IN': ['SR_2',255]}
    MULT_2 = {'IN': ['AND_1',117]}
    ADD_1 = {'IN': ['MULT_1','MULT_3']}
    MULT_3 = {'IN': ['AND_2',601]}
    ADD_2 = {'IN': ['ADD_1','MULT_2']}
    SR_3 = {'IN': ['ADD_2',10]}
    MULT_4 = {'IN': ['SR_3',240]}
    MULT_5 = {'IN': ['SR_3',200]}
    MULT_6 = {'IN': ['SR_3',145]}
    SR_4 = {'IN': ['MULT_4',8]}
    SR_5 = {'IN': ['MULT_5',8]}
    SR_6 = {'IN': ['MULT_6',8]}
    SL_1 = {'IN': ['SR_4',16]}
    SL_2 = {'IN': ['SR_5',8]}
    OR_1 = {'IN': ['SL_1','SL_2']}
    OR_2 = {'IN': ['OR_1','SR_6']}
    tasks = ['SR_1','SR_2','AND_1','MULT_1','AND_2','MULT_2','ADD_1','MULT_3','ADD_2','SR_3','MULT_4','MULT_5','MULT_6','SR_4','SR_5','SR_6','SL_1','SL_2','OR_1','OR_2','REG_IN']
    
    tasks_op = []
    for task in tasks[:-1]:
        OP = eval(task)
        tasks_op.append(OP)

    tasks_graph = digraph()
    tasks_graph.add_nodes(list(range(len(tasks)-1)))
    # REG_IN
    tasks_graph.add_node(-1)
    tasks_graph.add_edge((-1,0))
    tasks_graph.add_edge((-1,1))
    tasks_graph.add_edge((-1,2))
    # Tasks graph
    tasks_graph.add_edge((0,3))
    tasks_graph.add_edge((1,4))
    tasks_graph.add_edge((2,5))
    tasks_graph.add_edge((3,6))
    tasks_graph.add_edge((4,7))
    tasks_graph.add_edge((7,6))
    tasks_graph.add_edge((6,8))
    tasks_graph.add_edge((5,8))
    tasks_graph.add_edge((8,9))
    tasks_graph.add_edge((9,10))
    tasks_graph.add_edge((9,11))
    tasks_graph.add_edge((9,12))
    tasks_graph.add_edge((10,13))
    tasks_graph.add_edge((11,14))
    tasks_graph.add_edge((12,15))
    tasks_graph.add_edge((13,16))
    tasks_graph.add_edge((14,17))
    tasks_graph.add_edge((16,18))
    tasks_graph.add_edge((17,18))
    tasks_graph.add_edge((18,19))
    tasks_graph.add_edge((15,19))

    return tasks, tasks_graph, tasks_op

def af_graph():
    tasks = ['SR_1','SR_2','AND_1','AND_2','SR_3','AND_3','SR_4','AND_4','MULT_1','MULT_2','MULT_3','MULT_4','MULT_5','MULT_6','ADD_1','ADD_2','ADD_3','SR_5','SR_6','SR_7','SL_1','SL_2','OR_1','OR_2']
    tasks_graph = digraph()
    tasks_graph.add_nodes(list(range(len(tasks))))
    tasks_graph.add_edge((0,4))
    tasks_graph.add_edge((4,10))
    tasks_graph.add_edge((10,15))
    tasks_graph.add_edge((15,18))
    tasks_graph.add_edge((18,20))
    tasks_graph.add_edge((20,22))
    tasks_graph.add_edge((22,23))
    tasks_graph.add_edge((0,5))
    tasks_graph.add_edge((5,11))
    tasks_graph.add_edge((11,16))
    tasks_graph.add_edge((16,19))
    tasks_graph.add_edge((19,21))
    tasks_graph.add_edge((21,22))
    tasks_graph.add_edge((1,6))
    tasks_graph.add_edge((6,12))
    tasks_graph.add_edge((12,15))
    tasks_graph.add_edge((1,7))
    tasks_graph.add_edge((7,13))
    tasks_graph.add_edge((13,16))
    tasks_graph.add_edge((2,8))
    tasks_graph.add_edge((8,14))
    tasks_graph.add_edge((14,17))
    tasks_graph.add_edge((17,23))
    tasks_graph.add_edge((3,9))
    tasks_graph.add_edge((9,14))
    return tasks, tasks_graph

def af_graph_reg():
    SR_1 = {'IN': ['REG_IN_VAL_0',8]}
    SR_2 = {'IN': ['REG_IN_VAL_2',8]}
    AND_1 = {'IN': ['REG_IN_VAL_0',255]}
    AND_2 = {'IN': ['REG_IN_VAL_2',255]}
    SR_3 = {'IN': ['SR_1',8]}
    AND_3 = {'IN': ['SR_1',255]}
    SR_4 = {'IN': ['SR_2',8]}
    AND_4 = {'IN': ['SR_2',255]}
    MULT_1 = {'IN': ['AND_1',100]}
    MULT_2 = {'IN': ['AND_2',28]}
    MULT_3 = {'IN': ['SR_3',100]}
    MULT_4 = {'IN': ['AND_3',100]}
    MULT_5 = {'IN': ['SR_4',28]}
    MULT_6 = {'IN': ['AND_4',28]}
    ADD_1 = {'IN': ['MULT_1','MULT_2']}
    ADD_2 = {'IN': ['MULT_3','MULT_5']}
    ADD_3 = {'IN': ['MULT_4','MULT_6']}
    SR_5 = {'IN': ['ADD_1',7]}
    SR_6 = {'IN': ['ADD_2',7]}
    SR_7 = {'IN': ['ADD_3',7]}
    SL_1 = {'IN': ['SR_6',16]}
    SL_2 = {'IN': ['SR_7',8]}
    OR_1 = {'IN': ['SL_1','SL_2']}
    OR_2 = {'IN': ['OR_1','SR_5']}

    tasks = ['SR_1','SR_2','AND_1','AND_2','SR_3','AND_3','SR_4','AND_4','MULT_1','MULT_2','MULT_3','MULT_4','MULT_5','MULT_6','ADD_1','ADD_2','ADD_3','SR_5','SR_6','SR_7','SL_1','SL_2','OR_1','OR_2','REG_IN']
    tasks_op = []
    for task in tasks[:-1]:
        OP = eval(task)
        tasks_op.append(OP)

    # tasks = ['SR_1','SR_2','AND_1','AND_2','SR_3','AND_3','SR_4','AND_4','MULT_1','MULT_2','MULT_3','MULT_4','MULT_5','MULT_6','ADD_1','ADD_2','ADD_3','SR_5','SR_6','SR_7','SL_1','SL_2','OR_1','OR_2',8,255,100,28,7,16,'REG_IN']
    tasks_graph = digraph()
    tasks_graph.add_nodes(list(range(len(tasks)-1)))
    # REG_IN
    tasks_graph.add_node(-1)
    tasks_graph.add_edge((-1,0))
    tasks_graph.add_edge((-1,1))
    tasks_graph.add_edge((-1,2))
    tasks_graph.add_edge((-1,3))
    # Tasks graph
    tasks_graph.add_edge((0,4))
    tasks_graph.add_edge((4,10))
    tasks_graph.add_edge((10,15))
    tasks_graph.add_edge((15,18))
    tasks_graph.add_edge((18,20))
    tasks_graph.add_edge((20,22))
    tasks_graph.add_edge((22,23))
    tasks_graph.add_edge((0,5))
    tasks_graph.add_edge((5,11))
    tasks_graph.add_edge((11,16))
    tasks_graph.add_edge((16,19))
    tasks_graph.add_edge((19,21))
    tasks_graph.add_edge((21,22))
    tasks_graph.add_edge((1,6))
    tasks_graph.add_edge((6,12))
    tasks_graph.add_edge((12,15))
    tasks_graph.add_edge((1,7))
    tasks_graph.add_edge((7,13))
    tasks_graph.add_edge((13,16))
    tasks_graph.add_edge((2,8))
    tasks_graph.add_edge((8,14))
    tasks_graph.add_edge((14,17))
    tasks_graph.add_edge((17,23))
    tasks_graph.add_edge((3,9))
    tasks_graph.add_edge((9,14))
    return tasks, tasks_graph, tasks_op

def gray_graph_reg():
    SR_1 = {'IN': ['REG_IN_VAL_0',16]}
    SL_1 = {'IN': ['REG_IN_VAL_0',8]}
    AND_1 = {'IN': ['REG_IN_VAL_0',255]}
    SR_2 = {'IN': ['SL_1',16]}
    AND_2 = {'IN': ['SR_2',255]}
    ADD_1 = {'IN': ['SR_1','AND_2']}
    ADD_2 = {'IN': ['ADD_1','AND_1']}
    MULT_1 = {'IN': ['ADD_2',21]}
    SR_3 = {'IN': ['MULT_1',6]}
    SL_2 = {'IN': ['SR_3',8]}
    SL_3 = {'IN': ['SL_2',8]}
    OR_1 = {'IN': ['SL_2','SR_3']}
    OR_2 = {'IN': ['SL_3','OR_1']}
    tasks = ['SR_1','SL_1','AND_1','SR_2','AND_2','ADD_1','ADD_2','MULT_1','SR_3','SL_2','SL_3','OR_1','OR_2','REG_IN']
    
    tasks_op = []
    for task in tasks[:-1]:
        OP = eval(task)
        tasks_op.append(OP)

    tasks_graph = digraph()
    tasks_graph.add_nodes(list(range(len(tasks)-1)))
    # REG_IN
    tasks_graph.add_node(-1)
    tasks_graph.add_edge((-1,0))
    tasks_graph.add_edge((-1,1))
    tasks_graph.add_edge((-1,2))
    # Tasks graph
    tasks_graph.add_edge((0,5))
    tasks_graph.add_edge((5,6))
    tasks_graph.add_edge((6,7))
    tasks_graph.add_edge((7,8))
    tasks_graph.add_edge((8,9))
    tasks_graph.add_edge((8,11))
    tasks_graph.add_edge((9,10))
    tasks_graph.add_edge((9,11))
    tasks_graph.add_edge((10,12))
    tasks_graph.add_edge((11,12))
    tasks_graph.add_edge((1,3))
    tasks_graph.add_edge((3,4))
    tasks_graph.add_edge((4,5))
    tasks_graph.add_edge((2,6))

    return tasks, tasks_graph, tasks_op
    