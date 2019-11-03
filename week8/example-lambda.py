import json
import boto3 # AWS Python library.
import time
from decimal import Decimal

# Custom JSONEncoder that can encode Decimals. This is needed because
# DynamoDB cannot store floats (wtf?) so we must convert all floats 
# into Decimals.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Wrap our return object into Lambda's desired response type.
# err: Any error that occurred during the handling of the request
#       should be passed in as a parameter.
# res: The response object that we want to return to the API caller.
# cls: A custom JSONEncoder, if desired, can be passed in here.
def respond(err, res=None, cls=None):
    return {
        # We want to return a 200 status code (this means that the request
        # was handled successfully) if there is no error. Otherwise, return
        # a 400 error code. A 400 error code means that the request was
        # improper.
        'statusCode': '400' if err else '200',
        # If there's an error, we return the error string, otherwise we
        # return a JSON encoding of our response.
        'body': str(err) if err else json.dumps(res, cls=cls),
        # HTTP headers that pass along extra information to our API caller.
        'headers': {
            # Response type is JSON.
            'Content-Type': 'application/json',
            # Required for CORS support to work.
            'Access-Control-Allow-Origin' : '*',
            # Required for cookies, authorization headers with HTTPS.
            'Access-Control-Allow-Credentials' : True 
        },
    }

# Handle a request from API gateway.
def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    # Connect to our DynamoDB table. IMPORTANT: make sure this table name is
    # the correct one for your DynamoDB table.
    table = client.Table("analytics")
    try:
        method = event['httpMethod']

        # Return all rows in table if GET request.
        if method == 'GET':
            return respond(None, table.scan(), cls=DecimalEncoder)

        # Add data to DynamoDB if POST request.
        elif method == 'POST':
            # Create new item if POST request.
            json_dict = json.loads(event['body'])

            # Construct the item to place in DynamoDB from the request body.
            item = {
                'pagePath': json_dict['pathname'],
                # Note that to convert floats into Decimals, we need to first
                # cast it to a string. This is UGLY but is the simplest
                # solution we could come up with.
                'timestamp': Decimal(str(time.time())),
                'platform': json_dict['platform'],
                'userAgent': json_dict['userAgent'],
                'language': json_dict['language'],
            }

            # Location data is optional, so we only add it to the item if
            # it is present.
            if 'location' in json_dict:
                coords = json_dict['location']
                item['location'] = {
                    'latitude': Decimal(str(coords['latitude'])),
                    'longitude': Decimal(str(coords['longitude'])),
                }

            response = table.put_item(Item = item)

        # If not GET or POST, we don't need to do anything.
        else:
            return respond(Exception(f"HTTP Method {method} not supported."))
            
        return respond(None, response)
    except Exception as err:
        return respond(err)