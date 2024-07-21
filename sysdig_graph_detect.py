import networkx as nx
from config import *
from hashlib import md5
import csv
import string
import re
import pandas as pd
import json 
#from nostril import nonsense
import copy
f6 = open('./path_0320.txt', 'w')


def graph_init():
    G = nx.DiGraph()
    return G

def get_md5(s):
    return str(md5(s.encode('utf8')).hexdigest())

def read_org_log_from_json(file_path):
    syslog = pd.read_json(file_path, orient = 'columns', lines = True)
    print("complete loads", file_path)
    syslog = syslog.drop_duplicates()
    print("\ncomplete drop duplicates from syslog\n")
    syslog = syslog.fillna("None")
    print("complete fill miss parts as None\n")
    return syslog


def graph_add_node_realapt(g:nx.DiGraph, logs, key, md5_to_node:dict):
    node_set = set()
    edge_set = set()
    if key == APTLOG_KEY.FILE:
        for index, row in logs.iterrows():
            s_node = get_md5(row['proc.cmdline'])
            fd_name_tmp = row['fd.name']
            p1 = fd_name_tmp.find('(')
            p2 = fd_name_tmp.find(')')
            fd_name_tmp = fd_name_tmp[(p1+1):p2]
            t_node = get_md5(fd_name_tmp)
            if s_node not in md5_to_node:
                md5_to_node[s_node] = row['proc.cmdline']
            if t_node not in md5_to_node:
                md5_to_node[t_node] = row['fd.name']
            e_id = row['evt.num']
            is_warn = row['is_warn']
            sys_type = row['evt.type']
            proc_name = row['proc.name']
            tech_num = row['tech_num']
            anomaly_socre = row['anomaly_socre']
            node_set.add(s_node)
            node_set.add(t_node)
            edge_set.add((s_node, t_node, e_id, is_warn, sys_type, proc_name, tech_num, anomaly_socre))
    elif key == APTLOG_KEY.PROCESS:
        for index, row in logs.iterrows():
            s_node = get_md5(row['proc.pcmdline'])
            t_node = get_md5(row['proc.cmdline'])
            if s_node not in md5_to_node:
                md5_to_node[s_node] = row['proc.pcmdline']
            if t_node not in md5_to_node:
                md5_to_node[t_node] = row['proc.cmdline']
            e_id = row['evt.num']
            is_warn = row['is_warn']
            sys_type = row['evt.type']
            proc_name = row['proc.name']
            tech_num = row['tech_num']
            anomaly_socre = row['anomaly_socre']
            node_set.add(s_node)
            node_set.add(t_node)
            edge_set.add((s_node, t_node, e_id, is_warn, sys_type, proc_name, tech_num, anomaly_socre))
    elif key == APTLOG_KEY.NET:
            for index, row in logs.iterrows():
                s_node = get_md5(row['proc.cmdline'])
                t_node = get_md5(row['fd.name'])
                if s_node not in md5_to_node:
                    md5_to_node[s_node] = row['proc.cmdline']
                if t_node not in md5_to_node:
                    md5_to_node[t_node] = row['fd.name']
                e_id = row['evt.num']
                is_warn = row['is_warn']
                sys_type = row['evt.type']
                proc_name = row['proc.name']
                tech_num = row['tech_num']
                anomaly_socre = row['anomaly_socre']
                node_set.add(s_node)
                node_set.add(t_node)
                edge_set.add((s_node, t_node, e_id, is_warn, sys_type, proc_name, tech_num, anomaly_socre))
    '''
    elif key == APTLOG_KEY.EXECVE:
            for index, row in logs.iterrows():
                s_node = get_md5(row['proc.cmdline'])
                t_node = get_md5((row['evt.args']).strip('filename='))
                if s_node not in md5_to_node:
                    md5_to_node[s_node] = row['proc.cmdline']
                if t_node not in md5_to_node:
                    md5_to_node[t_node] = (row['evt.args']).strip('filename=')
                e_id = row['evt.num']
                is_warn = row['is_warn']
                proc_name = row['proc.name']
                tech_num = row['tech_num']
                anomaly_socre = row['anomaly_socre']
                node_set.add(s_node)
                node_set.add(t_node)
                edge_set.add((s_node, t_node, e_id, is_warn, sys_type, proc_name, tech_num, anomaly_socre))
    '''
    node_list = list(node_set)
    node_list.sort()
    for node in node_list:
        g.add_node(node)
        g.nodes[node]['label'] = md5_to_node[node]
    
    edge_list = list(edge_set)
    edge_list.sort()
    for edge in edge_list:
        g.add_edge(edge[0], edge[1], e_id = edge[2], is_warn = edge[3], sys_type = edge[4], proc_name = edge[5], tech_num = edge[6], anomaly_socre = edge[7])
    
    return g

def provenance_graph_realapt(org_log, md5_to_node:dict):
    file_op_logs = org_log[org_log['evt.type'].isin(APTLOG_TYPE.FILE_OP)]
    print("file log count: ", len(file_op_logs))
    process_op_logs = org_log[org_log['evt.type'].isin(APTLOG_TYPE.PROCESS_OP)]
    print("process log count: ", len(process_op_logs))
    net_op_logs = org_log[org_log['evt.type'].isin(APTLOG_TYPE.NET_OP)]
    print("net log count: ", len(net_op_logs))
    #execve_op_logs = org_log[org_log['evt.type'].isin(APTLOG_TYPE.XECVE_OP)]
    #print ('execve log count: ', len(execve_op_logs))

    if len(file_op_logs) > 0:
        file_op_logs = file_op_logs[APTLOG_ARTRIBUTE.FILE_ARTRIBUTE]
    if len(process_op_logs) > 0:
        process_op_logs = process_op_logs[APTLOG_ARTRIBUTE.PROCESS_ARTRIBUTE]
    if len(net_op_logs) > 0:
        net_op_logs = net_op_logs[APTLOG_ARTRIBUTE.NET_ARTRIBUTE]
    #if len(execve_op_logs) > 0:
    #    execve_op_logs = execve_op_logs[APT_LOG_ARTRIBUTE.EXECVE_ARTRIBUTE]

    G = graph_init()
    G = graph_add_node_realapt(G, file_op_logs, APTLOG_KEY.FILE, md5_to_node)
    G = graph_add_node_realapt(G, process_op_logs, APTLOG_KEY.PROCESS, md5_to_node)
    G = graph_add_node_realapt(G, net_op_logs, APTLOG_KEY.NET, md5_to_node)
    #G = graph_add_node_realapt(G, execve_op_logs, APTLOG_KEY.EXECVE, md5_to_node)
    return G

'''
def directed_acyclic_graph(graph = ''):
    if nx.is_directed_acyclic_graph(graph) == True:
        print("completed, DAG is true\n")
    else:
        print("found cycles in graph\n")
        while nx.is_directed_acyclic_graph(graph) == False:
            edge_list = list(nx.find_cycle(graph, orientation = 'original'))
            graph.remove_edges_from(edge_list)
        print("completed, DAG is true\n")
    weight = nx.pagerank(graph, alpha = 1)
    for e in graph.edges():
        graph[e[0]][e[1]]['weight'] = weight[e[0]]
    return graph
'''


def backtrack(node, g:nx.DiGraph, store:nx.DiGraph, s1:str):
    if list(g.predecessors(node)):
            for n in g.predecessors(node):
                store.add_node(n, label=copy.deepcopy(g.nodes[n]['label']))
                store.add_edge(n, node, e_id=g[n][node]['e_id'], is_warn=g[n][node]['is_warn'], sys_type=g[n][node]['sys_type'], proc_name=g[n][node]['proc_name'], tech_num=g[n][node]['tech_num'], anomaly_socre=g[n][node]['anomaly_socre'])
                k = ''
                if(g.nodes[n]['label'] == None):
                    k = k + 'None'
                else:
                    k = k + copy.deepcopy(g.nodes[n]['label'])
                k = k + ' *-* '
                k = k + copy.deepcopy(g[n][node]['sys_type'])
                k = k + ' -*- '
                k = k + copy.deepcopy(g[n][node]['tech_num'])
                k = k + ' -*- '
                k = k + copy.deepcopy(str(g[n][node]['anomaly_socre']))
                k = k + ' *-* '
                k = k + copy.deepcopy(s1)
                s = copy.deepcopy(backtrack(n, g, store, copy.deepcopy(k)))
                return copy.deepcopy(s)
    elif(s1 == None):
        return 'None'
    else:
        #print(copy.deepcopy(s1))
        f6.write(copy.deepcopy(s1) + '\n')
        return copy.deepcopy(s1)

def backtrack1(node, g:nx.DiGraph, store:nx.DiGraph, s1:str):
    if list(g.predecessors(node)) :
            for n in g.predecessors(node):
                store.add_node(n, label=copy.deepcopy(g.nodes[n]['label']))
                store.add_edge(n, node, e_id=g[n][node]['e_id'], is_warn=g[n][node]['is_warn'], sys_type=g[n][node]['sys_type'], proc_name=g[n][node]['proc_name'], tech_num=g[n][node]['tech_num'], anomaly_socre=g[n][node]['anomaly_socre'])
                k = ''
                if(g.nodes[n]['label'] == None):
                    k = k + 'None'
                else:
                    k = k + copy.deepcopy(str(g.nodes[n]['label']))
                k = k + ' *-* '
                k = k + copy.deepcopy(str(g[n][node]['sys_type']))
                k = k + ' -*- '
                k = k + copy.deepcopy(g[n][node]['tech_num'])
                k = k + ' -*- '
                k = k + copy.deepcopy(str(g[n][node]['anomaly_socre']))
                k = k + ' *-* '
                k = k + copy.deepcopy(s1)
                #print('hask', k)
                s = copy.deepcopy(backtrack1(n, g, store, copy.deepcopy(k)))
                #print('hass', s)
                return copy.deepcopy(s)
    elif(s1 == None):
        #print('non None')
        return 'None'
    else:
        k = copy.deepcopy(s1)
        #print('nonk', k)
        #print(k)
        f6.write(k + '\n')
        return k

def forwardtrack(node, g:nx.DiGraph, store:nx.DiGraph):
    if list(g.successors(node)):
            for n in g.successors(node):
                store.add_node(n, label=g.nodes[n]['label'])
                store.add_edge(node, n, e_id=g[node][n]['e_id'], is_warn=g[node][n]['is_warn'], sys_type=g[node][n]['sys_type'], proc_name=g[node][n]['proc_name'], tech_num=g[n][node]['tech_num'], anomaly_socre=g[n][node]['anomaly_socre'])
                forwardtrack(n, g, store)


if __name__ == "__main__":
    log = read_org_log_from_json("./0509000_new2.json")
    g = graph_init()
    node = {}
    g = provenance_graph_realapt(log, node)
    if nx.is_directed_acyclic_graph(g) == True:
        print("DAG IS TRUE\n")
    else:
        print("FOUND CYCLE\n")
        while(nx.is_directed_acyclic_graph(g) == False):
            edge = list(nx.find_cycle(g, orientation = 'original'))
            g.remove_edges_from(edge)
        print("FINISH REMOVING, DAG IS TRUE\n")
    #print('the node num of graph is ',len(g), '\n')
    #print('whether nx is connected ', nx.is_connected(g), '\n')
    #print('the num of connected components is ', nx.number_connected_components(g), '\n')
    
    truth = []
    f1 = open("./1.5+cmdline.txt", 'r', encoding='utf-8')
    for line in f1.readlines():
        #line = line.split(',')
        #if(line[1] == '1'):
        #   truth.append(line[0])
        line = line[:-1]
        #line[0] = line[0].replace('\n', '')
        line = line.replace('++', '\\')
        line = line.replace('++', '\\')
#        line = line.replace('_', '$')
        truth.append(get_md5(line))
    f1.close()
##    f2 = open("./road2.txt", 'w')
##    f3 = open("./road_str2.txt", 'w')
    f4 = open("./not_in_graph_0320.txt", 'w')
    f5 = open("road_whole_0320.txt", 'w')
    graph_list = []
    s_list = []
    allnum = 0
    continuenum = 0
#    print(len(truth))
#    print(truth)
    k = 0
    linei = 1
    g1 = nx.DiGraph()
    for n in truth:

        allnum += 1
        if(n not in g):
            f4.write("line NO." + str(i) + ":" + str(n) + "\n")
            continuenum += 1
            continue
#        print(n)
#        print(g.nodes[n]['label'])
        if(g.nodes[n]['label'] == None):
            g1.add_node(n, label='None')
        else:
            g1.add_node(n, label=g.nodes[n]['label'])
        '''
        for suc in g.successors(n):
            g1.add_node(suc, label=g.nodes[suc]['label'])
            g1.add_edge(n, suc, e_id=g[n][suc]['e_id'], is_warn=g[n][suc]['is_warn'], sys_type=g[n][suc]['sys_type'], proc_name=g[n][suc]['proc_name'])
        '''
        if(g.nodes[n]['label'] == None):
            s1 = 'None'
        else:
            s1 = str(g.nodes[n]['label'])
        if(k == 0):
            s = copy.deepcopy(backtrack1(n, g, g1, copy.deepcopy(s1)))
        else:
            s = copy.deepcopy(backtrack(n, g, g1, copy.deepcopy(s1)))
        k = 1
#        print(s)
        '''
        forwardtrack(n, g, g1)
        for tt in g.predecessors(n):
            if list(g.successors(tt)) is not None:
                    for tmp in g.successors(tt):
                        if tmp is not n:
                            g1.add_node(tmp, label=g.nodes[tmp]['label'])
                            g1.add_edge(tt, tmp, e_id=g[tt][tmp]['e_id'], is_warn=g[tt][tmp]['is_warn'], sys_type=g[tt][tmp]['sys_type'], proc_name=g[tt][tmp]['proc_name'])
                            forwardtrack(tmp, g, g1)
        
        '''
        fflag = 0
        '''
        for i in s_list:
            if str(s) in str(i):
                fflag = 1
                break

        if(fflag == 0):
            s_list.append(str(s))
            graph_list.append(g1)
            f3.write("***")
            f3.write('\n')
            f3.write(str(s) + '\n')
            f2.write("***")
            f2.write('\n')
            f2.write(str(g1.nodes.data()))
            f2.write('\n')
            f2.write(str(g1.edges.data()))
            f2.write('\n')
        '''
    f5.write("***")
    f5.write('\n')
    f5.write(str(g1.nodes.data()))
    f5.write('\n')
    f5.write(str(g1.edges.data()))
    f5.write('\n')
    print(allnum)
    print(continuenum)
##    f2.close()
##    f3.close()
    f4.close()
    f6.close()