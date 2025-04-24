import json
import copy
import time
import fasttext
import networkx as nx

M = 5

#filename = './all_description_new.txt'
#model = fasttext.train_unsupervised(filename, 'skipgram', dim=150, epoch=10, thread=10, lr=0.1)

g = nx.DiGraph(nx.nx_pydot.read_dot('./dot/whole_graph_new_new_new_new0.dot'))

print(g.number_of_nodes())
print(g.number_of_edges())
l = []
for n in g.nodes():
    if len(str(n)) > 5:
        if g.nodes[n]['stage'] == 'null':
            l.append(n)

for i in l:
    g.remove_node(i)

print(g.number_of_nodes())
print(g.number_of_edges())

num = 0
for sub in nx.weakly_connected_components(g):
    if (len(sub) < 5):
        continue
    sub = g.subgraph(sub).copy()

    print(len(sub.nodes))
    print(len(sub.edges))
    nx.drawing.nx_agraph.write_dot(sub, './chain' + str(num) + '.dot')
    num += 1

nx.drawing.nx_agraph.write_dot(g, './chain.dot')
