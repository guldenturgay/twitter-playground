from flask import Flask, render_template, request 
from flask_restful import Api
from wtforms import Form, TextAreaField, validators
from requests_oauthlib.oauth1_auth import Client
import __classification_init__
from __classification_init__ import predict_emotion
import get_tweets
from get_tweets import get_tweets
from dotenv import load_dotenv
import os



load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')


app = Flask(__name__)
api = Api(app)

# Initialize Our OAuth Client
oauth = Client(API_KEY, client_secret=API_SECRET_KEY)

from twitter import TwitterAuthenticate, TwitterCallback


"""def request_results():
    tweets = get_tweets()
    tweets = tweets.tweet_text
    predictions=[]

    for tweet in tweets:
        pred = predict_emotion(tweet)
        predictions.append(pred)
        emotion = max(set(predictions), key = predictions.count)
    return emotion

"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

"""

@app.route('/result', methods=['POST'])
def print_result():
    output = request_results()
    return render_template('result.html', output=output)

"""



#@app.route('/')
#def index():
    #output = request_results()
    #return render_template('result.html', output=output)
   

#@app.route('/result', methods=['GET'])
#def find_emotion():
    #if request.method == 'GET':
        #output = request_results()
        #return render_template('result.html', output=output)

api.add_resource(TwitterAuthenticate, '/authenticate/twitter')
api.add_resource(TwitterCallback, '/welcome') # This MUST match your Callback URL you set in the Twitter App Dashboard!!!

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
    