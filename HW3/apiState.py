from flask import Flask, request, render_template
import json
import redis
from collections import Counter
from math import log

#code borrowed from instructor's github

#in this piece of code we are spinning up a web server that allows us to get entropy, rate, distribution, probability of rsvp from particular state, distribution chart of the meetup.com rsvps

#connect to db containing time diff between rsvps
conn0 = redis.Redis(db=0)

#connect to db containing distribution of rsvp states
conn1 = redis.Redis(db=1)

#initialize flask server
app = Flask(__name__)

#function that calculates distribution of states. The distribution is basically the percentage of times each state has been rsvped in last 10 min
def calcDistribution():
    #get keys from the database
    keys = conn1.keys()
    
    # get the state names from the database
    messages = conn1.mget(keys)

    #get list of states along with the no. of times there has been rsvp for that state 
    messageCounts = Counter(messages)

    #calculate percent rsvp of each state
    numMessages = len(messages)
    distribution = {message: messageCount/float(numMessages) for message, messageCount in messageCounts.items()}
    return distribution

#calculates rate (avg amount of time between each meetup rsvp)
@app.route('/rate')
def getRate():
    # connect to database containing time diffs between meetup rsvp and get keys and values
    keys = conn0.keys()

    #calculate rate
    diffValues = conn0.mget(keys)
    diffValues = [float(diffValue) for diffValue in diffValues]
    rate = sum(diffValues)/len(diffValues)
    return json.dumps( {'rate': rate})

#calculates the distribution
@app.route('/distribution')
def getDistribution():
    distribution = calcDistribution()
    return json.dumps(distribution)

#calculates entropy
@app.route('/entropy')
def getEntropy():
    distribution = calcDistribution()
    entropy = -sum( [p*log(p) for p in distribution.values()] )
    return json.dumps({'entropy': entropy})

#calculates probability of meetup signup given a state
@app.route('/probability')
def getProbability():
    #get name of state from the argument /probability?state=NY
    state = request.args.get('state')

    #get the overall distribution
    distribution = calcDistribution()

    #compute the probability as the historic distribution value of that state
    probability = distribution.get(state, 0) 
    response = { 'state': state, 'probability': probability }
    return json.dumps(response)

#generate distribution chart
@app.route('/distributionChart')
def getDistributionChart():
    #the code goes to templates folder and looks fro distrubutionChart.html and renders it
    return render_template('distributionChart.html')


if __name__ == '__main__':
    app.run(debug=True)
