import sys
import json
filen = sys.argv[1]
score_bar = float(sys.argv[2])
proc_name = set()
cmd = set()
with open(str(filen), 'r') as f:
    lines = f.readlines()
    for line in lines:
        s = json.loads(line)
        score = float(s['anomaly_socre'])
        if score + 0.00001  > score_bar:
            proc_name.add(s['proc.pid'] + ' ' + s['proc.name'])
            cmd.add(s['proc.cmdline'])
    print(proc_name)
    print(cmd)
