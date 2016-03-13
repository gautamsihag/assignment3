import json
from sys import stdout
from time import sleep
import util

while True:
    entropy = util.entropy()
    rate = util.rate()
    print (json.dumps({'entropy':entropy,'rate':rate}))
    stdout.flush()
    sleep(1)