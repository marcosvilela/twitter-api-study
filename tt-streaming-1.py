import tweepy
import sys

#This file is not tracked because the credentials are PERSONAL. Just put your credentials file on the same directory and it will be fine
sys.path.insert(1, '/Estudos/TwitterAPI')
import tt_credentials

'''

Lucid Programming's tutorial on Twitter API with Python, using the 
Tweepy module. All these codes will be done based on Lucid's code.

Tweepy's documentation: https://tweepy.readthedocs.io/en/v3.5.0/
Lucid Programming's original video: https://www.youtube.com/watch?v=wlnx-7cm4Gg

'''


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
		print(status)


class twitterStreamer():

	def stream_tweets(self, target_filename, keywords_list):
		#This method handles the authentication and streaming of tweets
		#Our listener object
		listener = twitterListener(target_filename)
		#The authentication process is handled by the OAuthHandler
		authentication = tweepy.OAuthHandler(tt_credentials.CONSUMER_KEY, tt_credentials.CONSUMER_SECRET)
		authentication.set_access_token(tt_credentials.ACCESS_TOKEN, tt_credentials.ACCESS_TOKEN_SECRET)

		#The scream object, passing the listener and the authentication as arguments
		stream = tweepy.Stream(authentication, listener)

		#We need to filter Tweets acoording to a set of keywords or hashtags
		stream.filter(track=keywords_list)


if __name__ == '__main__':

	keywords_list = ['batman','tom king', 'dc comics']
	tweets_filename = "tweets.json"

	tt_streamer = twitterStreamer()
	tt_streamer.stream_tweets(tweets_filename, keywords_list)
