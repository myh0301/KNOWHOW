import sys
import json
filen = sys.argv[1]
score_cal = {}
with open(str(filen), 'r') as f:
    lines = f.readlines()
    for line in lines:
        s = json.loads(line)
        score = s['anomaly_socre']
        if score in score_cal.keys():
            score_cal[score] += 1
        else:
            score_cal[score] = 1
    print(score_cal)
