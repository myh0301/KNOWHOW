from subject_verb_object_extract import findSVOs, nlp
from nltk.stem.wordnet import WordNetLemmatizer

total = 0
total_s = 0
total_s_use = 0
total_use = 0
total_tech = 0
f1 = open('./technique_result1019.txt','r')
f2 = open('./result_contain_use.txt','w')
for i in range(0,552):
    num = f1.readline().split()[0]
    #f2.write(num+'\n')
    f1.readline()
    sentens = f1.readline().split('.')
    for j in sentens:
        if j == '\n':
            sentens.remove(j)
        elif j == ' ':
            sentens.remove(j)
#    print(sentens)
    contain = 0
    for j in sentens:
        flag = 0
        #f2.write(j+'\n')
        token = nlp(j)
        svos = findSVOs(token)
        for k in svos:
            word = WordNetLemmatizer().lemmatize(k[1],'v')
            if word == 'use':
                flag = 1
                contain = 1
                break;
        if flag == 1:
            f2.write(j+'\n')
            total_s_use += 1
            for k in svos:
                word = WordNetLemmatizer().lemmatize(k[1],'v')
                if word == 'use':
                    total_use += 1
                if len(k) == 2:
                    f2.write('('+str(k[0])+', '+str(word)+')'+'*')
                else:
                    f2.write('('+str(k[0])+', '+str(word)+', '+str(k[2])+')'+'*')
                total += 1 
        if flag == 1:
            f2.write('\n')
    if contain == 1:
        total_s += len(sentens)
        total_tech += 1
        f2.write(num+'\n')    
        f2.write('\n')
f1.close()
print(total)
print(total_s)
print(total_s_use)
print(total_use)
print(total_tech)
f2.close()
