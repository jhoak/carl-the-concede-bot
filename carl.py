"""
This script runs Carl's tweeting session in a loop.
To use it, just type the following in a console:

python carl.py
"""

import random, re, time
import keys, resps
import tweepy

# Get access to Twitter (i.e. ability to tweet, get others' tweets, etc)
handler = tweepy.OAuthHandler(keys.cons_key, keys.cons_key_secret)
handler.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(handler)
user = 'arguetron'
handle = '@' + user + ' '

# Get latest tweet first
timeline = api.user_timeline(id=user, count=1)
last_tweet = timeline[0].id

# Setup initial reply to start the conversation
firstone = True
firstresp = handle + random.choice(resps.starts)

# Set up later replies in conversation
responses = resps.all
lastresp = None
response = None

# Convo loop
while last_tweet:
	# Reply to last tweet (special case for initial reply)
	if firstone:
		response = firstresp
		firstone = False
	else:
		# No duplicates!
		while response == lastresp:
			response = handle + random.choice(responses)
	
	# Finally tweet our message
	api.update_status(response, in_reply_to_status_id=last_tweet)
	lastresp = response
	
	# Wait a bit (5min) for a reply
	time.sleep(300)

	# Receive arguetron's reply
	latest_tweets = api.user_timeline(id=user)
	for tweet in latest_tweets:
		text = tweet.text
		to_me_regex = r'@concedebot'
		if re.match(to_me_regex, text):
			last_tweet = tweet.id
			break
	else:
		last_tweet = None

# We're out of the loop, so we can't reply anymore for some reason. Finish!
print("Uh oh! Couldn't find a new tweet to reply to.")