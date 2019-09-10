import tweepy
import sys

#This file is not tracked because the credentials are PERSONAL. Just put your credentials file on the same directory and it will be fine
sys.path.insert(1, '/Estudos/TwitterAPI')
import tt_credentials

'''

Part 2: Cursor and pagination. With this, we can access our own tweets,
user tweets, followers or friends from a specific user

It picks up from the first part's code and improves it

'''
class twitterAuthenticator():

	def authenticate(self):
		#The authentication process is handled by the OAuthHandler
		authentication = tweepy.OAuthHandler(tt_credentials.CONSUMER_KEY, tt_credentials.CONSUMER_SECRET)
		authentication.set_access_token(tt_credentials.ACCESS_TOKEN, tt_credentials.ACCESS_TOKEN_SECRET)
		return authentication


class twitterListener(tweepy.StreamListener):

	def __init__(self, target_filename):
		self.target_filename = target_filename

	def on_data(self, data):
		#This method handles the arrival of data on our streamer
		f = open(self.target_filename, 'a')
		f.write(data)
		print(data)
		return True

	def on_error(self, status):
		#This method handles the error while streaming
		if status == 420:
			#Kills the connection when error 420 (rate limit) happens
			return False
		print(status)


class twitterStreamer():

	def __init__(self):
		self.tt_authenticator = twitterAuthenticator()


	def stream_tweets(self, target_filename, keywords_list):
		#This method handles the authentication and streaming of tweets
		#Our listener object
		listener = twitterListener(target_filename)
		#We create our authentication object
		authentication = self.tt_authenticator.authenticate()
		#The scream object, passing the listener and the authentication as arguments
		stream = tweepy.Stream(authentication, listener)
		#We need to filter Tweets acoording to a set of keywords or hashtags
		stream.filter(track=keywords_list)

class twitterClient():

	def __init__(self, tt_user=None):
		self.auth = twitterAuthenticator().authenticate()
		self.tt_client = tweepy.API(self.auth)
		#None is default because if we don't specify a user, it defaults to ourselves
		self.tt_user = tt_user

	def fetch_user_tweets(self, num_tweets):
		tweetlist = []
		#Iterate through the tweets on a user's timeline and gets his tweets.
		for tweet in tweepy.Cursor(self.tt_client.user_timeline, id=self.tt_user).items(num_tweets):
			tweetlist.append(tweet)
		return tweetlist

	#We can also use this for getting friendlist. We'll evolve this later
	#The only thing different is that we'll use the .friends attribute from the tt_client

if __name__ == '__main__':

	ttclient = twitterClient('jairbolsonaro')
	print(ttclient.fetch_user_tweets(1))
