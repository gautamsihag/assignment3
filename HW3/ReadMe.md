#Overview

In this home work, I have again chosen stream data from meetup.com which sends an event everytime some one signs up for the meetup. Details regarding the stream including the data dictionary of the stream is present in readme file of previous homework (https://github.com/ss4609/Storytelling-With-Streaming-Data/blob/master/Hw1Part1README.md).

So in this homework I am capturing the distribution of states of meetup for which rsvps are happening. I have extended the alerting system to send out an alert (I am showing it on a webpage) when the rsvp happens for a state whose probability of rsvp is less that .1%. Again as the rate of rsvp and state distribution varies during the date and time of day, this threshold can be driven by user input. The general idea can be drawn by observing the distribution barchart (histogram) - also a web page that I provide, to see what is the lower 5% of distribution looks like. Again if the entropy is high then this value could be high like 2% or when entropy is low then it could be as low as .01%. 

##Run Command
Note: all the below commands should be run on separate terminal windows

//Starts the redis server

redis-server

//Extracts states and timestamp of rsvp from the stream and sends the states to db1 and time diff to db0

python ingest.py | python  insertStatesAndCalcDiff.py | python insertTime.py 

//Starts the flask server and calculates entropy, distribution, rate, probability of signup from a state and distribution chart for the rsvps. All these are configured as get request (example of url calls provided below)

python apiState.py

//Start the alerting module. If a state rsvp happesn and if that state's rsvp probability is less than the threshold (provided by user as an argument) then an alert is sent via websocket server on port 8080.

websocketd --port=8080 python alertUnlikelyStateRsvp.py .1

Note: below are the urls

//Shows the rate rsvps (rate = time between rsvps). E.g. output {"rate": 0.9898505562641582}

http://127.0.0.1:5000/rate

//Shows the distribution of rsvps by state. E.g. output {"CA": 0.040110650069156296, "NY": 0.02351313969571231, "NJ": 0.0013831258644536654}

http://127.0.0.1:5000/distribution

//Shows the entropy of above distribution. E.g. output {"entropy": 3.157349414538496}

http://127.0.0.1:5000/entropy

//Shows probability of rsvp from the state provided in url argument (calculated based on histrorical distribution for that state). E.g. {"state": "CA", "probability": 0.2451523545706371}

http://127.0.0.1:5000/probability?state=CA

http://127.0.0.1:5000/probability?state=NY

//Listens to port 8080 and if there is an alert then it shows that alert

alertUnlikelyStateRsvp.html

//Shows the distribution of rsvp by state as a bar chart

http://127.0.0.1:5000/distributionChart

#Sample Alerts
RSVP occurred from Unlikely state: WI (probability = 0.00604229607251) 

RSVP occurred from Unlikely state: OR (probability = 0.0275650842266) 

#Dependencies
Python 2.7

Non basic python packages = requests-2.9.1

Redis

Websocketd
