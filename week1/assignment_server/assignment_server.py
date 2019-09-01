from flask import Flask, escape, request
from models import User, Tweet, db
from playhouse.shortcuts import model_to_dict, dict_to_model
import json

app = Flask(__name__)

@app.route('/')
@app.route('/<page>')
def show(page=1):
    return user_id + ':' + username
def hello():
    tweets = Tweet.select().order_by(Tweet.created_date.desc()).paginate(page, 10)
    return "\n".join([str(tweet) for tweet in tweets])


@app.route('/new/<username>/<message>')
def newTweet(username, message):
    # If user with username exists, get it.
    try:
        user = User.get(User.username == username)
    # Otherwise, create one with username.
    except:
        user = User(username=username)
        user.save()

    # Create tweet of message associated with user.
    tweet = Tweet(user=user, message=message)

    return str(tweet)



