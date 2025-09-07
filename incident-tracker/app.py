from flask import Flask, render_template, request, redirect
import sqlite3
import os
from prometheus_client import start_http_server, Counter

app = Flask(__name__)
DB_PATH = 'incidents.db'

# Prometheus Counter
incident_counter = Counter('incident_created_total', 'Total incidents created')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS incidents (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            status TEXT NOT NULL DEFAULT 'Open'
                        )''')

@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        incidents = conn.execute("SELECT * FROM incidents").fetchall()
    return render_template('index.html', incidents=incidents)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO incidents (title, status) VALUES (?, 'Open')", (title,))
    incident_counter.inc()  # Prometheus metric increment
    return redirect('/')

@app.route('/resolve/<int:id>')
def resolve(id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE incidents SET status='Resolved' WHERE id=?", (id,))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    start_http_server(9100)  # ✅ expose metrics internally
    app.run(host='0.0.0.0', port=5000)
