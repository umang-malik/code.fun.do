# Import the necessary methods from tweepy library
import sys

from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from tweepy import TweepError

import warnings
warnings.filterwarnings("ignore")

# Variables that contains the user credentials to access Twitter API 
# # keys from  "Twitter Tweet Summarization" app
access_token = "972806976777478144-k0gLBZPPsMj5NYOhGKlhHeCGZfpNcfV"
access_token_secret = "tCrQnXcx8h23SHvX483hugz6gXiPr9B5T8nMRbq7RTnt3"
consumer_key = "8UuhBhE1mDnM4KRxX4q1xClda"
consumer_secret = "0RbKRTsgEV05qPGZV5gtS8f63ex7fZxg3HHvtuUNsxMNUmla5O"

DATA_FOLDER = sys.argv[2].encode('utf-8')

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True
    def on_error(self, status):
        print (status)

def query_through_stream(topic):
    stream = Stream(auth, l)
    stream.filter(track=[topic])

def query_through_search(query):
	TOPIC_DATA_HANDLER = open(DATA_FOLDER + query, 'w')
	api = API(auth)
	
	tweets = dict()
	# # Initialization ## 
	max_tweets = 200
	tweet_count = 0
	max_id = -1
	since_id = None
	tweet_per_query = 100
	
	# print("Downloading tweets for query : "+query)
	while tweet_count < max_tweets:
		try:
			print(max_id)
			if max_id <= 0:
				if (not since_id):
					new_tweets = api.search(q=query, count=tweet_per_query, lang="en", result_type="mixed", locale="en", tweet_mode="extended")
				else:
					new_tweets = api.search(q=query, count=tweet_per_query, since_id=since_id, lang="en", result_type="mixed", locale="en", tweet_mode="extended")
			else:
				if (not since_id):
					new_tweets = api.search(q=query, count=tweet_per_query, max_id=str(max_id - 1), lang="en", result_type="mixed", locale="en", tweet_mode="extended")
				else:
					new_tweets = api.search(q=query, count=tweet_per_query, max_id=str(max_id - 1), since_id=since_id, lang="en", result_type="mixed", locale="en", tweet_mode="extended")
			if not new_tweets:
				print("No more tweets found")
				break
			tweet_id_iter = None
			for tweet in new_tweets:
				# json_tweet = jsonpickle.encode(tweet._json, unpicklable=False)
				if(tweet.user.followers_count > 200 and tweet.full_text not in tweets):

					
					tweet_text = (tweet.full_text).strip().replace('\n',' ')

					tweets[tweet.full_text] = 1  # # for duplicate identification
					
					TOPIC_DATA_HANDLER.write(tweet_text + '\n\n')
					tweet_count += 1
					if(tweet_id_iter):
						tweet_id_iter = min(tweet_id_iter, tweet.id)
					else:
						tweet_id_iter = tweet.id
					if(tweet_count == max_tweets):
						break					

			max_id = tweet_id_iter
			if max_id == None:    #API limit reached
				max_id = -2
				break
		except TweepError as e:
			print("some error : " + str(e))
			break
	
def isEnglish(s):
    return all(ord(c) < 128 for c in s)
        
if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    TOPICS = sys.argv[1]
    for topic in open(TOPICS, 'r'):
    	if(isEnglish(topic)):    		
	    	query_through_search(topic.strip().encode('utf-8'))
    	
    # query_through_stream("Scandal")