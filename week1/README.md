# Assignment 1: Setting up a simple Flask web server API

## Goals

- Learn how HTTP requests work
- Learn how to use external APIs and services

## Overview

This project will introduce you to several topics, including Flask, web requests, JSON, and external APIs. This is an individual assignment.

In this project, you will create a Flask web server inside of a [Glitch](https://glitch.com/) container that will allow you to text “dweets” to [Dwitter](http://67.207.94.120:5000/), a centralized dweet interface developed for this class. This is actually how Twitter started out way back in 2006, and you can learn more about that [here](https://www.lifewire.com/history-of-twitter-3288854)! You will accomplish this task by using [Twilio](https://www.twilio.com) to interface with SMS messages and by using the Assignment Server API defined below within your Flask app.

## Introductory Resources

Before moving on with the project, we highly recommend watching the following videos to familiarize yourself with how requests work on the internet.

[Overview and Frontend](https://www.youtube.com/watch?v=e4S8zfLdLgQ)

[Servers & Scaling](https://www.youtube.com/watch?v=FTAPjr7vgxE)

## Creating a project in Glitch

Glitch makes it super easy to build and deploy simple apps onto the internet. We’ll be using it for Project 1 so that we can focus more on concepts and less on the details of deploying an app (don’t worry, we’ll cover that later!).

Glitch runs applications in containers. You can think of containers as tiny virtual computers that only exist to run your application. They help isolate your application from other applications running in different containers on Glitch’s servers and make it easier to deploy your app onto their servers. It’s likely that your application is running in a container alongside hundreds of others on a server in Glitch’s cloud.

You can find the project starter code [here](https://glitch.com/~deploy-project1-starter). Feel free to remix it and use it as a launching point for your own project.

## Using Flask

Flask is a micro-service framework for Python that makes it super simple to set up a web application. The starter code above handles most of the set up for this project, so you’ll primarily be working within the `server.py` file in your Glitch remix. You can read more about Flask in these [docs](https://flask.palletsprojects.com/en/1.1.x/).

- We highly recommend using the Python [requests](https://2.python-requests.org/en/master/) library for making GET and POST requests from Python.
- We also recommend the [json](https://docs.python.org/3/library/json.html) library for decoding and encoding JSON responses.

## Using Twilio

Twilio is a service that lets your programmatically send and receive text messages. The way you use Twilio is by interacting with their public API. The Twilio API abstracts away the whole process of interacting with a cellular service and lets you send SMS messages in under 10 lines of Python code. See the Glitch starter project for an example Twilio usage and see the [Python Quickstart](https://www.twilio.com/docs/sms/quickstart/python) for more example usage. You will need to sign up for a free trial of Twilio before starting this project (don’t worry, there’s no credit card required).

- To access the SMS message body and phone number from flask, use the following code in your route handler:

```
# Twilio will call the '/sms' endpoint of our server when a text is received
@app.route('/sms', methods=['POST'])
def sms_reply():
    # Pulling the message body and number from Twilio's request
    body = request.form['Body']
    number = request.form['From']
    
    # <more code here>
```

## Assignment Server API

We have built and deployed a server that will aggregate all of your dweets and display them all in one page. You can view the home page at http://67.207.94.120:5000. This is also an API server that your service will interact with to post and retrieve dweets. See the endpoint reference below. You can set the username to any username you want. One possible strategy is to use your phone number, which the Twilio API lets you access easily.

If you’re curious, you can view the assignment server code [here](https://github.com/rashidlasker/deploy/tree/master/week1/assignment_server).

### API Endpoints
GET `/` and `/<page>`: If `page` is not supplied, displays the 10 most recent dweets in HTML format. Otherwise, will display the `page`th page of dweets.

GET `/dweets` and `/dweets/<page>`: similar to above but returns in JSON format.

POST `/new`: Accepts a POST request with two keys, `username` and `message`. `username` is the username of the user for which to post the dweet for and `message` contains the dweet text.

## Submission requirements

For this project, we we’ll ask each of you to slack us a link to your Glitch project. A complete solution should let you text a number, have Twilio trigger an endpoint in your Flask project, and then have your Flask project interface with the Assignment Server API. You should be able to retrieve the 10 most recent dweets and post new dweets from your phone using SMS messages.

## Next Steps

### Git
You'll use GitHub for version control for this class. If you don't have a GitHub account already, go create one. There's good online help for using GitHub and Git.

Creating a repo for Project 1 is not required since it is an individual project and is hosted on Glitch. However, if you are not experienced with Git/Github, it is highly recommended that you start to familiarize yourself with it now. You should be familiar with using a basic [Git Workflow](https://guides.github.com/introduction/flow/), and consider using it when you start Project 2 with your group. You should not be pushing pycache files, database files, or database migration files on Github. Learn to use `.gitignore` to enforce this, otherwise nasty merge conflicts and other issues will pop up later on.

### IDEs
For this project, you will be writing most of your code in the Glitch online IDE. For later projects, we recommend using VSCode, but any text editor should suffice.

### Preparing your OS

If you’re on Windows 10 Home, we’ll need you to upgrade to Windows 10 Professional/Education to prepare your system for the next project. UVA offers a free license for Windows 10 Education [here](https://virginia.service-now.com/its?id=sc_cat_item&sys_id=bccebb0edbcfa38c2192e6650596190c&sysparm_category=1fe6564cdb65e74ca6ddc191159619f7). The installation instructions are [here](https://virginia.service-now.com/its?id=itsweb_kb_article&sys_id=%20de496c09db0dd7084f32fb671d9619a7).

If you’re on Linux or Mac, you don’t need to do anything extra at this time.

### Brainstorming project ideas
In the coming weeks, you should start brainstorming ideas to work on for the semester-long multi-part project. You will work on these projects in groups and will end up deploying these projects onto AWS. Try to think of something fun and creative that you can show off to your friends or put on your resume after Deploy ends. The project shouldn’t be particularly complex, but would ideally involve storing some kind of data and/or interacting with some external API.

