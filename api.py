import json
import util
from flask import flask,request

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
