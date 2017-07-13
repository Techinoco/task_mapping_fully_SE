from moga_taskmapping_bbdlp import *
from itertools import combinations
vpcma_graph = digraph()

def read_delay(delay_file):
    delay_dict = {}
    with open(delay_file, 'r') as f:
        for row in f:
            column = row.split()
            delay_dict[column[0]] = float(column[1])

    return delay_dict

def read_graph(map_file,delay_file):
    delay_dict = read_delay(delay_file)
    with open(map_file, 'r') as f0:
        for row0 in f0:
            node = row0.split()
            node_num = int(node[0])
            node_x = node[2]
            node_y = node[3]
            vpcma_graph.add_node(node_num)
            vpcma_graph.add_node_attribute(node_num,(node_x,node_y))

    with open(map_file, 'r') as f1:
        for row1 in f1:
            node = row1.split()
            edges = []
            for i, word in enumerate(node):
                if i == 0:
                    node_id = int(word)

                elif i == 1:
                    node_delay = delay_dict[word]

                elif i != 2 and i != 3:
                    if word != "%":
                        node_dest = int(word)
                        edges.append((int(node_id),node_dest))
                    
            print(node_id,node_delay,edges)
            for edge in edges:
                vpcma_graph.add_edge(edge)
                vpcma_graph.set_edge_weight(edge,node_delay)

def critical(graph):
    crit_path = pygraphcp(graph)
    crit_value = path_value_eval(graph,crit_path)
    # print(crit_path,crit_value)
    return crit_path,crit_value

def path_value_eval(weighted_tasks_graph, path):
    import decimal
    decimal.getcontext().prec = 5
    value = 0
    for i in range(len(path)-1):
        value += decimal.Decimal(weighted_tasks_graph.edge_weight((path[i],path[i+1])))
    return float(value)

def pipeline(graph,pr_pos):
    if len(pr_pos) > 8:
        print("Error: The length of pr_pos is too large")
        
    sub_graphs = []
    remain_graph = copy.deepcopy(graph)

    for pos in pr_pos:
        tmp_graph = copy.deepcopy(remain_graph)
        for edge in tmp_graph.edges():
            edge_src = edge[0]
            edge_dst = edge[1]
            src_node_y = int(tmp_graph.node_attributes(edge_src)[0][1])
            if src_node_y > pos:
                tmp_graph.del_edge(edge)

        sub_graphs.append(tmp_graph)
        for previous_edge in tmp_graph.edges():
            remain_graph.del_edge(previous_edge)

    sub_graphs.append(remain_graph)                    
    return sub_graphs
    
def opt_pipeline(graph,num_pr):
    possibility_pr_pos = [0,1,2,3,4,5,6]
    com_pr_pos = list(itertools.combinations(possibility_pr_pos,num_pr))
    max_delays = []
    for pr_pos in com_pr_pos:
        sub_graphs = pipeline(graph,pr_pos)
        delays = []
        for sub_graph in sub_graphs:
            crit_path = pygraphcp(sub_graph)
            crit_value = path_value_eval(sub_graph,crit_path)
            delays.append(crit_value)
        max_delays.append(max(delays))
    optimal_pr_pos = com_pr_pos[max_delays.index(min(max_delays))]
    optimal_sub_graphs = pipeline(graph,optimal_pr_pos)

    return optimal_pr_pos,optimal_sub_graphs,min(max_delays)

def optimize(graph):
    opt_pr_pos_s = []
    opt_sub_graphs_s = []
    min_max_delay_s = []
    for num_pr in range(8):
        print(num_pr)
        tmp_opt_pr_pos,tmp_opt_sub_graphs,tmp_min_max_delay = opt_pipeline(graph,num_pr)
        opt_pr_pos_s.append(tmp_opt_pr_pos)
        opt_sub_graphs_s.append(tmp_opt_sub_graphs)
        min_max_delay_s.append(tmp_min_max_delay)
    opt_pr_pos = opt_pr_pos_s[min_max_delay_s.index(min(min_max_delay_s))]
    opt_sub_graphs = opt_sub_graphs_s[min_max_delay_s.index(min(min_max_delay_s))]
    min_max_delay = min(min_max_delay_s)
    return opt_pr_pos,opt_sub_graphs,min_max_delay
    
def test():
    vpcma_graph.add_nodes(list(range(24)))
    vpcma_graph.add_edge((0,1))
    vpcma_graph.set_edge_weight((0,1),4.812)
    vpcma_graph.add_edge((0,5))
    vpcma_graph.set_edge_weight((0,5),4.812)
    vpcma_graph.add_edge((1,8))
    vpcma_graph.set_edge_weight((1,8),4.812)
    vpcma_graph.add_edge((2,3))
    vpcma_graph.set_edge_weight((2,3),4.812)
    vpcma_graph.add_edge((2,7))
    vpcma_graph.set_edge_weight((2,7),4.812)
    vpcma_graph.add_edge((3,10))
    vpcma_graph.set_edge_weight((3,10),4.812)
    vpcma_graph.add_edge((4,12))
    vpcma_graph.set_edge_weight((4,12),2.970)
    vpcma_graph.add_edge((5,9))
    vpcma_graph.set_edge_weight((5,9),2.970)
    vpcma_graph.add_edge((6,14))
    vpcma_graph.set_edge_weight((6,14),2.970)
    vpcma_graph.add_edge((7,11))
    vpcma_graph.set_edge_weight((7,11),2.970)
    vpcma_graph.add_edge((8,13))
    vpcma_graph.set_edge_weight((8,13),14.464)
    vpcma_graph.add_edge((9,15))
    vpcma_graph.set_edge_weight((9,15),14.464)
    vpcma_graph.add_edge((10,13))
    vpcma_graph.set_edge_weight((10,13),14.464)
    vpcma_graph.add_edge((11,15))
    vpcma_graph.set_edge_weight((11,15),14.464)
    vpcma_graph.add_edge((12,16))
    vpcma_graph.set_edge_weight((12,16),14.464)
    vpcma_graph.add_edge((13,17))
    vpcma_graph.set_edge_weight((13,17),11.110)
    vpcma_graph.add_edge((14,16))
    vpcma_graph.set_edge_weight((14,16),14.464)
    vpcma_graph.add_edge((15,18))
    vpcma_graph.set_edge_weight((15,18),11.110)
    vpcma_graph.add_edge((16,19))
    vpcma_graph.set_edge_weight((16,19),11.110)
    vpcma_graph.add_edge((17,20))
    vpcma_graph.set_edge_weight((17,20),4.812)
    vpcma_graph.add_edge((18,21))
    vpcma_graph.set_edge_weight((18,21),4.812)
    vpcma_graph.add_edge((19,23))
    vpcma_graph.set_edge_weight((19,23),4.812)
    vpcma_graph.add_edge((20,22))
    vpcma_graph.set_edge_weight((20,22),3.972)
    vpcma_graph.add_edge((21,22))
    vpcma_graph.set_edge_weight((21,22),3.972)
    vpcma_graph.add_edge((22,23))
    vpcma_graph.set_edge_weight((22,23),2.783)
    crit_path = pygraphcp(vpcma_graph)
    crit_value = path_value_eval(vpcma_graph,crit_path)
    print(crit_path)
    print(crit_value)
