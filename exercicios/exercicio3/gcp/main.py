import functions_framework
import sqlalchemy
import os
import base64
import json

# Connection pool
db_config = {
    "pool_size": 5,
    "max_overflow": 2,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}

def init_connection_engine():
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    db_host = os.environ.get("DB_HOST") # Private IP
    
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            host=db_host,
            database=db_name,
        ),
        **db_config
    )
    return pool

engine = None

@functions_framework.cloud_event
def process_queue(cloud_event):
    global engine
    if engine is None:
        engine = init_connection_engine()
        
    # Decode pub/sub message
    pubsub_message = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    data = json.loads(pubsub_message)
    
    with engine.connect() as conn:
        conn.execute(
            sqlalchemy.text("INSERT INTO messages (content) VALUES (:content)"),
            {"content": data.get("message", "empty")}
        )
        conn.commit()
    
    print(f"GCP processed message: {data}")
