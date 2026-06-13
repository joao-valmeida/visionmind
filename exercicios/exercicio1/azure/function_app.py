import azure.functions as func
import json
import logging
import os
import uuid
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

COSMOS_DB_CONNECTION_STRING = os.environ.get("CosmosDBConnection")
client = CosmosClient.from_connection_string(COSMOS_DB_CONNECTION_STRING)
database = client.get_database_client("exercicio1-db")
container = database.get_container_client("items")

@app.route(route="items", methods=["GET", "POST"])
def handle_items(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == 'POST':
        try:
            req_body = req.get_json()
            item_id = str(uuid.uuid4())
            item = {
                'id': item_id,
                'name': req_body.get('name', 'Unknown'),
                'description': req_body.get('description', '')
            }
            container.upsert_item(item)
            return func.HttpResponse(json.dumps({'message': 'Item created', 'id': item_id}), status_code=201, mimetype="application/json")
        except ValueError:
            return func.HttpResponse("Invalid body", status_code=400)

    elif req.method == 'GET':
        items = list(container.read_all_items())
        return func.HttpResponse(json.dumps(items), status_code=200, mimetype="application/json")

    return func.HttpResponse("Method not allowed", status_code=405)
