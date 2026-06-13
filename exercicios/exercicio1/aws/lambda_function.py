import json
import boto3
import os
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'exercicio1-table')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    path = event.get('path')
    http_method = event.get('httpMethod')
    
    if http_method == 'POST':
        body = json.loads(event.get('body', '{}'))
        item_id = str(uuid.uuid4())
        item = {
            'id': item_id,
            'name': body.get('name', 'Unknown'),
            'description': body.get('description', '')
        }
        table.put_item(Item=item)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Item created', 'id': item_id})
        }
    
    elif http_method == 'GET':
        result = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(result.get('Items', []))
        }
    
    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method not allowed'})
    }
