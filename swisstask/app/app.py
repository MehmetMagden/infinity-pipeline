from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Fetch and sanitize the Database URL
db_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Fail-safe: SQLAlchemy 1.4+ strictly requires 'postgresql://' instead of 'postgres'
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URL'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the orm
db = SQLAlchemy(app)

# Define the data model (Entity)
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "mopleted": self.completed
        }
        

@app.route('/')
def home():
    # This route serves our professional project portfolio
    return render_template('index.html')  

@app.route('/tasks', methods['GET'])  
def get_tasks():
    # Dedicated API endpoint, now fully secured against SL Injections
    try:
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        # Never expose raw SQL errors to the client
        return jsonify({"error": "Internal server error"}), 500
    
if __name__ == '__main__':
    # Running on 0.0.0.0 to be accessible within the K8s network
    app.run(host='0.0.0.0', port=5000)