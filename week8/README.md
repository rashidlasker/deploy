```
import json
import boto3
import time
from decimal import Decimal

# Custom JSONEncoder that can encode Decimals.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Wrap our return object into Lambda's desired response type.
def respond(err, res=None, cls=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res, cls=cls),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    # Connect to our DynamoDB table. IMPORTANT: make sure this table name is
    # correct.
    table = client.Table("analytics")
    
    method = event['httpMethod']
    
    if method == 'GET':
        # Return all rows if GET request.
        return respond(None, table.scan(), cls=DecimalEncoder)
    else:
        # Create new item if POST request.
        json_dict = json.loads(event['body'])
        response = table.put_item(
            Item={
            'pagePath': json_dict['pathname'],
            'timestamp': Decimal(str(time.time())),
            'location': {
                'latitude': Decimal(str(json_dict['location']['latitude'])),
                'longitude': Decimal(str(json_dict['location']['longitude'])),
            },
            'platform': json_dict['platform'],
            'userAgent': json_dict['userAgent'],
            'language': json_dict['language'],
        },
        )
        
    return respond(None, response)
```
