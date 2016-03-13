# Following is a script containing functions that interact with the Redis
# database. They are used by several different components of this system. Note
# that they return Python objects, not JSON dumps, so that they can be used or
# repackaged by other Python programs as needed.




import redis
from collections import Counter
from math import log
# Establishing the connection to the Redis table containing time differences which is used for
# rate calculations
rate_conn = redis.Redis(db =0)
# Establish the connection to the Redis table containing the distribution.
dist_conn = redis.redis(db =1)
# This function generates a hostogram as a json.
def histogram():
	# Get the keys
	keys = dist_conn.keys()
	#using them to get the reservation schedules
	articles = dist_conn.mget(keys)
	# Repeat these two steps until there are no None articles which appear when:
	# an entry expired bween the time: 
	#when the list of keys was collected 
	#and the time they were pulled from the db. 
	while not all(articles):
		keys = dist_conn.keys()
		articles = dist_conn.mget(keys)
	# dictionary counter for counts for each entry (reservation message).
	counts = Counter(articles)
	# The number of messages is the denomentator for the proportion
	total = len(articles)
	# Using a dictionary to obtain a dictionary of the items and their proportions in the total population.
	hist = {article:count/float(total) for article,count in counts.items()}
	return hist
#function to define the rate of the reservation
def rate():
	# getting the keys and use the keys to get the diffs.
	keys = rate_conn.keys()
	diffs = rate_conn.mget(keys)
	# repeat these two steps until there are no Nones. Nones suggest that the collection of diffs has changed between getting
    	# keys and retrieving entries, which means the results would be out of date.
    	# Note, this would not work if it returned the actual integers because 0
    	# evaluates to False.
	while not all (diffs):
		keys = rate_conn.keys()
		diffs = rate_conn.mget(keys)
	# Converting numbers from strings to floats, because it will make the division below later, 
	# and it is also generalized, but for this data set everything in the DB is actually an
    	# integer.

	diffs = [float(diff) for diff in diffs]
	# Now we just average all of the diffs in the database.
	avg = sum(diffs)/len(diffs)

# function to calculate: entropy of the categorical distribution in the
# Redis db.
def entropy():
	# first calculate the histogram
	hist = histogram()
	# Entropy calculation: list comprehension goes through each entry and calculate p*log(p). 
	# Then sum those, and then negate the result.
	entropy = -sum([p*log(p) for p in hist.values()])
	return entropy
# To calculate the probability of a particular message appearing in the stream, based on the categorical distribution in the redis
# database
def probability(title):
	# getting the histogram
	hist = histogram()
	# the entry is the probability. 
	# The calculation: 
	# for histogram entries: 
	# the number of that message that has appeared, divided
    	# by the total number of messages. Here note that the
    	# have to return 0 (no probability) if that message
    	# has not been observed before.
	prob = hist.get(title,0)
	return prob
