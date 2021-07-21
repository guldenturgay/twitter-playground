from flask import Flask, render_template, request 
from wtforms import Form, TextAreaField, validators
import __classification_init__
from __classification_init__ import predict_emotion
import get_tweets
from get_tweets import get_tweets
app = Flask(__name__)


def request_results():
    tweets = get_tweets()
    tweets = tweets.tweet_text
    predictions=[]

    for tweet in tweets:
        pred = predict_emotion(tweet)
        predictions.append(pred)
        emotion = max(set(predictions), key = predictions.count)
    return emotion


@app.route('/')
def index():
    output = request_results()
    return render_template('result.html', output=output)
   

#@app.route('/result', methods=['GET'])
#def find_emotion():
    #if request.method == 'GET':
        #output = request_results()
        #return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=False)
    