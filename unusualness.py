# accepting a stream of meetup reservation from meet2.py (over stdin)
# and checks the probability of the probability of the
# property the system is keeping track of against the distribution in the Redis database. If
# it is below a threshold, a message is sent via stdout about
# the unusual message. They are then read by pushwithslack.py and sent to
# the notification system.

# A message whose probability is less than 15%, as judged by the entries in the
# Redis database, is considered unlikely. Chosing the value: because of the p-values. This 
# notifies us any time an reservation event is made for a location that represents less
# than 5% of the stream.


from sys import stdin,stdout
import json
import util

threshold = 15
while True:
    # The meet2.py data stream from input from stdin is input from line and
    # decoding JSON.
    line = stdin.readline()
    dic = json.loads(line)
    # Extracting the 'group_state' key, which is a unique identifier for the
    # reservation message.
    message = dic.get('group_state')
    # The util.py function gets the probability of a
    # specific message, given the entries in the Redis database.
    prob = util.probability(message)
    # when the probability is less than threshold, emit a message. Otherwise,
    # loop around.
    if prob < threshold:
        # This schema is taken care of by the puchwithslack.py file, which sends the sutiable notification.
        # Printing the notification to stdout and flush stdout to prevent message delay
        # from buffering.
        print ({'type':'unusualness','message':message,'prob':prob})
        stdout.flush()
