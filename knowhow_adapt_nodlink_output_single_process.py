import json
import json
import copy
import time
import string
import re
import sys
#from nostril import nonsense
import numpy as np
from numpy import tile
import math
from tqdm import tqdm
from gensim.models import FastText
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import *
from sklearn.metrics.pairwise import *
#from parse_technique_result import sanitize_string
import re, json, sys
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool
import networkx as nx
M = 5
start  = time.perf_counter()
check_nnn = 0

with open('clustered_phrases_dbscan.json', 'r') as f:
    cluster_results = json.load(f)

with open('dbscan_cluster_key_vectors.json', 'r') as fkey:
    cluster_key_vectors = json.load(fkey)


model_path = './technique-embedding-128.model'
model = FastText.load(model_path)




def encode_string(model, string):

    words = string.split()
    vectors = [model.wv[word] for word in words if word in model.wv]
    
    if not vectors:
        return None  # 如果没有有效的词向量，返回None
    
    return np.mean(vectors, axis=0)

def find_closest_clusters(target_vector, cluster_results, top_n=5):
    similarities = []
    for label, info in cluster_results.items():
        center_vector = np.array(info['center'])
        sim = cosine_similarity([target_vector], [center_vector])[0][0]
        similarities.append((label, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    closest_labels = [label for label, _ in similarities[:top_n]]
    return closest_labels

def calculate_similarities(target_vector, cluster_key_vectors, closest_labels):
    similarity_scores = {}
    
    for label in closest_labels:
        key_vectors = cluster_key_vectors.get(str(label), {})
        for key, avg_vector in key_vectors.items():
            sim = cosine_similarity([target_vector], [avg_vector])[0][0]
            
            if key not in similarity_scores:
                similarity_scores[key] = 0
            similarity_scores[key] += sim
    
    return similarity_scores

def log_svo_extract(log):
    subject1 = log[2]
    object1 = log[4]
    verb1 = log[3]
    cmdline1 = log[5]
    ssss = "None111"
    if subject1.find("->") != -1:
        ss = subject1.split(' ')[0]
        ss = ss.split('->')
        if len(ss) >= 2:
            ip1 = str(ss[0])
            ip2 = str(ss[1])
            if ip1.startswith('10.') or ip1.startswith('192.168') or ip1.startswith('172.16'):
                ip1 = "internal network address"
            else :
                ip1 = "external network address"
            if ip2.startswith('10.') or ip2.startswith('192.168') or ip2.startswith('172.16'):
                ip2 = "to internal network address"
            else :
                ip2 = "to external network address"
            subject1 = ip1 + ' ' + ip2
    elif(subject1.find(".so") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/proc/filesystems") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/proc/stat") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/usr/lib/locale") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/usr/lib/x86_64-linux-gnu") != -1):
        return ssss, ssss, ssss, ssss
    else:
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
        subject1 = subject1.replace('reg ', 'reg registry')
        subject1 = subject1.replace('pkill ', 'pkill stop process ')
        subject1 = subject1.replace('kill ', 'kill stop process ')
        subject1 = subject1.replace('ls ', 'ls list ')
        subject1 = subject1.replace('dir ', 'dir list ')
        subject1 = subject1.replace('mv ', 'mv move ')
        subject1 = subject1.replace('del ', 'del delete ')
        subject1 = subject1.replace('schtask ', 'schtask schdule task ')
        subject1 = subject1.replace('grep ', 'grep search ')
        subject1 = subject1.replace('find ', 'find search ')
        subject1 = subject1.replace('chmod ', 'chmod modify file permission ')
        subject1 = subject1.replace('chown ', 'chown modify file permission ')
        subject1 = subject1.replace('execve ', 'execve execute')
        subject1 = subject1.replace('recvmsg ', 'recvmsg receive message ')
        subject1 = subject1.replace('recvfrom ', 'recvfrom receive message ')
        subject1 = subject1.replace('sendmsg ', 'sendmsg send message ')
        subject1 = subject1.replace('tar ', 'tar compress ')
        subject1 = subject1.replace('zip ', 'zip compress ')
    
    if object1.find("->") != -1:
        ss = subject1.split(' ')[0]
        ss = ss.split('->')
        if len(ss) >= 2:
            ip1 = str(ss[0])
            ip2 = str(ss[1])
            if ip1.startswith('10.') or ip1.startswith('192.168') or ip1.startswith('172.16'):
                ip1 = "internal network address"
            else :
                ip1 = "external network address"
            if ip2.startswith('10.') or ip2.startswith('192.168') or ip2.startswith('172.16'):
                ip2 = "to internal network address"
            else :
                ip2 = "to external network address"
            object1 = ip1 + ' ' + ip2
    elif(object1.find(".so") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/proc/filesystems") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/proc/stat") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/usr/lib/locale") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/usr/lib/x86_64-linux-gnu") != -1):
        return ssss, ssss, ssss, ssss
    '''   
    else:
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
        object1 = object1.replace('reg ', 'reg registry')
        object1 = object1.replace('pkill ', 'pkill stop process ')
        object1 = object1.replace('kill ', 'kill stop process ')
        object1 = object1.replace('ls ', 'ls list ')
        object1 = object1.replace('dir ', 'dir list ')
        object1 = object1.replace('mv ', 'mv move ')
        object1 = object1.replace('rm ', 'rm delete ')
        object1 = object1.replace('del ', 'del delete ')
        object1 = object1.replace('schtask ', 'schtask schdule task ')
        object1 = object1.replace('grep ', 'grep search ')
        object1 = object1.replace('find ', 'find search ')
        object1 = object1.replace('chmod ', 'chmod modify file permission ')
        object1 = object1.replace('chown ', 'chown modify file permission ')
        object1 = object1.replace('tar ', 'tar compress ')
        object1 = object1.replace('zip ', 'zip compress ')
    '''
    verb1 = verb1.replace('execve', 'execute')
    verb1 = verb1.replace('recvmsg', 'recvmsg receive message')
    verb1 = verb1.replace('recvfrom', 'recvfrom receive message')
    verb1 = verb1.replace('sendmsg', 'sendmsg send message')
    verb1 = verb1.replace('sendto', 'sendto send message')
    verb1 = verb1.replace('rmdir', 'rmdir remove directory')
    verb1 = verb1.replace('chmod ', 'chmod modify file permission ')   
    '''
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
    cmdline1 = cmdline1.replace('reg ', 'reg registry')
    cmdline1 = cmdline1.replace('pkill ', 'pkill stop process ')
    cmdline1 = cmdline1.replace('kill ', 'kill stop process ')
    cmdline1 = cmdline1.replace('ls ', 'ls list ')
    cmdline1 = cmdline1.replace('dir ', 'dir list ')
    cmdline1 = cmdline1.replace('mv ', 'mv move ')
    cmdline1 = cmdline1.replace('rm ', 'rm delete ')
    cmdline1 = cmdline1.replace('del ', 'del delete ')
    cmdline1 = cmdline1.replace('schtask ', 'schtask schdule task ')
    cmdline1 = cmdline1.replace('grep ', 'grep search ')
    cmdline1 = cmdline1.replace('find ', 'find search ')
    cmdline1 = cmdline1.replace('chmod ', 'chmod modify file permission ')
    cmdline1 = cmdline1.replace('chown ', 'chown modify file permission ')
    cmdline1 = cmdline1.replace('execve ', 'execute ')
    cmdline1 = cmdline1.replace('recvmsg ', 'recvmsg receive message ')
    cmdline1 = cmdline1.replace('recvfrom ', 'recvfrom receive message ')
    cmdline1 = cmdline1.replace('sendmsg ', 'sendmsg send message ')
    cmdline1 = cmdline1.replace('sendto ', 'sendto send message ')
    cmdline1 = cmdline1.replace('tar ', 'tar compress ')
    cmdline1 = cmdline1.replace('zip ', 'zip compress ')
    '''
    subject1 = re.sub(r'[^A-Za-z0-9 ]+', ' ', subject1) 
    verb1 = re.sub(r'[^A-Za-z0-9 ]+', ' ', verb1) 
    object1 = re.sub(r'[^A-Za-z0-9 ]+', ' ', object1) 
    cmdline1 = re.sub(r'[^A-Za-z0-9 ]+', ' ', cmdline1) 
    return subject1, verb1, object1, cmdline1

def log_svo_extract_nostril(log):
    subject1 = log[2]
    object1 = log[4]
    verb1 = log[3]
    cmdline1 = log[5]
    ssss = "None111"
    if subject1.find("->") != -1:
        ss = subject1.split(' ')[0]
        ss = ss.split('->')
        if len(ss) >= 2:
            ip1 = str(ss[0])
            ip2 = str(ss[1])
            if ip1.startswith('10.') or ip1.startswith('192.168') or ip1.startswith('172.16'):
                ip1 = "internal network address"
            else :
                ip1 = "external network address"
            if ip2.startswith('10.') or ip2.startswith('192.168') or ip2.startswith('172.16'):
                ip2 = "to internal network address"
            else :
                ip2 = "to external network address"
            subject1 = ip1 + ' ' + ip2
    elif(subject1.find(".so") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/proc/filesystems") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/proc/stat") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/usr/lib/locale") != -1):
        return ssss, ssss, ssss, ssss
    elif(subject1.find("/usr/lib/x86_64-linux-gnu") != -1):
        return ssss, ssss, ssss, ssss
    else:
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
        subject1 = subject1.replace('reg ', 'reg registry')
        subject1 = subject1.replace('pkill ', 'pkill stop process ')
        subject1 = subject1.replace('kill ', 'kill stop process ')
        subject1 = subject1.replace('ls ', 'ls list ')
        subject1 = subject1.replace('dir ', 'dir list ')
        subject1 = subject1.replace('mv ', 'mv move ')
        subject1 = subject1.replace('del ', 'del delete ')
        subject1 = subject1.replace('schtask ', 'schtask schdule task ')
        subject1 = subject1.replace('grep ', 'grep search ')
        subject1 = subject1.replace('find ', 'find search ')
        subject1 = subject1.replace('chmod ', 'chmod modify file permission ')
        subject1 = subject1.replace('chown ', 'chown modify file permission ')
        subject1 = subject1.replace('execve ', 'execve execute')
        subject1 = subject1.replace('recvmsg ', 'recvmsg receive message ')
        subject1 = subject1.replace('recvfrom ', 'recvfrom receive message ')
        subject1 = subject1.replace('sendmsg ', 'sendmsg send message ')
        subject1 = subject1.replace('tar ', 'tar compress ')
        subject1 = subject1.replace('zip ', 'zip compress ')
    
    if object1.find("->") != -1:
        ss = subject1.split(' ')[0]
        ss = ss.split('->')
        if len(ss) >= 2:
            ip1 = str(ss[0])
            ip2 = str(ss[1])
            if ip1.startswith('10.') or ip1.startswith('192.168') or ip1.startswith('172.16'):
                ip1 = "internal network address"
            else :
                ip1 = "external network address"
            if ip2.startswith('10.') or ip2.startswith('192.168') or ip2.startswith('172.16'):
                ip2 = "to internal network address"
            else :
                ip2 = "to external network address"
            object1 = ip1 + ' ' + ip2
    elif(object1.find(".so") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/proc/filesystems") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/proc/stat") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/usr/lib/locale") != -1):
        return ssss, ssss, ssss, ssss
    elif(object1.find("/usr/lib/x86_64-linux-gnu") != -1):
        return ssss, ssss, ssss, ssss
    '''   
    else:
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
        object1 = object1.replace('reg ', 'reg registry')
        object1 = object1.replace('pkill ', 'pkill stop process ')
        object1 = object1.replace('kill ', 'kill stop process ')
        object1 = object1.replace('ls ', 'ls list ')
        object1 = object1.replace('dir ', 'dir list ')
        object1 = object1.replace('mv ', 'mv move ')
        object1 = object1.replace('rm ', 'rm delete ')
        object1 = object1.replace('del ', 'del delete ')
        object1 = object1.replace('schtask ', 'schtask schdule task ')
        object1 = object1.replace('grep ', 'grep search ')
        object1 = object1.replace('find ', 'find search ')
        object1 = object1.replace('chmod ', 'chmod modify file permission ')
        object1 = object1.replace('chown ', 'chown modify file permission ')
        object1 = object1.replace('tar ', 'tar compress ')
        object1 = object1.replace('zip ', 'zip compress ')
    '''
    verb1 = verb1.replace('execve', 'execute')
    verb1 = verb1.replace('recvmsg', 'recvmsg receive message')
    verb1 = verb1.replace('recvfrom', 'recvfrom receive message')
    verb1 = verb1.replace('sendmsg', 'sendmsg send message')
    verb1 = verb1.replace('sendto', 'sendto send message')
    verb1 = verb1.replace('rmdir', 'rmdir remove directory')
    verb1 = verb1.replace('chmod ', 'chmod modify file permission ')
    subject1 = sanitize_string(subject1)
    object1 = sanitize_string(object1)

    cmdline1 = sanitize_string(cmdline1)      
    '''
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
    cmdline1 = cmdline1.replace('reg ', 'reg registry')
    cmdline1 = cmdline1.replace('pkill ', 'pkill stop process ')
    cmdline1 = cmdline1.replace('kill ', 'kill stop process ')
    cmdline1 = cmdline1.replace('ls ', 'ls list ')
    cmdline1 = cmdline1.replace('dir ', 'dir list ')
    cmdline1 = cmdline1.replace('mv ', 'mv move ')
    cmdline1 = cmdline1.replace('rm ', 'rm delete ')
    cmdline1 = cmdline1.replace('del ', 'del delete ')
    cmdline1 = cmdline1.replace('schtask ', 'schtask schdule task ')
    cmdline1 = cmdline1.replace('grep ', 'grep search ')
    cmdline1 = cmdline1.replace('find ', 'find search ')
    cmdline1 = cmdline1.replace('chmod ', 'chmod modify file permission ')
    cmdline1 = cmdline1.replace('chown ', 'chown modify file permission ')
    cmdline1 = cmdline1.replace('execve ', 'execute ')
    cmdline1 = cmdline1.replace('recvmsg ', 'recvmsg receive message ')
    cmdline1 = cmdline1.replace('recvfrom ', 'recvfrom receive message ')
    cmdline1 = cmdline1.replace('sendmsg ', 'sendmsg send message ')
    cmdline1 = cmdline1.replace('sendto ', 'sendto send message ')
    cmdline1 = cmdline1.replace('tar ', 'tar compress ')
    cmdline1 = cmdline1.replace('zip ', 'zip compress ')
    '''
    return subject1, verb1, object1, cmdline1


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
                          
    #split_path = [item for item in filter(lambda x:x != '',newline)]
    #return split_path
    sss = ''
    for item in filter(lambda x:x != '',newline):
        sss += str(item) + ' '
    return sss[:-1]

def process_log(s, nostril=False, top_keys=3):
    if int(nostril):
        sub, verb, obj, cmd = log_svo_extract_nostril(s)
    else:
        sub, verb, obj, cmd = log_svo_extract(s)
    if sub == "None111":
        g[s[0]][s[1]]["tech_num"] = 'None'
        s[s[0]][s[1]]['tech_score'] = '0'
        g[s[0]][s[1]]["anomaly_socre"] = '0'
        return 

    total_similarity_scores = {}
    if sub != "":
        sub_emb = encode_string(model, sub)
        sub_closest_labels = find_closest_clusters(sub_emb, cluster_results, top_n=5)
        sub_similarity_scores = calculate_similarities(sub_emb, cluster_key_vectors, sub_closest_labels)
        for key, score in sub_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score
    if verb != "":
        verb_emb = encode_string(model, verb)
        verb_closest_labels = find_closest_clusters(verb_emb, cluster_results, top_n=5)
        verb_similarity_scores = calculate_similarities(verb_emb, cluster_key_vectors, verb_closest_labels)
        for key, score in verb_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score
    if obj != "":
        obj_emb = encode_string(model, obj)
        obj_closest_labels = find_closest_clusters(obj_emb, cluster_results, top_n=5)
        obj_similarity_scores = calculate_similarities(obj_emb, cluster_key_vectors, obj_closest_labels)
        for key, score in obj_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score
    if cmd != "":
        cmd_emb = encode_string(model, cmd)
        cmd_closest_labels = find_closest_clusters(cmd_emb, cluster_results, top_n=5)
        cmd_similarity_scores = calculate_similarities(cmd_emb, cluster_key_vectors, cmd_closest_labels)
        for key, score in cmd_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score

    #print('22222')

    sorted_scores = sorted(total_similarity_scores.items(), key=lambda item: item[1], reverse=True)[:min(top_keys, len(total_similarity_scores.keys()))]
    print("44444")
    ll, ss = '', ''

    for i in range(len(sorted_scores)):
        if sorted_scores[i][1] != 0:
            ll += (str(sorted_scores[i][0]) + ' ') 
            ss += (str(sorted_scores[i][1]) + ' ') 
    g[s[0]][s[1]]["tech_num"] = ll[:-1]
    g[s[0]][s[1]]['tech_score'] = ss[:-1] 
    if sorted_scores:
        g[s[0]][s[1]]["anomaly_socre"] = sorted_scores[0][1]
    else:
        g[s[0]][s[1]]["anomaly_socre"] = 0
    print("55555")
    return

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


filen = sys.argv[1]
nostril = sys.argv[2]
g = nx.DiGraph(nx.nx_pydot.read_dot(filen))
if True:
    logs = [(g[e[0]], g[e[1]], g[e[0]]['label'], g[e[0]][e[1]]['syscall'] ,g[e[1]]['label'], g[e[0]][e[1]]['cmd']) for e in g.edges()]
    for log in logs:
        process_log(log, nostril, 3)
    #pool = Pool(processes=30) 
    #results = pool.starmap(process_log, [(log, nostril, 3) for log in logs])
    #pool.close()
    #pool.join()
        
    #for s in results:
    #    json.dump(s, f1)
    #    f1.write("\n")

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

nx.drawing.nx_agraph.write_dot(g, './lifecycle_'+filen.split('0')[0].split('/')[-1]+'.dot')
