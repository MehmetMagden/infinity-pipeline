from flask import Flask, jsonify, render_template
import os
import psycopg2

app = Flask(__name__)

# Database connection configuration using environment variables
DB_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # Establishes connection to the PostgreSQL container
    conn = psycopg2.connect(DB_URL)
    return conn

@app.route('/')
def home():
    # Renders the professional project dashboard
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Fetch all tasks from the PostgreSQL database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks;')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

if __name__ == '__main__':
    # Running the Flask app on the internal container port
    app.run(host='0.0.0.0', port=5000)