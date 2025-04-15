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
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt



def preprocess(text):
    # 去除Windows路径中的反斜杠和冒号
    text = re.sub(r'\\|:', ' ', text)
    
    # 处理可能存在的URL或文件路径，简单替换为"filepath"或"url"
    #text = re.sub(r'(http[s]?://\S+|\/\S*\.?\S*)', 'filepath', text)
    
    # 将所有斜杠（正斜杠和反斜杠）替换为空格
    text = re.sub(r'[\\/]', ' ', text)
    
    # 移除括号
    text = re.sub(r'[()$${}]', '', text)
    
    # 替换单引号和双引号为空格
    text = re.sub(r'[\'"]', ' ', text)
    
    # 移除感叹号
    text = re.sub(r'!', ' ', text)
    
    # 将多余的空格替换为单个空格，并去除首尾空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    text = text.lower()
    
    return text

def phrase_vector(model, phrase):
    words = phrase.split()
    vectors = [model.wv[word] for word in words if word in model.wv]
    
    if not vectors:
        print(phrase + "IS OOV")
        return None  
    
    return np.mean(vectors, axis=0)




if __name__ == "__main__":

    mean_shift_bool = int(sys.argv[1])
    inputfile = "./technique_text.txt"

    model_path = './technique-embedding-128.model'
    model = FastText.load(model_path)
    f = open("./tech_dic.txt", 'r')
    tech_dic = eval(f.readline())
    f.close()
    
    all_vectors = []
    labels = []
    tech_vectors ={}
    for key, phrase_list in tech_dic.items():
        tech_vectors[key] = []
        for phrase in phrase_list:
            processed_phrase = preprocess(phrase)
            vector = phrase_vector(model, processed_phrase)
            if vector is not None:  
                tech_vectors[key].append(vector.tolist())
                all_vectors.append(vector)
                labels.append(str(key)+"*****"+str(processed_phrase))

    # 将结果保存到本地文件
    with open('./tech_dic_vectors.json', 'w') as f:
        json.dump(tech_vectors, f)


    X = np.array(all_vectors)

    if mean_shift_bool == True:
    # 应用Mean Shift聚类
        bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=1000)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(X)
        labels_ms = ms.labels_
        cluster_centers = ms.cluster_centers_

        # 创建聚类结果字典
        cluster_results = {}
        cluster_results1 = {}
        for i, label in enumerate(labels_ms):
            label = int(label)
            if label not in cluster_results:
                cluster_results1[label] = {'points': [], 'center': cluster_centers[label].tolist()}
                cluster_results[label] = {'points': [], 'center': cluster_centers[label].tolist()}
            cluster_results[label]['points'].append((labels[i], X[i].tolist()))

        # 将结果保存到本地文件
        with open('./meanshift_clustered_phrases.json', 'w') as f:
            json.dump(cluster_results1, f)
        
        cluster_key_vectors = {}
        for label, info in cluster_results.items():
            key_vectors_sum = {}
            
            for original_phrase, vector in info['points']:
                key = original_phrase.split('*****')[0]
                
                if key not in key_vectors_sum:
                    key_vectors_sum[key] = np.zeros_like(vector)
                    
                key_vectors_sum[key] += np.array(vector)
            
            
            cluster_key_vectors[label] = {key: vector.tolist() for key, vector in key_vectors_sum.items()}

        # 将结果保存到本地文件
        with open('meanshift_cluster_key_vectors.json', 'w') as f:
            #json.dump({label: {key: vector.tolist() for key, vector in vectors.items()} for label, vectors in cluster_key_vectors.items()}, f)        
            json.dump(cluster_key_vectors, f)    
        
    else:
        # 应用DBSCAN聚类
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        dbscan.fit(X)
        labels_dbscan = dbscan.labels_

        # 计算每个聚类的中心向量
        unique_labels = set(labels_dbscan)
        cluster_centers = {}
        for label in unique_labels:
            if label != -1:  # 忽略噪声点（如果有的话）
                class_members = [X[i] for i in range(len(labels_dbscan)) if labels_dbscan[i] == label]
                center = np.mean(class_members, axis=0)
                cluster_centers[label] = center.tolist()

        # 创建聚类结果字典
        cluster_results = {}
        cluster_results1 = {}
        for i, label in enumerate(labels_dbscan):
            if label == -1:
                continue  # 忽略噪声点
            label = int(label)
            if label not in cluster_results:
                cluster_results1[label] = {'points': [], 'center': cluster_centers[label]}
                cluster_results[label] = {'points': [], 'center': cluster_centers[label]}
            cluster_results[label]['points'].append((labels[i], X[i].tolist()))

        # 将结果保存到本地文件
        #print(cluster_results1)
        with open('clustered_phrases_dbscan.json', 'w') as f:
            json.dump(cluster_results1, f)

        cluster_key_vectors = {}
        for label, info in cluster_results.items():
            key_vectors_sum = {}
            
            for original_phrase, vector in info['points']:
                key = original_phrase.split('*****')[0]
                
                if key not in key_vectors_sum:
                    key_vectors_sum[key] = np.zeros_like(vector)
                    
                key_vectors_sum[key] += np.array(vector)
            
            cluster_key_vectors[label] = {key: vector.tolist() for key, vector in key_vectors_sum.items()}

        # 将结果保存到本地文件
        with open('dbscan_cluster_key_vectors.json', 'w') as f:
            #json.dump({label: {key: vector.tolist() for key, vector in vectors.items()} for label, vectors in cluster_key_vectors.items()}, f)        
            json.dump(cluster_key_vectors, f)    
    
        
                

    print("Phrase vectors have been saved to 'phrase_vectors.json'")
    
    # 使用PCA降维以便于可视化
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # 可视化聚类结果
    plt.figure(figsize=(10, 7))
    unique_labels = set(labels_dbscan)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        if k == -1:
            col = 'k'  # 设置噪声点颜色为黑色

        class_member_mask = (labels_dbscan == k)
        xy = X_pca[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=6, label=f'Cluster {k}')
        
        # 添加文本标注
        for i, txt in enumerate(np.array(labels)[class_member_mask]):
            plt.annotate(txt, (xy[i, 0], xy[i, 1]), fontsize=8, alpha=0.7)

    plt.title('Estimated number of clusters: %d' % len(unique_labels))
    plt.legend()
    plt.savefig('cluster_visualization.png')



