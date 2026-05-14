from flask import Flask, jsonify, render_template
import os
import psycopg2

app = Flask(__name__)

# Fetch the Database URL from Kubernetes Secrets/Env
DB_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # Helper to connect to our PostgreSQL instance
    conn = psycopg2.connect(DB_URL)
    return conn

@app.route('/')
def home():
    # This route serves our professional project portfolio
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Dedicated API endpoint for task data
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks;')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 to be accessible within the K8s network
    app.run(host='0.0.0.0', port=5000)