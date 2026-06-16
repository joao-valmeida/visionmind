import os
import json
import pytest
from unittest.mock import MagicMock, patch

# Set dummy environment variable for initialization
os.environ["CosmosDBConnection"] = "AccountEndpoint=https://local.documents.azure.com:443/;AccountKey=dummy;"

# Mock CosmosClient before importing the app to avoid connection errors
with patch('azure.cosmos.CosmosClient.from_connection_string') as mock_cosmos:
    import azure.functions as func
    from function_app import handle_items

@pytest.fixture
def mock_container():
    with patch('function_app.container') as mock:
        yield mock

def test_handle_items_get(mock_container):
    # Mock data
    mock_container.read_all_items.return_value = [{"id": "1", "name": "Item 1"}]
    
    # Create mock request
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/items'
    )
    
    resp = handle_items(req)
    
    assert resp.status_code == 200
    assert json.loads(resp.get_body()) == [{"id": "1", "name": "Item 1"}]

def test_handle_items_post(mock_container):
    # Create mock request
    req = func.HttpRequest(
        method='POST',
        body=json.dumps({"name": "Test Azure", "description": "Testing Azure"}).encode('utf-8'),
        url='/api/items'
    )
    
    resp = handle_items(req)
    
    assert resp.status_code == 201
    body = json.loads(resp.get_body())
    assert body["message"] == "Item created"
    assert "id" in body
    
    # Verify container was called
    mock_container.upsert_item.assert_called_once()
