import boto3
import json

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pwc-dynamodb-table')


def handler(event, context):
    params = event['queryStringParameters']
    path = event['path']
    method = event['httpMethod']

    if path == '/users/create' and method == 'POST':
        user = params['user']
        print(user)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "path": path,
            "params": params,
            "event": event
        }),
    }
