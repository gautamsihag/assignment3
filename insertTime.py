import json
import sys
import redis

#inserts the time differe between signups to redis (keeps for 60 s)
#code borrowed from instructor's github


#opens connection to redis server
conn = redis.Redis()

#runs forever
while 1:
    #reads the input from command line (assuming piped input)
    line = sys.stdin.readline()
    
    #creates json object
    d = json.loads(line)

    #extracts timestamp and time difference from json object
    delta = d["delta"]
    time = d["t"]

    #insert timestamp and time difference as key value in redis to be stored for 60 seconds
    conn.setex(time, delta, 60)

    #also print the key and value on screen for debugging
    print json.dumps({"time":time, "delta":delta})
    sys.stdout.flush()
