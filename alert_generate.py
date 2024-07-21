import json
import copy
import time
import fasttext
import networkx as nx

M = 5
#f1 = open("./0509111.json", 'w')
#with open('./anomaly.json', 'r') as f:   
#f1 = open('./0509222.json', 'w')
#with open('./0509111.json', 'r') as f:
start  = time.perf_counter()

#filename = './all_description_new.txt'
#model = fasttext.train_unsupervised(filename, 'skipgram', dim=150, epoch=10, thread=10, lr=0.1)

g = nx.DiGraph(nx.nx_pydot.read_dot('./dot/whole_graph.dot'))

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
for n in g.nodes():
    #print(n)
    #print(g.nodes[n])
    if len(str(n)) > 5:
        subject1 =  g.nodes[n]['label']
        subject1 = subject1.replace('\n', '')
        subject1 = subject1.replace('\\', '++')
        subject1 = subject1.replace('\\', '++')
        subject1 = subject1.replace('$', '_')
        subject1 = subject1.replace('\"', '')
        if i111 == 0:
            i111 += 1
            #print(g.nodes[n]['label'])
            #print(subject1)
        g.nodes[n]['label'] = subject1
    #print('success')

for e in g.edges():
    subject1 = g.nodes[e[0]]['label']
    object1 = g.nodes[e[1]]['label']
    g.nodes[e[0]]['label'] = subject1
    g.nodes[e[1]]['label'] = object1
    syscall1 = g[e[0]][e[1]]['syscall']
    cmdline1 = g[e[0]][e[1]]['cmd']
    max_score = 0
    specialnum = 0
    more20num = 0
    more17num = 0
    if True:
        line += 1
        if subject1.find("->") != -1:
            ss = subject1.split(' ')[0]
            ss = ss.split('->')
            ip1 = str(ss[0])
            ip2 = str(ss[1])
            if ip1.startswith('10.') or ip1.startswith('192.168') or ip1.startswith('172.16'):
                ip1 = "internal network address"
            else :
                ip1 = "external network address"
            if ip2.startswith('10.') or ip2.startswith('192.168') or ip2.startswith('172.16'):
                ip2 = "internal network address"
            else :
                ip2 = "external network address"
        else:
            if(subject1 != None):
                if(subject1.find(".so") != -1):
                    line = line - 1
                    continue
                elif(subject1.find("/proc/filesystems") != -1):
                    line = line - 1
                    continue
                elif(subject1.find("/proc/stat") != -1):
                    line = line - 1
                    continue
                elif(subject1.find("/usr/lib/locale") != -1):
                    line = line - 1
                    continue
                elif(subject1.find("/usr/lib/x86_64-linux-gnu") != -1):
                    line = line - 1
                    continue
            if(object1 != None):
                if(object1.find(".so") != -1):
                    line = line - 1
                    continue
                elif(object1.find("/proc/filesystems") != -1):
                    line = line - 1
                    continue
                elif(object1.find("/proc/stat") != -1):
                    line = line - 1
                    continue
                elif(object1.find("/usr/lib/locale") != -1):
                    line = line - 1
                    continue
                elif(object1.find("/usr/lib/x86_64-linux-gnu") != -1):
                    line = line - 1
                    continue
            
            #if(s["evt.args"].find("-n.s/^cpu\\s//p./proc/stat.") != -1):
        subject1 = subject1.replace('\n', '')
        subject1 = subject1.replace('\\', '++')
        subject1 = subject1.replace('\\', '++')
        subject1 = subject1.replace('$', '_')
        subject1 = subject1.replace('\"', '')
        subject1 = subject1.replace('sh ', 'shell ')
        subject1 = subject1.replace('bash ', 'bash shell ')
        subject1 = subject1.replace('cp ', 'copy ')
        subject1 = subject1.replace('scp ', 'scp transfer ')
        subject1 = subject1.replace('ssh ', 'ssh transfer ')
        subject1 = subject1.replace('sftp ', 'sftp transfer ')
        subject1 = subject1.replace('tftp ', 'tftp transfer ')
        subject1 = subject1.replace('curl ', 'curl transfer ')
        subject1 = subject1.replace('sshd ', 'sshd transfer ')
        subject1 = subject1.replace('certutil ', 'certutil transfer ')
        subject1 = subject1.replace('wget ', 'wget download ')
        subject1 = subject1.replace('cat ', 'cat read ')

        object1 = object1.replace('\n', '')
        object1 = object1.replace('\\', '++')
        object1 = object1.replace('\\', '++')
        object1 = object1.replace('$', '_')
        object1 = object1.replace('\"', '')
        object1 = object1.replace('sh ', 'shell ')
        object1 = object1.replace('bash ', 'bash shell ')
        object1 = object1.replace('cp ', 'copy ')
        object1 = object1.replace('scp ', 'scp transfer ')
        object1 = object1.replace('ssh ', 'ssh transfer ')
        object1 = object1.replace('sftp ', 'sftp transfer ')
        object1 = object1.replace('tftp ', 'tftp transfer ')
        object1 = object1.replace('curl ', 'curl transfer ')
        object1 = object1.replace('sshd ', 'sshd transfer ')
        object1 = object1.replace('certutil ', 'certutil transfer ')
        object1 = object1.replace('wget ', 'wget download ')
        object1 = object1.replace('cat ', 'cat read ')
        g.nodes[e[0]]['label'] = subject1
        g.nodes[e[1]]['label'] = object1

        cmdline1 = cmdline1.replace('\n', '')
        cmdline1 = cmdline1.replace('\\', '++')
        cmdline1 = cmdline1.replace('\\', '++')
        cmdline1 = cmdline1.replace('$', '_')
        cmdline1 = cmdline1.replace('\"', '')
        cmdline1 = cmdline1.replace('sh ', 'shell ')
        cmdline1 = cmdline1.replace('bash ', 'bash shell ')
        cmdline1 = cmdline1.replace('cp ', 'copy ')
        cmdline1 = cmdline1.replace('scp ', 'scp transfer ')
        cmdline1 = cmdline1.replace('ssh ', 'ssh transfer ')
        cmdline1 = cmdline1.replace('sftp ', 'sftp transfer ')
        cmdline1 = cmdline1.replace('tftp ', 'tftp transfer ')
        cmdline1 = cmdline1.replace('curl ', 'curl transfer ')
        cmdline1 = cmdline1.replace('sshd ', 'sshd transfer ')
        cmdline1 = cmdline1.replace('certutil ', 'certutil transfer ')
        cmdline1 = cmdline1.replace('wget ', 'wget download ')
        cmdline1 = cmdline1.replace('cat ', 'cat read ')
        g[e[0]][e[1]]['cmd'] = cmdline1


        f2 = open('./database_content.txt', 'r', encoding='utf-8')
        tech_dic = eval(f2.readline())
        f2.close()
        top5 = []
        for i in range(0, M):
            top5.append([0, 0])
        for k in tech_dic.keys():
            temp = 0
            for j in tech_dic[k]:
                if j in syscall1.lower():
                    temp += 1
                if subject1!= None:
                    if j in subject1.lower():
                        temp += 1
                if cmdline1 != None:
                    if j in cmdline1.lower():
                        temp += 1
                if object1 != None:
                    if j in object1.lower():
                        temp += 1
            for i in range(0, 5):
                if temp > top5[i][1]:
                    for j in range(0, 4 - i):
                        top5[4 - j][0] = copy.deepcopy(top5[3 - j][0])
                        top5[4 - j][1] = copy.deepcopy(top5[3 - j][1])
                        # print(top5)
                    top5[i][0] = k
                    top5[i][1] = temp
                    break;
        '''
        score = 0
        m = 3
        n = 2
        nums = 0
        special = 0
        for i in range(0, 5):
            if (top5[i][1] != 0):
                nums += 1
                if ('T1189' in top5[i][0] or 'T1190' in top5[i][0] or 'T1133' in top5[i][0] or 'T1200' in top5[i][0]
                        or 'T1566' in top5[i][0] or 'T1195' in top5[i][0] or 'T1199' in top5[i][0] or
                        'T1078' in top5[i][0]):
                    score += 1
                    top5[i][1] += 1
                elif ('T1020' in top5[i][0] or 'T1030' in top5[i][0] or 'T1048' in top5[i][0] or 'T1041' in top5[i][0]
                      or 'T1011' in top5[i][0] or 'T1052' in top5[i][0] or 'T1567' in top5[i][0] or
                      'T1029' in top5[i][0] or 'T1537' in top5[i][0] or 'T1531' in top5[i][0] or 'T1485' in top5[i][0]
                      or 'T1486' in top5[i][0] or 'T1565' in top5[i][0] or 'T1491' in top5[i][0] or 'T1561' in top5[i][
                          0]
                      or 'T1499' in top5[i][0] or 'T1495' in top5[i][0] or 'T1490' in top5[i][0] or 'T1498' in top5[i][
                          0]
                      or 'T1496' in top5[i][0] or 'T1489' in top5[i][0] or 'T1529' in top5[i][0]):
                    score += m
                    top5[i][1] += m
                    special = 1
                else:
                    score += n
                    top5[i][1] += n
        if (nums != 0):
            score = round((float(score) / float(nums)), 2)
        g[e[0]][e[1]]['anomaly_socre'] = str(score)
        if score > max_score:
            max_score = score
        if score > 2:
            more20num += 1
        if score > 1.7:
            more17num += 1
        if special == 1:
            specialnum += 1
        '''
        
        
        ll = ''
        tac_score = {}
        stage_score = {}
        for i in range(0, 5):
            if (top5[i][1] != 0):
                ll += (top5[i][0] + ' ')
                #tac_score_calculation
                tac_list = tech2tac[top5[i][0]]
                for items1 in tac_list.split(', '):
                    if items1 not in tac_score.keys():
                        tac_score[items1] = top5[i][1]
                    else:
                        tac_score[items1] += top5[i][1]
                
        g[e[0]][e[1]]['tech_num'] = ll

        tac_score_sort = sorted(tac_score.items(), key = lambda x:x[1],reverse=True)
        if len(tac_score_sort) > 3:
            l = list(tac_score_sort)
            tn0, ts0 = l[0]
            tn1, ts1 = l[1]
            tn2, ts2 = l[2]
            g[e[0]][e[1]]['tac_name'] = tn0 + ' ' + tn1 + ' ' + tn2
            g[e[0]][e[1]]['tac_score'] = str(ts0) + ' ' + str(ts1) + ' ' + str(ts2)
        #stage_score_calculation
            stagename = tac2stage[tn0]
            if stagename not in stage_score.keys():
                stage_score[stagename] = float(ts0)
            else:
                stage_score[stagename] += float(ts0)
            stagename = tac2stage[tn1]
            if stagename not in stage_score.keys():
                stage_score[stagename] = float(ts1)
            else:
                stage_score[stagename] += float(ts1)
            stagename = tac2stage[tn2]
            if stagename not in stage_score.keys():
                stage_score[stagename] = float(ts2)
            else:
                stage_score[stagename] += float(ts2)
        else:
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


        #elif(s["proc.cmdline"] == "sed -n s/^cpu\\s//p /proc/stat"):
        #    json.dump(s, f1)
        #    f1.write("\n")
end = time.perf_counter()
#print("time for ", line, " lines is ", (end - start))
#print("line_num= ", line)
#print("max_score= ", max_score)
#print("special_num= ", specialnum)
nx.drawing.nx_agraph.write_dot(g, './tag1.dot')


