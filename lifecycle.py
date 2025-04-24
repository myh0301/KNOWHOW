import time
import networkx as nx

g = nx.DiGraph(nx.nx_pydot.read_dot('./dot/alert1.dot'))

tech2tac = {}
f2 = open('./tech2tac.txt', 'r')
for l in f2.readlines():
    l = l[:-1]
    tmp = l.split('\t')
    tech = tmp[0]
    tac = tmp[1]
    tech2tac[tech]= tac
f2.close()

tac2stage = {}
f2 = open('./tac2stage.txt', 'r')
for l in f2.readlines():
    l = l[:-1]
    tmp = l.split('...')
    tac = tmp[0]
    stage = tmp[1]
    for tacc in tac.split(', '):
        tac2stage[tacc]= stage
f2.close()

line = 0
#with open('./anomaly.json', 'r') as f:
i111 = 0

for e in g.edges():
    if True:
        ll = ''
        tac_score = {}
        stage_score = {}
        if g[e[0]][e[1]]['tech_num']!= '':
            tech_num_list  = g[e[0]][e[1]]['tech_num'].split(' ')
            tech_score_list = g[e[0]][e[1]]['tech_socre'].split(' ')
            for i in range(0, len(tech_num_list)):
                if tech_num_list[i] not in tac_score.keys():
                    tac_score[tech_num_list[i]] = tech_score_list[i]
                else:
                    tac_score[tech_num_list[i]] += tech_score_list[i]
        tac_score_sort = sorted(tac_score.items(), key = lambda x:x[1],reverse=True)
 
        if True:
            l = list(tac_score_sort)
            g[e[0]][e[1]]['tac_name'] = ''
            g[e[0]][e[1]]['tac_score'] = ''
            for i in l:
                g[e[0]][e[1]]['tac_name'] += i[0] + ' '
                g[e[0]][e[1]]['tac_score'] += str(i[1]) + ' '
                #stage_score_calculation
                stagename = tac2stage[i[0]]
                if not stagename in stage_score.keys():
                    stage_score[stagename] = float(i[1])
                else:
                    stage_score[stagename] += float(i[1])
        
        stage_score_sort = sorted(stage_score.items(), key = lambda x:x[1],reverse=True)
        if len(stage_score_sort) >4:
            l = list(stage_score_sort)
            tn0, ts0 = l[0]
            tn1, ts1 = l[1]
            tn2, ts2 = l[2]
            tn3, ts3 = l[3]
            g[e[0]][e[1]]['stage_name'] = tn0 + '***' + tn1 + '***' + tn2 + '***' + tn3 
            g[e[0]][e[1]]['stage_score'] = str(ts0) + '***' + str(ts1) + '***' + str(ts2) + '***' + str(ts3) 
        else:
            g[e[0]][e[1]]['stage_name'] = ''
            g[e[0]][e[1]]['stage_score'] = ''
            l = list(stage_score_sort)
            for i in l:
                g[e[0]][e[1]]['stage_name'] += i[0] + '***'
                g[e[0]][e[1]]['stage_score'] += str(i[1]) + '***'
            g[e[0]][e[1]]['stage_name'] += g[e[0]][e[1]]['stage_name'][:-3]
            g[e[0]][e[1]]['stage_score'] += g[e[0]][e[1]]['stage_score'][:-3]

iik = 0
for n in g.nodes():
    iik += 1
    if len(str(n)) > 5:
        g.nodes[n]['stage'] = ''
        stagedic = {}
        if iik == 16:
            print(stagedic)
        for outedge in g.out_edges(n):
            sn = g[outedge[0]][outedge[1]]['stage_name'].split('***')
            sc = g[outedge[0]][outedge[1]]['stage_score'].split('***')
            if iik == 16:
                print(n)
                print(outedge)
                print(sn)
                print(sc)
                print(g[outedge[0]][outedge[1]]['stage_name'])
                print(g[outedge[0]][outedge[1]]['stage_score'])
            
            for i in range(0, len(sn)):
                if not sn[i] in stagedic.keys():
                    stagedic[sn[i]] = float(sc[i])
                else:
                    stagedic[sn[i]] += float(sc[i])
        if iik == 16:
            print(stagedic)
        stagedic_sort = sorted(stagedic.items(), key = lambda x:x[1],reverse=True)
        if iik == 16:
            print(stagedic)
        l = list(stagedic_sort)
        if len(l) != 0:
            g.nodes[n]['stage'], g.nodes[n]['stage_score'] = l[0]
            g.nodes[n]['label'] = g.nodes[n]['stage'] + '  ***  ' + str(g.nodes[n]['stage_score']) + '  ***  ' + g.nodes[n]['label']
        else:
            g.nodes[n]['stage'], g.nodes[n]['stage_score'] = "null", 0
            g.nodes[n]['label'] = g.nodes[n]['stage'] + '  ***  ' + str(g.nodes[n]['stage_score']) + '  ***  ' + g.nodes[n]['label']
        if iik ==16 :
            print(stage_score_sort)
            print(g.nodes[n]['label'])

nx.drawing.nx_agraph.write_dot(g, './lifecycle1.dot')


