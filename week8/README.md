1. follow this guide to create a lambda function: https://docs.aws.amazon.com/lambda/latest/dg/with-on-demand-https-example-configure-event-source_1.html
2. copy paste the code `example-lambda.py`. READ THIS THOROUGHLY
3. Create a DynamoDB table with partition key pagePath of type string and sort key timestamp of type number. Modify the code in your lambda function to point to this table
4. get the API gateway URL (should look something like this: https://hhsmls5bb6.execute-api.us-east-2.amazonaws.com/default/analytics)
5. you can POST to the gateway url a request with body raw = {"pathname":"/","language":"en-US","platform":"MacIntel","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36","location":{"latitude":38.0307484,"longitude":-78.5077828}}
6. you can GET to the gateway URL to get a list of all records (edited) 

notes for sunday:
- POST / GET demo to API gateway
- structure of Lambda + API gateway + dynamoDB service
- talk about partition / sort key and why we chose the ones we did