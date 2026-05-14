import pytest
from unittest.mock import patch
import sys
import os

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app import app

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    # Test if the professional dashboard loads correctly
    response = client.get('/')
    assert response.status_code == 200
    # Check if our new HTML content is present
    assert b"Infinity Pipeline" in response.data

@patch('app.get_db_connection')
def test_get_tasks(mock_get_db_connection, client):
    # Mock the database connection to avoid needing a real DB during CI tests
    mock_conn = mock_get_db_connection.return_value
    mock_cur = mock_conn.cursor.return_value
    
    # Simulate the data that PostgreSQL would return
    mock_cur.fetchall.return_value = [
        (1, "Install Kubernetes", True),
        (2, "Setup Cloudflare Tunnel", False)
    ]

    # Hit the /tasks endpoint
    response = client.get('/tasks')
    
    assert response.status_code == 200
    # Verify the mocked data is returned in the JSON response
    assert b"Setup Cloudflare Tunnel" in response.data