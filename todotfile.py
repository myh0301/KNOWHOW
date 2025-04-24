import networkx as nx
import difflib as df
import sys

ffff1 = sys.argv[1]
f1 = open(str(ffff1), 'r')


f1.readline()
node = eval(f1.readline())
edge = eval(f1.readline())
g1 = nx.DiGraph()
for i in node:
    s1 = i[1]['label'].replace('\"', '')
    g1.add_node(i[0], label = s1)
for i in edge:
    l = is_warn = i[2]['tech_num'] + ' ** ' + str(i[2]['anomaly_socre']) + ' ** ' + i[2]['sys_type']
    g1.add_edge(i[0], i[1], label= l , e_id=i[2]['e_id'], is_warn=i[2]['is_warn'], sys_type=i[2]['sys_type'],
                   proc_name=i[2]['proc_name'], tech_num=i[2]['tech_num'],
                   anomaly_socre=i[2]['anomaly_socre'])
a = []


for nod in list(g1.nodes()):
    if(len(a) == 0):
        a.append(str(g1.nodes[nod]['label']))
    else:
        flag = 0
        for tmp in a:
            cc = df.SequenceMatcher(None, str(tmp), str(g1.nodes[nod]['label'])).quick_ratio()
            if cc > 0.95:
                print('kkk')
                flag = 1
                break;
        if flag == 0:
            a.append(str(g1.nodes[nod]['label']))
        else:
            print('qqq')
            g1.remove_node(nod)

num = 1
for sub in nx.weakly_connected_components(g1):
    if (len(sub) < 10):
        continue
    sub = g1.subgraph(sub)
    print(len(sub.nodes))
    print(len(sub.edges))
    for k in sub.nodes():
        sub.nodes[k]['label'] = sub.nodes[k]['label'].replace(':',' ')

    nx.drawing.nx_pydot.write_dot(sub, 'whole_graph_new_'+ str(ffff1).split('.')[0] + str(num) + '.dot')
    num += 1
#nx.drawing.nx_agraph.write_dot(g1, 'whole_graph_new' + '.dot')
#dot -T svg ./whole_graph_new1.dot -o ./whole_graph_new1.svg
