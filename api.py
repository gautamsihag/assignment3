# To connects to a Redis database 
# table 0: with time diffs between events, 
# table 1 with a distribution over articles, and 
# defination for the API to
# access the rate, the histogram, the entropy,
# and the probability of a given message.

import json
import util
from flask import Flask,request

app = Flask(__name__)

@app.route('/rate')
def get_rate():
	rate = util.rate()
	return json.dumps({'avg_rate':rate})

@app.route('/histogram')
def get_histogram():
	hist = util.histogram()
	return json.dumps(hist)

@app.route('/entropy')
def get_entropy():
	entropy = util.entropy()
	return json.dumps({'entropy':entropy})
@app.route('/probability')
def get_probability():
	title = request.args.get('title')
	if not title:
		return json.dumps({'error':'no \'title\'argument given'})
	prob = util.probability(title)
	response = {'title':title,'p':prob}
	return json.dumps(response)

if __name__=='__main__':
	app.run(debug=True)
