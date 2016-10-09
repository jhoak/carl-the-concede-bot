import random, re, time
import keys, resps
import tweepy

handler = tweepy.OAuthHandler(keys.cons_key, keys.cons_key_secret)
handler.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(handler)

# Get latest tweet
timeline = api.user_timeline(id='arguetron', count=1)
last_tweet = timeline[0].id

responses = resps.all
firstone = True
firstresp = '@arguetron ' + random.choice(resps.starts)
lastresp = None
response = None

while last_tweet:
	# Reply to it
	if firstone:
		response = firstresp
		firstone = False
	else:
		while response == lastresp:
			response = '@arguetron ' + random.choice(responses)
	
	api.update_status(response, in_reply_to_status_id=last_tweet)
	lastresp = response
	
	# Wait a bit (5min?)
	time.sleep(300)

	# Receive arguebot's reply
	latest_tweets = api.user_timeline(id='arguetron')
	for tweet in latest_tweets:
		text = tweet.text
		to_me_regex = r'@concedebot'
		if re.match(to_me_regex, text):
			last_tweet = tweet.id
			break
	else:
		last_tweet = None

print("Uh oh! Couldn't find a new tweet to reply to.")