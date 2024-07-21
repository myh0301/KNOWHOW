import json
import copy
import time
import fasttext
import numpy as np
M = 5
#f1 = open("./0509111.json", 'w')
#with open('./anomaly.json', 'r') as f:   
#f1 = open('./0509222.json', 'w')
#with open('./0509111.json', 'r') as f:
start  = time.perf_counter()

#读入数据集
f1 = open('./dataset.json', 'w')

#embedding模型训练，利用未标注cti文本
filename = './all_description_new.txt'
model = fasttext.train_unsupervised(filename, 'skipgram', dim=150, epoch=10, thread=10, lr=0.1)



with open('./anomaly.json', 'r') as f:
    line = 0
    max_score = 0
    specialnum = 0
    more20num = 0
    more17num = 0
    for s in f.readlines():
        s = json.loads(s)
        line += 1
        if(s["fd.name"] != None):
            if(s["fd.name"].find(".so") != -1):
                line = line - 1
                continue
            elif(s["fd.name"].find("/proc/filesystems") != -1):
                line = line - 1
                continue
            elif(s["fd.name"].find("/proc/stat") != -1):
                line = line - 1
                continue
            elif(s["fd.name"].find("/usr/lib/locale") != -1):
                line = line - 1
                continue
            elif(s["fd.name"].find("/usr/lib/x86_64-linux-gnu") != -1):
                line = line - 1
                continue
        #if(s["evt.args"].find("-n.s/^cpu\\s//p./proc/stat.") != -1):
        s["proc.name"] = s["proc.name"].replace('\n', '')
        s["proc.name"] = s["proc.name"].replace('\\', '++')
        s["proc.name"] = s["proc.name"].replace('\\', '++')
        s["proc.name"] = s["proc.name"].replace('$', '_')

        f2 = open('./tech_dic.txt', 'r', encoding='utf-8')
        tech_dic1 = eval(f2.readline())
        tech_dic = {}
        for key in tech_dic1.keys():
            tech_dic[key] = []
            for item in tech_dic1[key]:
                item0 = item.split()
                tem = model.get_word_vector(item0[0])
                for i in range(1,len(item0)):
                     tmp = tmp + model.get_word_vector(item0[i])
                tmp = tmp / len(item0)
                tech_dic[key].append(tmp)
        f3 = open('./ioc.txt', 'r', encoding='utf-8')
        ioc_text = eval(f3.readline())
        #print(type(tech_dic))
        f2.close()
        top5 = []
        for i in range(0, M):
            top5.append([0, 0])
        
                

        
        for k in tech_dic.keys():
            temp = 0
            for j in tech_dic[k]:
                type1 = model.get_word_vector(s["evt.type"].lower())
                sc = np.dot(j,type1)/(np.linalg.norm(j)*np.linalg.norm(type1)) 
                if sc > 0.8:
                    temp = temp + sc
                type1 = model.get_word_vector(s["fd.name"])
                sc = np.dot(j,type1)/(np.linalg.norm(j)*np.linalg.norm(type1)) 
                if sc > 0.8:
                    temp = temp + sc
                type1 = model.get_word_vector(s["proc.cmdline"])
                sc = np.dot(j,type1)/(np.linalg.norm(j)*np.linalg.norm(type1)) 
                if sc > 0.8:
                    temp = temp + sc
                type1 = model.get_word_vector(s["proc.name"])
                sc = np.dot(j,type1)/(np.linalg.norm(j)*np.linalg.norm(type1)) 
                if sc > 0.8:
                    temp = temp + sc
            for j in ioc_text[k]:
                if j in s["evt.type"].lower():
                    temp += 1
                if s["fd.name"] != None:
                    if j in s["fd.name"].lower():
                        temp += 1
                if s["proc.cmdline"] != None:
                    if j in s["proc.cmdline"].lower():
                        temp += 1
                if s["proc.name"] != None:
                    if j in s["proc.name"].lower():
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
        ll = ''
        for i in range(0, 5):
            if (top5[i][1] != 0):
                ll += (top5[i][0] + ' ')
        s["tech_num"] = ll
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
                elif ('T1020' in top5[i][0] or 'T1030' in top5[i][0] or 'T1048' in top5[i][0] or 'T1041' in top5[i][0]
                      or 'T1011' in top5[i][0] or 'T1052' in top5[i][0] or 'T1567' in top5[i][0] or
                      'T1029' in top5[i][0] or 'T1537' in top5[i][0] or 'T1531' in top5[i][0] or 'T1485' in top5[i][0]
                      or 'T1486' in top5[i][0] or 'T1565' in top5[i][0] or 'T1491' in top5[i][0] or 'T1561' in top5[i][
                          0]
                      or 'T1499' in top5[i][0] or 'T1495' in top5[i][0] or 'T1490' in top5[i][0] or 'T1498' in top5[i][
                          0]
                      or 'T1496' in top5[i][0] or 'T1489' in top5[i][0] or 'T1529' in top5[i][0]):
                    score += m
                    special = 1
                else:
                    score += n
        if (nums != 0):
            score = round((float(score) / float(nums)), 2)
        s["anomaly_socre"] = str(score)
        if score > max_score:
            max_score = score
        if score > 2:
            more20num += 1
        if score > 1.7:
            more17num += 1
        if special == 1:
            specialnum += 1
        for i in range(1, 13):
            if i * 1000000 == line:
                end = time.perf_counter()
                print("time for ", i * 1000000, " lines is ", (end - start))
        json.dump(s, f1)
        f1.write("\n")
        #elif(s["proc.cmdline"] == "sed -n s/^cpu\\s//p /proc/stat"):
        #    json.dump(s, f1)
        #    f1.write("\n")
    end = time.perf_counter()
 #   print("time for ", line, " lines is ", (end - start))
 #   print("line_num= ", line)
 #   print("max_score= ", max_score)
 #   print("special_num= ", specialnum)
f1.close()


