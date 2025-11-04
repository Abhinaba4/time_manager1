from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# --- Database Models ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_time = db.Column(db.Float)  # in minutes

# --- Routes ---
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/start', methods=['POST'])
def start_task():
    name = request.form['task_name']
    new_task = Task(name=name, start_time=datetime.now())
    db.session.add(new_task)
    db.session.commit()
    flash(f"Started task: {name}")
    return redirect(url_for('index'))

@app.route('/stop/<int:id>')
def stop_task(id):
    task = Task.query.get(id)
    task.end_time = datetime.now()
    task.total_time = round((task.end_time - task.start_time).total_seconds() / 60, 2)
    db.session.commit()
    flash(f"Stopped task: {task.name} ({task.total_time} min)")
    return redirect(url_for('index'))

@app.route('/report')
def report():
    tasks = Task.query.all()
    total = sum(t.total_time or 0 for t in tasks)
    return render_template('report.html', tasks=tasks, total=total)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
