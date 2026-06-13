import functions_framework
from google.cloud import firestore
import json
import uuid

db = firestore.Client()

@functions_framework.http
def handle_items(request):
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        item_id = str(uuid.uuid4())
        doc_ref = db.collection('items').document(item_id)
        item = {
            'id': item_id,
            'name': request_json.get('name', 'Unknown'),
            'description': request_json.get('description', '')
        }
        doc_ref.set(item)
        return json.dumps({'message': 'Item created', 'id': item_id}), 201, {'Content-Type': 'application/json'}
    
    elif request.method == 'GET':
        items_ref = db.collection('items')
        docs = items_ref.stream()
        items = [doc.to_dict() for doc in docs]
        return json.dumps(items), 200, {'Content-Type': 'application/json'}
    
    return json.dumps({'message': 'Method not allowed'}), 405, {'Content-Type': 'application/json'}
