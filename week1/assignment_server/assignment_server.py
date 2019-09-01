from flask import Flask, request, render_template
from models import User, Tweet, db
import json

app = Flask(__name__)

@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    # Paginate the list of tweets and show the newest ones first.
    tweets = Tweet.select().order_by(Tweet.created_date.desc()).paginate(page, 10)
    # return "\n".join([str(tweet) for tweet in tweets])
    return render_template('home.html', tweets=tweets, page=page)


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



