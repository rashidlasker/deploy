Week 8
----
[Slides](https://docs.google.com/presentation/d/1UWrqe_0HA57ZJkE_JLB9ai9o28wNSDqV3hNmmOFH9cc/edit?usp=sharing)

This week we'll be hooking up the analytics data collection code we wrote last week to a microservice built using AWS Lambda, API Gateway, and DynamoDB. This will replace our earlier solution, where we logged user data to a file. The purpose of this is to allow us to isolate our analytics data away from a single instance of our web app. This would be useful if we have to scale up and create multiple instances of our web app to meet demand.

## Setting up a Logging Database
To collect and store our logging information, we'll create a table in AWS DynamoDB, which is a managed NoSQL service. 

1. Sign in to the AWS Management Console and go to the DynamoDB dashboard.
2. Click on the **Create Table** button.
3. Give your table a name. We named ours `DeployHits`.
4. Set the partition key to `pagePath`. Note: In an actual implementation, we would likely use something with a wide range of values that are evenly distributed, like IP addresses.
5. Set the sort key to `timestamp` and set the type to `Number`.

## Setting up Lambda and API Gateway
1. Sign in to the AWS Management Console and open the AWS Lambda console.
2. Choose **Create Lambda function**.
3. Choose **Blueprint**.
4. Enter `microservice` in the search bar. Choose the **microservice-http-endpoint-python** blueprint and then choose **Configure**.
5. Configure the following settings.
   - Name – `analytics`.
   - Role – Create a new role from one or more templates.
   - Role name – `analytics-role`.
   - Policy templates – Simple microservice permissions.
   - API – Create a new API.
   - Security – Open.

## Writing your AWS Lambda function

We want our analytics microservice to support two HTTP methods, `GET`, and `POST`. 
- When our microservice receives a `POST` request, it expects the body to contain analytics data in JSON form. It'll parse this JSON and store this information in a new row in DynamoDB.
- When our microservice receives a `GET` request, it will return all of the rows in our DynamoDB table.

We highly encourage you to try to write the AWS Lambda function on your own. We have provided example code in `example-lambda.py` that will work for this project that you can use as reference in case you get stuck. `example-lambda.py` is well documented with thorough comments. If you choose to use it, please read through the code and make sure you understand how it works.

## Hook up your new microservice to your existing code

Your API endpoint URL should look something like this: https://hhsmls5bb6.execute-api.us-east-2.amazonaws.com/default/analytics. You have two options for integrating your microservice into your existing data collection code.
1. Client side. You can modify your base template to send `POST` requests directly to your AWS API using JavaScript's `fetch` function. Then, you won't even need the Django view you wrote to log data to a file.
2. Server side. You can modify the Django view that logs data to a file to instead send this data to your AWS API using a `POST` request.

## Visualizing your data
We've included `visualization.html`, which you can add, as a template, to your Django app to visualize page hit statistics. Feel free to build upon this and come up with more cool and interesting charts and visualizations!

# What to turn in

Send us a screenshot of your visualization page!