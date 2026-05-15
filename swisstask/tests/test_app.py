import pytest
from app.app import app, db, Task

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    # Use a volatile, in-memory database specifically for tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            # Create the mock tables based on our SQLAlchemy models
            db.create_all()
            yield client
            # Clean up after the tests are done
            db.session.remove()
            db.drop_all()
            
def test_home(client):
    """Test if portfolio home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    
    
def test_Get_tasks(client):    
    """Test if the API retrieves tasks correctly using the ORM"""
    # Inject mock data into our test database using the ORM
    with app.app_context():
        task1 = Task(title="Deploy K8s Cluster", completed=True)
        task2 = Task(title="Fix Pytest Suite", completed=False)
        db.session.add(task1)
        db.session.add(task2)
        db.session.commit()
        
    # Call the ApI endpoint
    response = client.get('/tasks')

    # Verify the response
    assert response.status_code == 200
    data = response.get_json()
    
    assert len(data) == 2
    assert data [0]['title'] == "Deploy K8s Cluster" 
    assert data[0]['completed'] is True
    assert data[1]['title'] == "Fix Pytest Suite"
    assert data[1]['completed'] is False