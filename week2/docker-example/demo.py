import os

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    name = os.environ['NAME']
    return f'Hello, {name}'


app.run(host="0.0.0.0", port=int("80"), debug=True)
