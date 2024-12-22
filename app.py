from flask import Flask, request, jsonify
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

app = Flask(__name__)

def parse_log_file(file_content):
    tasks = []
    current_date = None
    
    for line in file_content.split('\n'):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check if line is a date
        if line.startswith(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')):
            current_date = line
            continue
        
        # Parse task lines
        if '=' in line and '@' in line:
            try:
                # Split task info and notes
                task_info, *notes = line.split('*')
                notes = notes[0] if notes else ''
                
                # Split quantity and time
                task_part, time_part = task_info.split('@')
                
                # Parse task type and quantity
                task_type, quantity = task_part.split('=')
                task_type = task_type.strip()
                quantity = quantity.strip()
                
                # Parse start and end times
                if '-' in time_part:
                    start_time, end_time = time_part.strip().split('-')
                else:
                    start_time = time_part.strip()
                    end_time = ''
                
                tasks.append({
                    'date': current_date,
                    'task_type': task_type,
                    'quantity': quantity,
                    'start_time': start_time,
                    'end_time': end_time,
                    'notes': notes.strip()
                })
            except Exception as e:
                print(f"Error parsing line: {line}")
                continue
    
    return pd.DataFrame(tasks)

def create_sankey_diagram():
    nodes = ['Receiving', 'Zone A', 'Zone B', 'Zone C', 'Zone F', 'Picking', 'Batching', 'Outbound']
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = nodes,
            color = "blue"
        ),
        link = dict(
            source = [0, 0, 0, 0, 4, 5, 6],
            target = [1, 2, 3, 4, 5, 6, 7],
            value = [1, 1, 1, 1, 4, 3, 2]
        )
    )])

    fig.update_layout(title_text="Warehouse Material Flow", font_size=10)
    return fig.to_json()

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        content = file.read().decode('utf-8')
        df = parse_log_file(content)
        return jsonify({
            'message': f'Successfully loaded {len(df)} records!',
            'data': df.to_dict(orient='records')
        })

@app.route('/api/sankey', methods=['GET'])
def get_sankey():
    return jsonify(create_sankey_diagram())

@app.route('/api/bottlenecks', methods=['GET'])
def get_bottlenecks():
    bottleneck_type = request.args.get('type', 'Equipment')
    if bottleneck_type == "Equipment":
        return jsonify({
            'title': 'Equipment Related Delays:',
            'metrics': [
                {'label': 'Average Printer Delay', 'value': '15-20 min'},
                {'label': 'Equipment Search Time', 'value': '15-30 min'}
            ]
        })
    elif bottleneck_type == "Traffic":
        return jsonify({
            'title': 'Traffic Related Delays:',
            'metrics': [
                {'label': 'Peak Hours', 'value': '11:30-14:30'},
                {'label': 'Average Congestion Delay', 'value': '10-15 min'}
            ]
        })
    else:
        return jsonify({'error': 'Invalid bottleneck type'}), 400

@app.route('/api/zone', methods=['GET'])
def get_zone_analysis():
    zone = request.args.get('zone', 'Zone A')
    if zone == "Zone A":
        return jsonify({
            'metrics': [
                {'label': 'Processing Rate', 'value': '120-150 items/hr'}
            ]
        })
    elif zone == "Zone B":
        return jsonify({
            'metrics': [
                {'label': 'Processing Rate', 'value': '40-60 items/hr'},
                {'label': 'Average Load', 'value': '300-600 lbs/cart'}
            ]
        })
    else:
        return jsonify({'error': 'Invalid zone'}), 400

if __name__ == '__main__':
    app.run(debug=True)