import os
import json
import pytest
import boto3
from moto import mock_aws

# Set environment variables before importing the handler
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["DYNAMODB_TABLE"] = "test-table"

from lambda_function import lambda_handler

@pytest.fixture
def dynamodb_mock():
    with mock_aws():
        conn = boto3.resource("dynamodb", region_name="us-east-1")
        conn.create_table(
            TableName="test-table",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        yield conn

def test_lambda_handler_get(dynamodb_mock):
    event = {
        "path": "/items",
        "httpMethod": "GET"
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == []

def test_lambda_handler_post(dynamodb_mock):
    event = {
        "path": "/items",
        "httpMethod": "POST",
        "body": json.dumps({"name": "Test Item", "description": "This is a test"})
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["message"] == "Item created"
    assert "id" in body
