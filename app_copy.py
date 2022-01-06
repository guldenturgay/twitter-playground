from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv


app_copy = Flask(__name__)

load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
 
app_copy.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<\
!\xd5\xa2\xa0\x9fR"\xa1\xa8'
 
'''
    Set SERVER_NAME to localhost as twitter callback
    url does not accept 127.0.0.1
    Tip : set callback origin(site) for facebook and twitter
    as http://domain.com (or use your domain name) as this provider
    don't accept 127.0.0.1 / localhost
'''
 
app_copy.config['SERVER_NAME'] = 'http://getthemood.gulden.me/welcome'
oauth = OAuth(app)

@app_copy.route('/')
def index():
    return render_template('index.html')

@app_copy.route('/twitter/')
def twitter():
   
    # Twitter Oauth Config
    
    oauth.register(
        name='twitter',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        request_token_params=None,
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None,
        api_base_url='https://api.twitter.com/1.1/',
        client_kwargs=None,
    )
    redirect_uri = url_for('twitter_auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)
 
@app_copy.route('/twitter/auth/')
def twitter_auth():
    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    profile = resp.json()
    print(" Twitter User", profile)
    return redirect('/')
 
if __name__ == "__main__":
    app_copy.run(debug=True)