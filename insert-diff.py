# This script takes the Unix-piped stream from diff.py (which are time deltas)
# between events in the stream and adds it to redis with a unique identifier.
#
# Although works on its wn, the idea is based on:
# https://github.com/mikedewar/RealTimeStorytelling/blob/master/2/insert.py

from sys import stdin, stdout
from uuid import uuid1
import json
import redis
# Connect to the diff redis db
conn = redis.Redis(db=0)
while True:
    # This is the piped time deltas from diff.py
    d = stdin.readline()
    l = json.loads(d)
    # The time diff is in the key 'delta'
    diff = l.get('delta')
    # 'expiration' time assists in adding smoothness to the function smooth function that still has variability.
    # Add it to the database; have it expire after 120 seconds (2 mins).
    conn.setex(str(uuid1()),diff,120)
    print(json.dumps({'delta':diff}))
    stdout.flush()
