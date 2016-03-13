# govwithmike hw3
# Storytelling with streaming data HW3
I am looking to use meetup api to figure out the states where the rate of booking a meetup using the meetup is comparably higher as compared to others. Metups are where people usually from tech companies get together to network, talk shop, and learn from each others. 

The general thought process is that as per this assumption the rate of booking should be almost be constant because of the states with the likes of New York, California and washington. So the system is accessed at a constant rate. I am tracking this assumption usign a counter for 10 states which I have chosen as per my thought process of the states with the highest percentage of tech companies. It turns out that tech industry meets steadily at a reservation which may be taable at a coffee shop, a bar table or a board room. 

It is significant to note that Meetup was stated in New york and not in the Sillicon valley. The rate of technology meetups has been growing at seady rate since 2013 when it was at a high of 89%. While it is not accurate to compare the states in the united states, there can still interesting insights to be gleaned from the usage accross various states. New York and california are well out in front and they together have the most number of users as compared to members put together from rest of the nation. 

Consuming event stream of meetup.com in specific the RSVP event stream to obtain infromation about a reservation. The idea here is that booking of events reflects the frequency of people organizing an event, tells about what is the frequency and the urgency. As we discussed in class, stories require change, and a lot of meeting bookings reflects a lot of
transfer of communication across platforms and involves varied people. so here I consider when the rate of events booking changes and steps over the certain threshold (e.g. the average time between events has dropped to a small number, or the events are happening very frequently). 
The threshold for the rate alerts i.e the time between the meetup reservation is variable bt I have initialized it with the intitial value of 20 seconds and it is dynamically adjusted as per the trend under the current polled api stream. The 20 seconds is just an arbitrary initial value and has no associated bias but it is ajusted on the go as the system sees a change in the trend as described before.

The probablility thresholdo for notifiation is 5. I have chosen this as per the previous assumption and keeping a comparable probability of placing a meeting request. The key to understand here is that the system is keeping track of the rate at which it has been seeing the booking probability of 15%. Now if the request falls below or crosses the  rate of meeting being reserved at the specified 10 states, the systems raises an alert. If the rate crosses a higher benchmark, it can be said that the bookings for reservation are being made at a higher rate but if the rate falls below 15%, it can be sensed that there is an unusual pattern of low meeting behaviour.

For entropy, it is observable that the system might be looking forward to be interested in the situation where the distribution over the states evens out. Certain states like New York or California should generally dominate, so there is pretty low entropy to begin with. As such cetain states like Maine which to my observation has a comparably lower rate of meeting bookings, suddely sees a lot of reservation, the entropy will rise as the distribution evens out. 

Stream can be accessed at:  
http://stream.meetup.com/2/rsvps with the detailed documentation at:
http://www.meetup.com/meetup_api/docs/stream/2/rsvps/.
 As per my second assignment, notifications are sent through Slack bot.
# Sample JSON format of a meetup API response

The detailed infromation for the data dictionary can be accessed at: http://www.meetup.com/meetup_api/docs/stream/2/rsvps/

# Included Files:
There are two .sh files, that means two commands to be executed simulatneoulsy: 

1. Step 1: For connecting to the RSVP meetup API, calculating the amount of time that elapsed between two events and loading these time differences into a Redis in-memory database.
2. Step 2: For calculating the average amount of time between consecutive events (using the data in the Redis database), creating an alert when the average time-between-consecutive-events crosses the specified THRESHOLD, and communicating these via Slackbot.


# Visualization and API Launchpad
The API is in `api.py` and has the following endpoints: 

- `GET /histogram`
    - Retrieve the histogram. The keys are states nane and the values are the ratio of total reservation for that state to toal reservation of all states.
- `GET /entropy`
    - Returns the eentropy in JSON encoded form.
- `GET /probability`
    - Returns the probability of a message as JSON encoded objet.
- `GET /vis`
  - To view the webpage with a simple visualization over distribution over the states.

## API Launchpad
Make sure the backend is running. To start the API:

```python api.py```


# Notifications

There are two prallel notification system that system maintains.

```
reservation-db.py -> check-detect.py -> pushwithslack.py

meet2.py -> unusualness.py -> puchwithslack.py
```
## Notification System

Please make sure that the backend is already running and the notification can be launched all together.

This command sets up alerts for entropy and rate anomalies.

```python reservation-db.py | python check-detect.py | python pushwithslack.py```

This command polls the rate and entropy of the database every one second, then outputs it to the checking mechanism for anomaly detection, and any detected anomaly that are found are sent via Slack. 
This command sets up alerts for unlikely messages (articles) in the stream.

```python ingest.py | python unusualness.py | python pushwithslack.py```

The second command listens to the stream, and for each message, calculates the probability of the incoming messages using the data in the Redis database as the reference distribution.

## Slack

Finally, you'll need to have a Slack channel set up and ready for a Slackbot. if you're not accessing this through the GitHub repo, this is already set, although you'll want to log into the Slack team to check out the notifications it produces. If you are not able to figure out how to make it work, please contact me and I can set you up.

## Files for Step 1: 

- `1-stream-ingest.sh`
	- script to process the step 1. 
	- Before running this, make sure there is a Redis database server serving over the default port (6379)!
- `meet2.py`
	- Connects to the RSVP meetup API, and outputs the edit event messages to stdout.
- `diff.py`
	- Reads the event messages via stdin, retrieves the timestamp (Unix epoch time) and then calculates the elapsed (server) time between two events and outputs them to stdout.
- `redis-insert.py`
	- Takes the time differences and sticks them into a Redis database, each with a 120 second lifespan.

## Files for Step 2:

- `avg.py`
	- This script looks at all entries in the Redis database and calculates the average of the time differences there. It outputs this average to stdout.
- `check_detect.py`
	- Reads the average values coming via stdin from `avg.py` and checks if the value is falls under the desired booking phase or tends to cross out of it.
- `pushwithslack.py`
	- This script reads the data from stdin and creates a message to be posted on Slack. It then posts that message to the Slack channel using the URL in `CONFIG_SLACK.py`.
- `CONFIG_SLACK.py`
	- You should create it yourself, or use the repository I have provided! It contain a single line for SLackbot's 
	- url =`https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.


Please refer to [Slack's API webpage](https://api.slack.com/)--> log in--> click the button that says 'Start building custom integrations,' and follow the instructions to setup an 'Incoming Webhook.' Once that URL is set, you must insert that URL into a file called `CONFIG_SLACK.py`, which should have a single line that looks like this:

```
url = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
```

Of course, insert the URL you got through the Slack API. The online interface allows you to specify what channel you would like it to post to, what the avatar should be for that bot, and some other features like that.

## Step 1:

This step is associated with the backend of the system. Here is brief desription of the system:
The bakend system consumes the meetup reservation data stream (`meet2.py`) and sends it to two processes. So it can be said that the system workflow from here proceeds with two paths. The first path is the employed to calculate the rate. `diff.py` uses a queue to so as to reorder the reservation as per the timings of the incoming message and presents the difference between reservation in the stream. `insert-diff.py` takes those time difference and sends them to redis db in a manner similar to the second assignment.

The second is the insert-distribution path, which uses `insert-distribution.py` pulls out the variable from the reservation stream in which the system is interested, here it is 'group_state', which is unique for each reservation and puts it into the database. The values that had not been seen before, the system puts them as a new entry.

## Launching the backend

The backend will start loading the time diffs between messages and the distribution of state meeting reservation into the Redis database.


```
python meet2.py | tee >(python diff.py | python insert-diffs.py) >(python insert-distribution.py)
```

This is launching an instance of `meet2.py`, and splitting the output to both branches described above.


## Step 2:

run the following command:

```
./notifysystem.sh
```


or the following command:

```
python avg.py | python check_detect.py | python pushwithslack.py
```

# Displaying Histogram

The histogram can be launched as:

```
python api.py
```
Then open a web browser and visit localhost:8000/vis. 
