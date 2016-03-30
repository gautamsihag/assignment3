import redis
from sys import stdin
import json
from uuid import uuid1
import sys

#in this piece of code we are consuming state and timestamp of rsvp and inserting the state in db1 and calculating the time diff and dumping that on standard output

#variable used to keep track of time
last = 0

#connection to db1 in redis. This is used to store the distribution data
conn1 = redis.Redis(db=1)

#initialize the set of states
states = set([])

#run forever
while 1:
    #read from piped input
    line = stdin.readline()

    #convert the input to json object
    d = json.loads(line)
    
    #extract state and time stamp from json object
    state = d["State"]
    time = d["t"]

    #add entry to the distribution db in redis. We add entries for states, if there are more than one entry for state then we set to expire after 10 min 
    if state in states:
        conn1.setex(str(uuid1()), state, 600)
    else:
        states.add(state)
        conn1.set(str(uuid1()), state)

    #calculate the time difference between rsvp
    if last == 0 :
        last = time
        continue
    delta = time - last

    #Prints the time difference
    print json.dumps({"delta":delta, "t":time})
    sys.stdout.flush()

    #updates the previous time variable
    last = time
    
