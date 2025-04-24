import json
import copy
import time
import sys
M = 5
start  = time.perf_counter()


def sanitize_string(s):
    # Translate non-ASCII character codes.
    s = s.strip().encode('ascii', errors='ignore').decode()
    if s.endswith('/32'):
        s = s.replace('/32','')
        split_path = re.split('/|\.|,',s)
        split_path = [item for item in filter(lambda x:x != '',split_path)]
        # print(split_path)
        return split_path
    # Lower-case the string & strip non-alpha.
    for i in s:
        if i in string.punctuation:
            s = s.replace(i," ")

    split_path = s.lower().split()
    # split_path = [item for item in filter(lambda x:x != '',split_path)]
    newline = []
    for item in split_path:
        # print(item)
        if len(item) < 2 or item.isdigit():
            continue
        if len(item) <= 5 and len(item) >= 2:
            newline.append(item)
        else:
            # print(item)
            try:
                if not nonsense(item):
                    newline.append(item)
                else:
                # print(item)
                    newline.append('hash')
            except Exception as e:
                print(s)
    split_path = [item for item in filter(lambda x:x != '',newline)]
    return split_path


f1 = open('./benign_tag/' + sys.argv[1] + '_tag.json', 'w')
with open(sys.argv[1], 'r') as f:
    line = 0
    max_score = 0
    specialnum = 0
    more20num = 0
    more17num = 0
    for s in f.readlines():
        s = json.loads(s)
        line += 1

        f2 = open('./tech_dic.txt', 'r', encoding='utf-8')
        tech_dic = eval(f2.readline())
        #print(type(tech_dic))
        f2.close()
        top5 = []
        for i in range(0, M):
            top5.append([0, 0])
        for k in tech_dic.keys():
            temp = 0
            for j in tech_dic[k]:
                for keyy in s.keys():
                    if keyy == 'is_warn':
                        s[keyy] = 'false'
                    if j in s[keyy].lower():
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
    print("time for ", line, " lines is ", (end - start))
    print("line_num= ", line)
    print("max_score= ", max_score)
    print("special_num= ", specialnum)
f1.close()
