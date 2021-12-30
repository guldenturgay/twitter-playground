from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource, reqparse
from wtforms import Form, TextAreaField, validators
from requests_oauthlib.oauth1_auth import Client
# Import requests in order to make server sided requests
import requests
#import __classification_init__
#from __classification_init__ import predict_emotion
#import get_tweets
#from get_tweets import get_tweets
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')

# Create A Config To Store Values
config = {
    'twitter_consumer_key': API_KEY,
    'twitter_consumer_secret': API_SECRET_KEY
}


app = Flask(__name__)
api = Api(app)

@app.route('/welcome')
def welcome():
    form = CompareForm(request.form)
    return render_template('first_page.html', form=form)

# Initialize Our OAuth Client
oauth = Client(config['twitter_consumer_key'], client_secret=config['twitter_consumer_secret'])

# We have to create our initial endpoint to login with twitter
class TwitterAuthenticate(Resource):
    # Here we are making it so this endpoint accepts GET requests
    def get(self):
        # We must generate our signed OAuth Headers
        uri, headers, body = oauth.sign('https://twitter.com/oauth/request_token')
        # We need to make a request to twitter with the OAuth parameters we just created
        res = requests.get(uri, headers=headers, data=body)
        # This returns a string with OAuth variables we need to parse
        res_split = res.text.split('&') # Splitting between the two params sent back
        oauth_token = res_split[0].split('=')[1] # Pulling our APPS OAuth token from the response.
        # Now we have to redirect to the login URL using our OAuth Token
        return redirect('https://api.twitter.com/oauth/authenticate?oauth_token=' + oauth_token, 302)

# We need to create a parser for that callback URL
def callback_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('oauth_token')
    parser.add_argument('oauth_verifier')
    return parser

# Now we setup the Resource for the callback
class TwitterCallback(Resource):
    def get(self):
        parser = callback_parser()
        args = parser.parse_args() # Parse our args into a dict
        # We need to make a request to twitter with this callback OAuth token
        res = requests.post('https://api.twitter.com/oauth/access_token?oauth_token=' + args['oauth_token'] + '&oauth_verifier=' + args['oauth_verfier'])
        res_split = res.text.split('&')
        # Now we need to parse our oauth token and secret from the response
        oauth_token = res_split[0].split('=')[1]
        oauth_secret = res_split[1].split('=')[1]
        userid = res_split[2].split('=')[1]
        username = res_split[3].split('=')[1]

        print(userid)
        print(username)
        # We now have access to the oauth token, oauth secret, userID, and username of the person who logged in. 
        # .... Do more code here
        # ....
        return redirect('http://getthemood.gulden.me/welcome', 302)




api.add_resource(TwitterAuthenticate, '/authenticate/twitter')
api.add_resource(TwitterCallback, '/welcome') # This MUST match your Callback URL you set in the Twitter App Dashboard!!!

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
    