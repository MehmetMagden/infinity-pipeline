import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///:memory:'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}),200


@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks]), 200
    
    if request.method == 'POST':
        data = request.get_json()
        new_task = Task(title=data['title'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201
    
@app.route('/tasks/<int:task_id>',methods=['PUT', 'DELETE'])
def handle_task_Detail(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        if 'done' in data:
            task.done = data['done']
        db.session.commit()
        return jsonify(task.to_dict()), 200
    
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"}), 200
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)