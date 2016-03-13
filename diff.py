# This script takes the Unix-piped stream from meet2.py. 
# it calculates the time difference between the two
# earliest timestamps, outputs the result as a JSON to stdout.
# This script is a copy of:
# https://github.com/mikedewar/RealTimeStorytelling/blob/master/2/diff.py

# When estimates of the server time elapsed between the earliest and oldest observation in the buffer exceeds
# threshold, the system then calculates the time difference between the two
# earliest timestamps, outputs the result as a JSON to stdout, and removes the
# oldest element from the array.
import sys
import json
from sys import stdin, stdout
from bisect import insort

# to hold the value of the last event
last = []
# repeat while true
while True:
    # load the JSON string, and then get the 'timestamp' key, which is a
    # Unix timestamp
    line = stdin.readline()
    d = json.loads(line)
    time = d.get('timestamp')
    # if the last doesnot have a values till now; this captures the first condition
    # one in the buffer, we didn't wait long enough, and we emitted a few
    # function to ensure that there's a limit to the delay
    # we'll accept, so that we don't accidentally include the old activity thus avoiding
    # more errorneous diffs.
    # If this is the first message in the stream, this is going to fail, so we
    # can just pass on that iteration.
    try:
        if time < last[0]:
            continue
    except IndexError:
        pass
    # insort(x, y), from bisect package: for inserting sortable y into
    # iterable x so as to keep the values in x ascending.
    insort(last,time)
    # condition to spit out a delta: 
    # more than five seconds elapsed between the most recent edit and the earliest edit. 
    # goal: create a kind of time-window. The difference of 5 seconds
    # between the highest and lowest time readings ensures that at least five
    # seconds have elapsed (on the server) since any event that would change the
    # diff that we are outputting. This roughly corresponds to the assumption
    # that the server will push out any changes within five seconds of it
    # happening.
    if last[-1] - last[0]>5:
        # Poping the oldest entry in the array, removing it and
        # shifting everything over one spot.
        oldest = last.pop(0)
        # Subtract it from the new first element (the second oldest)
        diff = last[0]-oldest
        # dump the diff to stdout as a JSON with key 'delta'
        print(json.dumps({'diff':diff}))
        stdout.flush()
