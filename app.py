from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Directory to store received data
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def index():
    # Get list of all clients
    clients = []
    if os.path.exists(DATA_DIR):
        for client_id in os.listdir(DATA_DIR):
            if os.path.isdir(os.path.join(DATA_DIR, client_id)):
                clients.append(client_id)
    return render_template('index.html', clients=clients)

@app.route('/client/<client_id>')
def client_details(client_id):
    client_dir = os.path.join(DATA_DIR, client_id)
    if not os.path.exists(client_dir):
        return "Client not found", 404
    
    # Get all log files for this client
    logs = []
    for filename in os.listdir(client_dir):
        if filename.endswith('.json'):
            with open(os.path.join(client_dir, filename), 'r') as f:
                data = json.load(f)
                logs.append({
                    'timestamp': data.get('timestamp', 'Unknown'),
                    'filename': filename,
                    'type': data.get('type', 'Unknown')
                })
    
    # Sort logs by timestamp (newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('client.html', client_id=client_id, logs=logs)

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        # Get client identifier or generate one
        client_id = request.form.get('client_id', str(uuid.uuid4()))
        data_type = request.form.get('type', 'unknown')
        
        # Create client directory if it doesn't exist
        client_dir = os.path.join(DATA_DIR, client_id)
        if not os.path.exists(client_dir):
            os.makedirs(client_dir)
        
        # Create timestamp and filename
        timestamp = datetime.now().isoformat()
        filename = f"{data_type}_{timestamp.replace(':', '-')}.json"
        file_path = os.path.join(client_dir, filename)
        
        # Save uploaded data
        data = {
            'timestamp': timestamp,
            'type': data_type,
            'content': request.form.get('content', ''),
            'system_info': request.form.get('system_info', ''),
        }
        
        # Save attached files if any
        for key in request.files:
            file = request.files[key]
            file_save_path = os.path.join(client_dir, f"{key}_{timestamp.replace(':', '-')}_{file.filename}")
            file.save(file_save_path)
            data[f'file_{key}'] = file_save_path
        
        # Save the data
        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        return jsonify({
            'success': True, 
            'client_id': client_id,
            'message': 'Data received successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/log/<client_id>/<log_file>')
def get_log(client_id, log_file):
    log_path = os.path.join(DATA_DIR, client_id, log_file)
    if not os.path.exists(log_path):
        return jsonify({'error': 'Log not found'}), 404
    
    with open(log_path, 'r') as f:
        data = json.load(f)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
