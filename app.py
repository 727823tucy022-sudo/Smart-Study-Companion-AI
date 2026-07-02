import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from config import config
from predict import StudyPredictor

app = Flask(__name__)
app.config.from_object(config)

def init_sqlite_database():
    """Builds historical persistent ledger data-stores safely."""
    conn = sqlite3.connect(config.DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            sleep_hours REAL NOT NULL,
            study_hours REAL NOT NULL,
            stress_level INTEGER NOT NULL,
            mood INTEGER NOT NULL,
            break_count INTEGER NOT NULL,
            productivity_level TEXT NOT NULL,
            confidence REAL NOT NULL,
            suggestions TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run database setup context
init_sqlite_database()

# Core Navigation Controllers
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Operational Inquiry Sent! Our operations team will process your response.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Input extraction and explicit data parsing validation mapping
            sleep_hours = float(request.form.get('sleep_hours', 0))
            study_hours = float(request.form.get('study_hours', 0))
            stress_level = int(request.form.get('stress_level', 1))
            mood = int(request.form.get('mood', 2))
            break_count = int(request.form.get('break_count', 0))
            
            # Boundary checks
            if not (0 <= sleep_hours <= 24) or not (0 <= study_hours <= 24):
                flash("Operational Failure: Time inputs must reside in legal diurnal configurations (0-24 hrs).", "danger")
                return redirect(url_for('predict'))
                
            predictor = StudyPredictor()
            results = predictor.infer_productivity(sleep_hours, study_hours, stress_level, mood, break_count)
            
            # Persist evaluation records to database
            conn = sqlite3.connect(config.DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO prediction_history 
                (timestamp, sleep_hours, study_hours, stress_level, mood, break_count, productivity_level, confidence, suggestions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                sleep_hours, study_hours, stress_level, mood, break_count,
                results['productivity_level'], results['confidence'],
                json.dumps(results['suggestions'])
            ))
            conn.commit()
            conn.close()
            
            # Pack current runtime metrics into view return context
            payload = {
                'sleep_hours': sleep_hours,
                'study_hours': study_hours,
                'stress_level': stress_level,
                'mood': mood,
                'break_count': break_count,
                **results
            }
            return render_template('predict.html', result=payload)
            
        except Exception as err:
            flash(f"Data ingestion pipeline execution failure: {str(err)}", "danger")
            return redirect(url_for('predict'))
            
    return render_template('predict.html', result=None)

@app.route('/dashboard')
def dashboard():
    """Compiles analytic models metadata configurations alongside historical structural updates."""
    meta_path = os.path.join(config.MODEL_DIR, 'model_metadata.json')
    meta_stats = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as file:
            meta_stats = json.load(file)
            
    # Gather aggregate database counts
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM prediction_history")
    total_predictions = cursor.fetchone()['total']
    
    cursor.execute("SELECT AVG(confidence) as avg_conf FROM prediction_history")
    avg_confidence = cursor.fetchone()['avg_conf'] or 0.0
    
    conn.close()
    
    summary = {
        'total_predictions': total_predictions,
        'avg_confidence': round(avg_confidence, 2),
        'winning_model': meta_stats.get('winning_model', 'Random Forest'),
        'metrics_log': meta_stats.get('metrics', {})
    }
    
    return render_template('dashboard.html', summary=summary)

# RESTful History Persistence Interfaces
@app.route('/api/history', methods=['GET'])
def get_history_api():
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prediction_history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    history_list = []
    for row in rows:
        history_list.append({
            'id': row['id'],
            'timestamp': row['timestamp'],
            'sleep_hours': row['sleep_hours'],
            'study_hours': row['study_hours'],
            'stress_level': row['stress_level'],
            'mood': row['mood'],
            'break_count': row['break_count'],
            'productivity_level': row['productivity_level'],
            'confidence': row['confidence'],
            'suggestions': json.loads(row['suggestions'])
        })
    return jsonify(history_list)

@app.route('/api/history/delete/<int:record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    try:
        conn = sqlite3.connect(config.DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prediction_history WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Record {record_id} pruned successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)