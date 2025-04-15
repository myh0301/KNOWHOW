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
M = 5
start  = time.perf_counter()

with open('clustered_phrases_dbscan.json', 'r') as f:
    cluster_results = json.load(f)

model_path = './technique-embedding-128.model'
model = FastText.load(model_path)

def encode_string(model, string):
    """
    对给定的字符串进行编码，返回其词向量平均值。
    """
    words = string.split()
    vectors = [model.wv[word] for word in words if word in model.wv]
    
    if not vectors:
        return None  # 如果没有有效的词向量，返回None
    
    return np.mean(vectors, axis=0)

def find_closest_clusters(target_vector, cluster_results, top_n=3):
    similarities = []
    for label, phrases in cluster_results.items():
        for phrase_info in phrases:
            _, vector = phrase_info
            sim = cosine_similarity([target_vector], [vector])[0][0]
            similarities.append((label, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    closest_labels = list(set([label for label, _ in similarities[:top_n]]))
    
    return closest_labels

def calculate_similarities(target_vector, cluster_results, closest_labels):
    similarity_scores = {}
    
    for label in closest_labels:
        for phrase_info in cluster_results[label]:
            original_phrase, vector = phrase_info
            key = original_phrase.split('*****')[0]  # 提取key
            
            sim = cosine_similarity([target_vector], [vector])[0][0]
            
            if key not in similarity_scores:
                similarity_scores[key] = 0
            similarity_scores[key] += sim
    
    return similarity_scores


def log_svo_extract(log):
    subject1 = log['proc.name']
    object1 = log['fd.name']
    verb1 = log['evt.type']
    cmdline1 = log['proc.cmdline'] + ' ' + log['proc.pcmdline']

    if True:
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
                ip2 = "to internal network address"
            else :
                ip2 = "to external network address"
        if object1.find("->") != -1:
            ss = subject1.split(' ')[0]
            ss = ss.split('->')
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
        else:
            ssss = "None111"
            if(subject1 != None):
                if(subject1.find(".so") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/proc/filesystems") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/proc/stat") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/usr/lib/locale") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/usr/lib/x86_64-linux-gnu") != -1):
                    return ssss, ssss, ssss, ssss
            if(object1 != None):
                if(object1.find(".so") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/proc/filesystems") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/proc/stat") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/usr/lib/locale") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/usr/lib/x86_64-linux-gnu") != -1):
                    return ssss, ssss, ssss, ssss
            
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

        verb1 = verb1.replace('execve', 'execute')
        verb1 = verb1.replace('recvmsg', 'recvmsg receive message')
        verb1 = verb1.replace('recvfrom', 'recvfrom receive message')
        verb1 = verb1.replace('sendmsg', 'sendmsg send message')
        verb1 = verb1.replace('sendto', 'sendto send message')
        verb1 = verb1.replace('rmdir', 'rmdir remove directory')
        verb1 = verb1.replace('chmod ', 'chmod modify file permission ')

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
        return subject1, verb1, object1, cmdline1

def log_svo_extract_nostril(log):
    subject1 = sanitize_string(log['proc.name'])
    object1 = sanitize_string(log['fd.name'])
    verb1 = sanitize_string(log['evt.type'])
    cmdline1 = sanitize_string(log['proc.cmdline'] + ' ' + log['proc.pcmdline'])

    if True:
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
                ip2 = " to internal network address"
            else :
                ip2 = " to external network address"
            subject1 = ip1 + ip2
        if object1.find("->") != -1:
            ss = subject1.split(' ')[0]
            ss = ss.split('->')
            ip1 = str(ss[0])
            ip2 = str(ss[1])
            if ip1.startswith('10.') or ip1.startswith('192.168') or ip1.startswith('172.16'):
                ip1 = "internal network address"
            else :
                ip1 = "external network address"
            if ip2.startswith('10.') or ip2.startswith('192.168') or ip2.startswith('172.16'):
                ip2 = " to internal network address"
            else :
                ip2 = " to external network address"
            object1 = ip1 + ip2
        else:
            ssss = "None111"
            if(subject1 != None):
                if(subject1.find(".so") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/proc/filesystems") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/proc/stat") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/usr/lib/locale") != -1):
                    return ssss, ssss, ssss, ssss
                elif(subject1.find("/usr/lib/x86_64-linux-gnu") != -1):
                    return ssss, ssss, ssss, ssss
            if(object1 != None):
                if(object1.find(".so") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/proc/filesystems") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/proc/stat") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/usr/lib/locale") != -1):
                    return ssss, ssss, ssss, ssss
                elif(object1.find("/usr/lib/x86_64-linux-gnu") != -1):
                    return ssss, ssss, ssss, ssss
            
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

        verb1 = verb1.replace('execve', 'execute')
        verb1 = verb1.replace('recvmsg', 'recvmsg receive message')
        verb1 = verb1.replace('recvfrom', 'recvfrom receive message')
        verb1 = verb1.replace('sendmsg', 'sendmsg send message')
        verb1 = verb1.replace('sendto', 'sendto send message')
        verb1 = verb1.replace('rmdir', 'rmdir remove directory')
        verb1 = verb1.replace('chmod ', 'chmod modify file permission ')

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
    split_path = [item for item in filter(lambda x:x != '',newline)]
    return split_path



def process_log(s, nostril=False):
    if nostril:
        sub, verb, obj, cmd = log_svo_extract_nostril(s)
    else:
        sub, verb, obj, cmd = log_svo_extract(s)
    if sub == "None111":
        s["tech_num"] = 'None'
        s['tech_score'] = '0'
        s["anomaly_socre"] = '0'
        return s
    sub_emb = encode_string(model, sub)
    verb_emb = encode_string(model, verb)
    obj_emb = encode_string(model, obj)
    cmd_emb = encode_string(model, cmd)

    sub_closest_labels = find_closest_clusters(sub_emb, cluster_results, topn=3)
    sub_similarity_scores = calculate_similarities(sub_emb, cluster_results, sub_closest_labels)
    verb_closest_labels = find_closest_clusters(verb_emb, cluster_results, topn=3)
    verb_similarity_scores = calculate_similarities(verb_emb, cluster_results, verb_closest_labels)
    obj_closest_labels = find_closest_clusters(obj_emb, cluster_results, topn=3)
    obj_similarity_scores = calculate_similarities(obj_emb, cluster_results, obj_closest_labels)
    cmd_closest_labels = find_closest_clusters(cmd_emb, cluster_results, topn=3)
    cmd_similarity_scores = calculate_similarities(cmd_emb, cluster_results, cmd_closest_labels)

    total_similarity_scores = {}

    for key, score in sub_similarity_scores.items():
        if key not in total_similarity_scores:
            total_similarity_scores[key] = 0
        total_similarity_scores[key] += score
        
    for key, score in verb_similarity_scores.items():
        if key not in total_similarity_scores:
            total_similarity_scores[key] = 0
        total_similarity_scores[key] += score

    for key, score in obj_similarity_scores.items():
        if key not in total_similarity_scores:
            total_similarity_scores[key] = 0
        total_similarity_scores[key] += score

    for key, score in cmd_similarity_scores.items():
        if key not in total_similarity_scores:
            total_similarity_scores[key] = 0
        total_similarity_scores[key] += score
    sorted_scores = sorted(total_similarity_scores.items(), key=lambda item: item[1], reverse=True)[:top_keys]
    ll, ss = '', '', ''

    # 格式化输出
    for i in range(len(sorted_scores)):
        if sorted_scores[i][1] != 0:
            ll += (str(sorted_scores[i][0]) + ' ')  # 技术标签
            ss += (str(sorted_scores[i][1]) + ' ')  # 相似度得分
    s["tech_num"] = ll[:-1]
    s['tech_score'] = ss[:-1]  # 移除最后一个多余的空格
    if sorted_scores:
        s["anomaly_score"] = sorted_scores[0][1]
    else:
        s["anomaly_score"] = 0
    
    return s

filen = sys.argv[1]
nostril = sys.argv[2]

f1 = open('./benign_tag/' +sys.argv[1] + '_tag.json', 'w')

with open(sys.argv[1], 'r') as f:
    line = 0
    max_score = 0
    specialnum = 0
    more20num = 0
    more17num = 0
    for s in f.readlines():
        s = json.loads(s)
        
        line += 1
        
        if nostril:
            sub, verb, obj, cmd = log_svo_extract_nostril(s)
        else:
            sub, verb, obj, cmd = log_svo_extract(s)
        if sub == "None111":
            s["tech_num"] = 'None'
            s['tech_score'] = '0'
            s["anomaly_socre"] = '0'
            continue
        sub_emb = encode_string(model, sub)
        verb_emb = encode_string(model, verb)
        obj_emb = encode_string(model, obj)
        cmd_emb = encode_string(model, cmd)

        sub_closest_labels = find_closest_clusters(sub_emb, cluster_results, topn=3)
        sub_similarity_scores = calculate_similarities(sub_emb, cluster_results, sub_closest_labels)
        verb_closest_labels = find_closest_clusters(verb_emb, cluster_results, topn=3)
        verb_similarity_scores = calculate_similarities(verb_emb, cluster_results, verb_closest_labels)
        obj_closest_labels = find_closest_clusters(obj_emb, cluster_results, topn=3)
        obj_similarity_scores = calculate_similarities(obj_emb, cluster_results, obj_closest_labels)
        cmd_closest_labels = find_closest_clusters(cmd_emb, cluster_results, topn=3)
        cmd_similarity_scores = calculate_similarities(cmd_emb, cluster_results, cmd_closest_labels)

        total_similarity_scores = {}

        for key, score in sub_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score
        
        for key, score in verb_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score

        for key, score in obj_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score

        for key, score in cmd_similarity_scores.items():
            if key not in total_similarity_scores:
                total_similarity_scores[key] = 0
            total_similarity_scores[key] += score
        sorted_scores = sorted(total_similarity_scores.items(), key=lambda item: item[1], reverse=True)[:top_keys]
        ll, ss = '', '', ''

        # 格式化输出
        for i in range(len(sorted_scores)):
            if sorted_scores[i][1] != 0:
                ll += (str(sorted_scores[i][0]) + ' ')  # 技术标签
                ss += (str(sorted_scores[i][1]) + ' ')  # 相似度得分
        s["tech_num"] = ll[:-1]
        s['tech_score'] = ss[:-1]  # 移除最后一个多余的空格
        if sorted_scores:
            s["anomaly_score"] = sorted_scores[0][1]
        else:
            s["anomaly_score"] = 0

        json.dump(s, f1)
        f1.write("\n")


    print("line_num= ", line)
    print("max_score= ", max_score)
    print("special_num= ", specialnum)
    f1.close()


'''
        top5 = []
        for i in range(0, M):
            top5.append([0, 0, 0])
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
                    top5[i][2] = 1
                elif ('T1020' in top5[i][0] or 'T1030' in top5[i][0] or 'T1048' in top5[i][0] or 'T1041' in top5[i][0]
                      or 'T1011' in top5[i][0] or 'T1052' in top5[i][0] or 'T1567' in top5[i][0] or
                      'T1029' in top5[i][0] or 'T1537' in top5[i][0] or 'T1531' in top5[i][0] or 'T1485' in top5[i][0]
                      or 'T1486' in top5[i][0] or 'T1565' in top5[i][0] or 'T1491' in top5[i][0] or 'T1561' in top5[i][
                          0]
                      or 'T1499' in top5[i][0] or 'T1495' in top5[i][0] or 'T1490' in top5[i][0] or 'T1498' in top5[i][
                          0]
                      or 'T1496' in top5[i][0] or 'T1489' in top5[i][0] or 'T1529' in top5[i][0]):
                    score += m
                    top5[i][2] = m
                    special = 1
                else:
                    score += n
                    top5[i][2] = n
        ll = ''
        mm = ''
        ss = ''
        for i in range(0, 5):
            if (top5[i][1] != 0):
                ll += (str(top5[i][0]) + ' ')
                mm += (str(top5[i][1]) + ' ')
                ss += (str(top5[i][2]) + ' ')
        s["tech_num"] = ll[0:-1]
        s['tech_match_time'] = mm[0:-1]
        s['tech_score'] = ss[0:-1]
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
                #elif(s["proc.cmdline"] == "sed -n s/^cpu\\s//p /proc/stat"):
        #    json.dump(s, f1)
        #    f1.write("\n")
    end = time.perf_counter()
'''
        