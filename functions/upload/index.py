import boto3
import json
import base64

client = boto3.client('dynamodb')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pwc-dynamodb-table')

headers = {
    'Access-Control-Allow-Origin': '*',  # Allow any origin
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS,PUT,DELETE',
    'Access-Control-Allow-Credentials': 'true',
}


def upload_file(file_name, bucket_name, object_name, metadata, file):
    # file remove prefix
    file = file.replace('data:image/jpeg;base64,', '')
    file = base64.b64decode(file)
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, file_name).put(
        Body=file, Metadata=metadata, ContentType='image/jpeg')
    return True


def handler(event, context):
    path = event['path']
    method = event['httpMethod']

    body = event['body']

    if path == '/upload' and method == 'POST':
        body = json.loads(body)
        file = body['file']
        file_name = body['file_name']
        bucket_name = body['bucket_name']
        object_name = body['object_name']
        metadata = body['metadata']

        if upload_file(file_name, bucket_name, object_name, metadata, file):
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "path": path,
                    "params": body,
                    "event": event
                }),
            }
        else:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "path": path,
                    "params": body,
                    "event": event
                }),
            }
    else:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({
                "path": path,
                "params": body,
                "event": event
            }),
        }
