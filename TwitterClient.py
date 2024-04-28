import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient:
    
    #Constructor
    def __init__(self) -> None:
       
        consumer_key = 'X'
        consumer_secret = 'X'
        access_token = 'X-X'
        access_token_secret = 'X'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)

            self.api = tweepy.api(self.auth)
            print("Connection Successful")
        except:
            print("Error: Authentication Failed")
    
    # def post_tweets(self, tweet):

    #     self.api.post_tweets()