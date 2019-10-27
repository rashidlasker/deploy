Assignment 7:  Analytics
========

[Week 7 slides](https://docs.google.com/presentation/d/1O3mh5e6nY46rENSuxEYg6mqi7bDv2ZasN_BTrMxfYeA/edit?usp=sharing)

This week you'll be implementing a simple Django endpoint to capture analytics information from your users. This endpoint will log user information and output them to an external log file. You'll also learn about template inheritance and performing client-side requests.

Django View
-----
You'll need to write a simple Django view that will take in a POST request containing user information and then log it to a file on your machine. You will also need to edit `urls.py` to make this view accessible as an API endpoint. What information you choose to log is up to you, but our provided JavaScript code gives you location, webpage path, platform, and user agent. You might also be able to collect a user's IP address by following the advice given [here](https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django). 

We recommend appending values in CSV (comma separated values) format to a text file.

Template Inheritance + Client-side Requests
-----
Template inheritance is a useful feature of Django that allows you to write a set of code once and then apply it to all your web pages. Here, we will write a wrapper that calls the logging endpoint on every page. The example repo includes code under `deploy_app/templates` that shows how it works. The starter code below shows you how to extract information from a user's client-side browser and then call the logging endpoint.

[`base.html`](https://github.com/rashidlasker/deploy/blob/master/week7/example-repo/app/deploy_project/deploy_app/templates/base.html)

What to turn in
---------------

Send us a link to your GitHub repo after you implement the client-side requests and logging endpoint. Next week we'll go into sending requests to Lambda!

We strongly encourage you to take time to demo in the office hours or in lab. We want to make sure not only you are writing code that works but also code that is of best practices.
