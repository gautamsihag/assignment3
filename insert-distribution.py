# Taking a pipe from stdin, in which every message is a JSON
# corresponding to a meetup reservation. It extracts the state name
# and puts that into a Redis database (running on the default port) as the
# value of an entry. (The key is a randomly generated unique identifier.)
#
# Entries Expiration set to 15 minutes because there is tendency that at certain moment of time
# a minute-to-minute updation may cause erroneous data to
# get a good sense of the distribution, Fifteen minutes allows us to observe some
# variation and avoiding random noise.
import redis
from sys import stdin
from uuid import uuid1
import json
# Establish a Redis connection on the default port: with db index 1. 
# allowing to separate the distribution database from the database
# containing time diffs which is used to calculate the rate
conn = redis.Redis(db=1)
# To hold the categories previuosly seen
# That's important so that we can put one entry in the DB that will never erase

seen = set([])

while True:
    # Read the JSON string from stdin, and load it into a Python dictionary.
    line = stdin.readline()
    dic = json.loads(line)
    # Grab the type of the change.
    change = dic.get('group_state')
    if change not in seen:
        # If fresh category: add an entry in Redis so as to give it a non-zero probability of happening,
        # Also, add it to our set of seen categories so we don't add another permanent entry.
        seen.add(change)
        conn.set(str(uuid1()),change)
        # Adding article name to db along with a unique identifier key. Set
        # the expiration time to 15 minutes from discussion above
    else:
        conn.setex(str(uuid1()),change,900)
