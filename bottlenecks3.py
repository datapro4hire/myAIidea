import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

def parse_log_file(file):
    tasks = []
    current_date = None
    
    # Read lines from the file
    lines = file.getvalue().decode().split('\n') if hasattr(file, 'getvalue') else file.readlines()
    
    for line in lines:
        # Ensure line is a string
        if isinstance(line, bytes):
            line = line.decode()
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
                st.warning(f"Error parsing line: {line}\nError: {str(e)}")
                continue
    
    if not tasks:
        st.warning("No valid data found in the file")
        return pd.DataFrame()  # Return empty DataFrame instead of None
    
    return pd.DataFrame(tasks)

# [Rest of your existing code remains the same...]