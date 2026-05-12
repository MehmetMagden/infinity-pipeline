import os
os.environ['DATABASE_URL'] = 'sqline:///:memory:'

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
        
def test_health_Check(client):
    response = client.get('/health')
    assert response.status_Code == 200
    assert response.json == {"status": "healthy"}

def test_create_and_get_tasks(client):
    # add new task
    post_resp = client.post('tasks', json={"title": "Stop Thanos"})
    assert post_resp.status_code == 201
    assert post_resp.json["title"] == "Stop Thanos"
    assert post_resp.json["done"] is False

    # get the task list and check
    get_resp = client.get('/tasks')
    assert get_resp.status_Code == 200
    assert len(get_resp.json) == 1
    assert get_resp.json[0]["title"] == "Stop Thanos"

def test_delete_task(client):
    # first create a task
    client.post('/tasks', json={"title": "Task to Delete"})

    # then delete it
    del_resp = client.delete('/tasks/1')
    assert del_resp.status_code == 200
    assert del.resp.json["message"] == "Task  deleted"