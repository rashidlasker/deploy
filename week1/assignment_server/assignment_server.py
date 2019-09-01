from flask import Flask, request, render_template, jsonify
from models import User, Tweet, db
from playhouse.shortcuts import model_to_dict
import json

app = Flask(__name__)

# Return template rendering of tweets.
@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    # Paginate the list of tweets and show the newest ones first.
    tweets = get_tweets(page)
    return render_template('home.html', tweets=tweets, page=page)


# Returns JSON representation of tweets.
@app.route('/tweets')
@app.route('/tweets/<int:page>')
def tweets(page=1):
     # Paginate the list of tweets and show the newest ones first.
    tweets = get_tweets(page)
    return jsonify([model_to_dict(tweet) for tweet in tweets])

# Create a new tweet for user with given username and message.
@app.route('/new', methods=["POST"])
def new():
    username = request.form['username']
    message = request.form['message']

    # If user with username exists, get it.
    try:
        user = User.get(User.username == username)
    # Otherwise, create one with username.
    except:
        user = User.create(username=username)

    # Create tweet of message associated with user.
    tweet = Tweet.create(user=user, message=message)

    return str(tweet)

# Return page of tweets.
def get_tweets(page):
    return Tweet.select().order_by(
        Tweet.created_date.desc()).paginate(page, 10)
