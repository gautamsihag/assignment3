import redis
from sys import stdin
import json
from collections import Counter
import sys
import requests
from sys import stdout

#this code listens to the meetup rsvp stream and for every state that gets rsvp, it checks if the probability of rsvp is below a certain threshold (user provided or default of 0.001) then it prints that event

#connect to database containing the rsvp state distribution
conn1 = redis.Redis(db=1)

#initializes the rates threshold
probability_threshold = 0

#handles the case when rate is not provided by user. Defaults to .32 in that case
try:
    probability_threshold= float(sys.argv[1])
except:
    probability_threshold = .001


#consuming the stream from source
r = requests.get("http://stream.meetup.com/2/rsvps", stream=True)

#stays on forever unless the stream stops
for raw_rsvp in r.iter_lines():

    # loops over all the stream messages
    try:
        m = json.loads(raw_rsvp.decode('utf-8'))

        # Filtering for meetup group state
        if "group" in m:
	    #extracts state from stream
            state = m["group"]["group_state"]
            
            #calculate the distribution of states by rsvp
	    keys = conn1.keys()
            messages = conn1.mget(keys)
            messageCounts = Counter(messages)
            numMessages = len(messages)
            distribution = {message: messageCount/float(numMessages) for message, messageCount in messageCounts.items()}

            #calculates the probability of the current state from the distribution
            stateProbability = distribution.get(state,0)

            #checks if the probability is below a certain threshold then it prints that
            if stateProbability < probability_threshold:
	        print "RSVP occurred from Unlikely state: " + state + " (probability = " + str(stateProbability) + ")" 
                stdout.flush()
    # Exception handling in case the state field is empy or the encoding is different
    except:
        continue
















