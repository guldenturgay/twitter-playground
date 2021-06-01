import tweepy as tw
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_tweets():
    
    timeline = api.home_timeline(count=1000)

    tweets = []
    for tweet in timeline:
        text = api.get_status(id=tweet.id, tweet_mode = 'extended', lan='en').full_text
        tweets.append(text)
        home_timeline_tweets = pd.DataFrame(tweets, columns=['tweet_text'])

    return home_timeline_tweets
        
