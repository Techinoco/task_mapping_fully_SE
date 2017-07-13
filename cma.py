import copy
from pygraph.classes.digraph import digraph

def generate_cma_graph(n, m):
    cma_graph = digraph()

    # PE nodes (ALU + SE)
    for i in range(n):
        for j in range(m):
            str_coord = str(j) + '_' + str(i)
            SE_name = 'SE' + str_coord
            ALU_name = 'ALU' + str_coord
            cma_graph.add_node(SE_name)
            cma_graph.add_node(ALU_name)
            cma_graph.add_node_attribute(SE_name, ('position',(i,j)))
            cma_graph.add_node_attribute(ALU_name, ('position',(i,j)))

    # Edges
    for i in range(n):
        for j in range(m):

            SE_cur, SE_N, SE_NE, SE_E, SE_S, SE_W, SE_NW, ALU_cur, ALU_N, ALU_NE, ALU_E, ALU_S, ALU_W, ALU_NW = neighbour_coord(j,i)

            # PE_SW
            if i == 0 and j == 0:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)

            # First line
            elif i == 0 and 0 < j < m-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)

            # PE_SE
            elif i == 0 and j == m-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)

            # First column
            elif j == 0 and 0 < i < n-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)

            # PE_NW
            elif j == 0 and i == n-1:
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)

            # Last row
            elif i == n-1 and 0 < j < m-1:
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)

            # PE_NE
            elif j == m-1 and i == n-1:
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)

            # Last column
            elif j == m-1 and 0 < i < n-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)

            # Others
            else:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)

    SE_graph = copy.deepcopy(cma_graph)
    ALU_graph = copy.deepcopy(cma_graph)
    for edge in SE_graph.edges():
        if ('ALU' in edge[0] and 'ALU' in edge[1]) or ('REG_IN' in edge[0] and 'ALU' in edge[1]):
            SE_graph.del_edge(edge)

    for node in ALU_graph.nodes():
        if 'SE' in node:
            ALU_graph.del_node(node)

    return cma_graph, SE_graph, ALU_graph

def generate_cma_reg_graph(n, m):
    cma_graph = digraph()

    # PE nodes (ALU + SE)
    for i in range(n):
        for j in range(m):
            str_coord = str(j) + '_' + str(i)
            SE_name = 'SE' + str_coord
            ALU_name = 'ALU' + str_coord
            cma_graph.add_node(SE_name)
            cma_graph.add_node(ALU_name)
            cma_graph.add_node_attribute(SE_name, ('position',(i,j)))
            cma_graph.add_node_attribute(ALU_name, ('position',(i,j)))
            if 'REG_IN_' + str(j) not in cma_graph:
                cma_graph.add_node('REG_IN_' + str(j))
        CA_name = 'C_' + str(i) + 'A'
        CB_name = 'C_' + str(i) + 'B'
        cma_graph.add_node(CA_name)
        cma_graph.add_node(CB_name)

    # Edges
    for i in range(n):
        for j in range(m):

            SE_cur, SE_N, SE_NE, SE_E, SE_S, SE_W, SE_NW, ALU_cur, ALU_N, ALU_NE, ALU_E, ALU_S, ALU_W, ALU_NW = neighbour_coord(j,i)

            CA = 'C_' + str(i) + 'A'
            CB = 'C_' + str(i) + 'B'
            cma_graph.add_edge((CA,ALU_cur), wt = 1)
            cma_graph.add_edge((CB,ALU_cur), wt = 1)
            cma_graph.add_edge((CA,SE_cur), wt = 1)

            # PE_SW
            if i == 0 and j == 0:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_N), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NE), wt = 1)
                # REG_IN
                cma_graph.add_edge(('REG_IN_' + str(j),ALU_cur), wt = 1)
                cma_graph.add_edge(('REG_IN_' + str(j),SE_cur), wt = 1)

            # First line
            elif i == 0 and 0 < j < m-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_N), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NW), wt = 1)
                # REG_IN
                cma_graph.add_edge(('REG_IN_' + str(j),ALU_cur), wt = 1)
                cma_graph.add_edge(('REG_IN_' + str(j),SE_cur), wt = 1)

            # PE_SE
            elif i == 0 and j == m-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_N), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NW), wt = 1)
                # REG_IN
                cma_graph.add_edge(('REG_IN_' + str(j),ALU_cur), wt = 1)
                cma_graph.add_edge(('REG_IN_' + str(j),SE_cur), wt = 1)

            # First column
            elif j == 0 and 0 < i < n-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_N), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NE), wt = 1)

            # PE_NW
            elif j == 0 and i == n-1:
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)

            # Last row
            elif i == n-1 and 0 < j < m-1:
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)

            # PE_NE
            elif j == m-1 and i == n-1:
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)

            # Last column
            elif j == m-1 and 0 < i < n-1:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_N), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NW), wt = 1)

            # Others
            else:
                cma_graph.add_edge((SE_cur,SE_N), wt = 1)
                cma_graph.add_edge((SE_cur,SE_E), wt = 1)
                # cma_graph.add_edge((SE_cur,SE_S), wt = 1)
                cma_graph.add_edge((SE_cur,SE_W), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_N), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_E), wt = 1)
                cma_graph.add_edge((SE_cur,ALU_W), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_cur), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_N), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,ALU_NW), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_N), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NE), wt = 1)
                cma_graph.add_edge((ALU_cur,SE_NW), wt = 1)

    SE_graph = copy.deepcopy(cma_graph)
    ALU_graph = copy.deepcopy(cma_graph)
    for edge in SE_graph.edges():
        if 'ALU' in edge[0] and 'ALU' in edge[1]:
            SE_graph.del_edge(edge)

    for node in ALU_graph.nodes():
        if 'SE' in node:
            ALU_graph.del_node(node)

    return cma_graph, SE_graph, ALU_graph

def neighbour_coord(j,i):
    cur_coord = str(j) + '_' + str(i)
    N_coord = str(j) + '_' + str(i+1)
    NE_coord = str(j+1) + '_' + str(i+1)
    E_coord = str(j+1) + '_' + str(i)
    S_coord = str(j) + '_' + str(i-1)
    W_coord = str(j-1) + '_' + str(i)
    NW_coord = str(j-1) + '_' + str(i+1)
    SE_cur = 'SE' + cur_coord
    SE_N = 'SE' + N_coord
    SE_NE = 'SE' + NE_coord
    SE_E = 'SE' + E_coord
    SE_S = 'SE' + S_coord
    SE_W = 'SE' + W_coord
    SE_NW = 'SE' + NW_coord
    ALU_cur = 'ALU' + cur_coord
    ALU_N = 'ALU' + N_coord
    ALU_NE = 'ALU' + NE_coord
    ALU_E = 'ALU' + E_coord
    ALU_S = 'ALU' + S_coord
    ALU_W = 'ALU' + W_coord
    ALU_NW = 'ALU' + NW_coord

    return SE_cur, SE_N, SE_NE, SE_E, SE_S, SE_W, SE_NW, ALU_cur, ALU_N, ALU_NE, ALU_E, ALU_S, ALU_W, ALU_NW
