# This script takes the Unix-piped stream from meet2.py. 
# it calculates the time difference between the two
# earliest timestamps, outputs the result as a JSON to stdout.
# This script is a copy of:
# https://github.com/mikedewar/RealTimeStorytelling/blob/master/2/diff.py
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
    try:
        if time < last[0]:
            continue
    except IndexError:
        pass
    insort(last,time)
    if last[-1] - last[0]>5:
        oldest = last.pop(0)
        diff = last[0]-oldest
        print(json.dumps({'diff':diff}))
        stdout.flush()