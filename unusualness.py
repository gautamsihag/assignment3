from sys import stdin,stdout
import json
import util

threshold = 0.05
while True:
    line = stdin.readline()
    dic = json.loads(line)
    message = dic.get('meeting')
    prob = util.probability(message)
    if prob < threshold:
        print ({'type':'unusualness','message':message,'prob':prob})
        stdout.flush()