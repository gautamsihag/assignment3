# must create it by the user or use mine 
# contains a single line,
# url = 'users Slackbot's URL'. 
# It should look something like 
# https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX.
# The Slack API requires just one argument, the message content 
# I have built this using the details here:
# https://api.slack.com/incoming-webhooks
# The Slack API specifies the data be encoded as a JSON string in the body
# of the post request. The `json` parameter
# takes a dictionary and post it as a JSON string, equivalent to:
# data=json.dumps(data).

url = 'https://hooks.slack.com/services/Txxxxxxxxx/xxxxxxxx/xxxxxxxxxxxxxxxxxxx'
