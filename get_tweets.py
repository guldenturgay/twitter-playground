import tweepy as tw
from dotenv import load_dotenv
import pandas as pd
import random
import os
import nltk
from nltk.corpus import stopwords
import re
import string
from autocorrect import Speller
stopword = nltk.corpus.stopwords.words('english')


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_tweets():
    
    timeline = api.home_timeline(count=50)

    tweets = []
    for tweet in timeline:
        text = api.get_status(id=tweet.id, tweet_mode = 'extended', lan='en').full_text
        tweets.append(text)
    home_timeline_tweets = pd.DataFrame(tweets, columns=['tweet_text'])


    # Function to clean and tokenize the data
    def clean_text(text):

        #Clear out HTML characters 
        import html
        text=html.unescape(text)

        # Replace or remove the characters 
        replacement_dict={"https?:\/\/.\S+":"", # Remove hyperlinks
                        "^RT[\s]+":"", # Remove old style retweet text "RT"
                        "\\n":"", # Remove newline caharacter
                        "@\w+.":"", # Remove mentions starting with @
                        "#":"", # Remove the hash # sign
                        "’":"'", # Replace ’ with '
                        "'s":" is", # Replace the contractions
                        "n't":" not",
                        "'m":" am",
                        "'ll":" will",
                        "'d":" would",
                        "'ve":
                        " have",
                        "'re":" are",
                        "\W+":" ", # Remove non-word caharacters
                        "^\s+":"" # Remove whitespace at the beginning
                        } 

        for item in replacement_dict.keys():
            text=re.sub(item,replacement_dict[item], text)
            
        # Separate the words 
        text = " ".join([char for char in re.split("([A-Z][a-z]+[^A-Z]*)",text) if char])

        # Replace double spaces with one
        text = re.sub("\s+"," ",text)     

        # Convert to lower case
        text = ''.join([char for char in text if char not in string.punctuation])
        tokens = re.split('\W+', text)
        
        # Remove stopwords
        text = ' '.join([word for word in tokens if word not in stopword])
        

        text = text.lower()
    
        # Spell check 
        spell = Speller(lang='en') 
        text=spell(text)  
        
        # Return text
        return text


    # Apply the function to text column
    home_timeline_tweets['tweet_text'] = home_timeline_tweets['tweet_text'].apply(lambda x: clean_text(x))

    return home_timeline_tweets
        
