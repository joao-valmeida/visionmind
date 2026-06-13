import azure.functions as func
import logging
import os
import psycopg2

app = func.FunctionApp()

@app.service_bus_queue_trigger(arg_name="msg", 
                               queue_name="exercicio3-queue",
                               connection="ServiceBusConnection")
def process_service_bus_message(msg: func.ServiceBusMessage):
    message_body = msg.get_body().decode('utf-8')
    logging.info(f"Azure processed Service Bus message: {message_body}")
    
    # Connect to PostgreSQL (Private)
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (%s)", (message_body,))
    conn.commit()
    cur.close()
    conn.close()
