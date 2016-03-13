import redis
from sys import stdin
from uuid import uuid1
import json

conn = redis.Redis(db=1)

seen = set([])

while True:
    line = stdin.readline()
    dic = json.loads(line)
    change = dic.get('meeting')
    if change not in seen:
        seen.add(change)
        conn.set(str(uuid1()),change)
    else:
        conn.setex(str(uuid1()),change,900)