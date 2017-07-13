from pygraph.classes.digraph import digraph
from pygraph.algorithms.heuristics.chow import chow
from pygraph.algorithms.heuristics.euclidean import euclidean
from pygraph.algorithms.minmax import *
from moga_taskmapping_v2 import *

g = digraph()
g.add_nodes(['ALU0','SE0','ALU1','SE1'])
g.add_node_attribute('ALU0', ('position',(0,0)))
g.add_node_attribute('SE0', ('position',(0,0)))
g.add_node_attribute('ALU1', ('position',(1,0)))
g.add_node_attribute('SE1', ('position',(1,0)))
g.add_edge(('ALU0','SE0'), wt=1)
g.add_edge(('SE0','SE1'), wt=1)
g.add_edge(('SE1','SE0'), wt=1)
g.add_edge(('SE0','ALU1'), wt=1)
g.add_edge(('ALU1','SE1'), wt=1)
h = euclidean()
h.optimize(g)
path = heuristic_search(g,'ALU0', 'ALU1', h)
print(path)
path_evaluation(g,path)
