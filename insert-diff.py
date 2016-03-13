from sys import stdin, stdout
from uuid import uuid1
import json
import redis

conn = redis.Redis(db=0)
while True:
    d = stdin.readline()
    l = json.loads(d)
    diff = l.get('delta')
    conn.setex(str(uuid1()),diff,120)
    print(json.dumps({'delta':diff}))
    stdout.flush()