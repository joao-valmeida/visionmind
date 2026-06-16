import json
import pytest
from unittest.mock import MagicMock, patch

# Patch firestore Client before import
with patch('google.cloud.firestore.Client') as mock_firestore:
    from main import handle_items

@pytest.fixture
def mock_db():
    with patch('main.db') as mock:
        yield mock

def test_handle_items_get(mock_db):
    # Mock stream data
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {"id": "g1", "name": "GCP Item"}
    mock_db.collection.return_value.stream.return_value = [mock_doc]
    
    # Mock request
    request = MagicMock()
    request.method = 'GET'
    
    resp_body, status_code, headers = handle_items(request)
    
    assert status_code == 200
    assert json.loads(resp_body) == [{"id": "g1", "name": "GCP Item"}]

def test_handle_items_post(mock_db):
    # Mock request
    request = MagicMock()
    request.method = 'POST'
    request.get_json.return_value = {"name": "Test GCP", "description": "Testing Google Cloud"}
    
    # Mock firestore methods
    mock_doc_ref = MagicMock()
    mock_db.collection.return_value.document.return_value = mock_doc_ref
    
    resp_body, status_code, headers = handle_items(request)
    
    assert status_code == 201
    body = json.loads(resp_body)
    assert body["message"] == "Item created"
    assert "id" in body
    
    # Verify firestore calls
    mock_db.collection.assert_called_with('items')
    mock_doc_ref.set.assert_called_once()
