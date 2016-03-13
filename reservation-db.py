# using the functions from util.py to
# calculate entropy and rate based on the state of the Redis db. It takes no
# input, and emits a JSON string with the entropy and rate to stdout. These
# messages are monitored by check-detect.py to, find outliers.
import json
from sys import stdout
from time import sleep
import util
#Repeat the entropy and rate calculation
while True:
    # using the util function to calculate entropy and rate
    entropy = util.entropy()
    rate = util.rate()
    # the entropy and the rate over to stdout
    print (json.dumps({'entropy':entropy,'rate':rate}))
    stdout.flush()
    # sleep for a second: to ensure to get a smoother function for the entropy values and rate.
    sleep(1)
