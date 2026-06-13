import json
import os
import psycopg2

def lambda_handler(event, context):
    # Connect to Aurora Postgres
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    cur = conn.cursor()
    
    for record in event['Records']:
        body = json.loads(record['body'])
        message = body.get('message', 'empty')
        
        # Save to database
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        print(f"Processed message: {message}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'Success'})
    }
