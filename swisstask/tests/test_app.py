import pytest
from unittest.mock import patch
import sys
import os

# Add the app directory to the system path so Python can find it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Now we can safely import app (without db!)
from app import app

@pytest.fixture
def client():
    # Configure the Flask app for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    # Ensure the frontend dashboard loads with 200 OK
    response = client.get('/')
    assert response.status_code == 200
    assert b"Infinity Pipeline" in response.data

@patch('app.get_db_connection')
def test_get_tasks(mock_get_db_connection, client):
    # Mock the PostgreSQL connection and cursor
    mock_conn = mock_get_db_connection.return_value
    mock_cur = mock_conn.cursor.return_value
    
    # Simulate data coming from the database
    mock_cur.fetchall.return_value = [
        (1, "Install Kubernetes", True),
        (2, "Setup Cloudflare Tunnel", False)
    ]

    # Call the API
    response = client.get('/tasks')
    
    assert response.status_code == 200
    assert b"Setup Cloudflare Tunnel" in response.data