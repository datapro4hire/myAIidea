import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

def parse_log_file(file):
    tasks = []
    current_date = None
    
    for line in file:
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
                print(f"Error parsing line: {line}")
                continue
    
    return pd.DataFrame(tasks)

def create_sankey_diagram():
    # Define nodes and links for Sankey diagram
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
            source = [0, 0, 0, 0, 4, 5, 6], # indices correspond to nodes
            target = [1, 2, 3, 4, 5, 6, 7],
            value = [1, 1, 1, 1, 4, 3, 2]  # flow values
        )
    )])

    fig.update_layout(title_text="Warehouse Material Flow", font_size=10)
    return fig

def show_bottlenecks(df):
    st.subheader("Common Bottlenecks")
    
    # Interactive bottleneck selection
    bottleneck_type = st.selectbox(
        "Select Bottleneck Category",
        ["Equipment", "Traffic", "Processing", "Temperature Control"]
    )

    if bottleneck_type == "Equipment":
        st.write("Equipment Related Delays:")
        st.metric("Average Printer Delay", "15-20 min")
        st.metric("Equipment Search Time", "15-30 min")

    elif bottleneck_type == "Traffic":
        st.write("Traffic Related Delays:")
        st.metric("Peak Hours", "11:30-14:30")
        st.metric("Average Congestion Delay", "10-15 min")

def show_zone_analysis(df):
    st.subheader("Zone Performance Metrics")
    
    # Zone selection
    zone = st.selectbox("Select Zone", ["Zone A", "Zone B", "Zone C", "Zone F"])
    
    if zone == "Zone A":
        st.metric("Processing Rate", "120-150 items/hr")
    elif zone == "Zone B":
        st.metric("Processing Rate", "40-60 items/hr")
        st.metric("Average Load", "300-600 lbs/cart")

def show_time_analysis(df):
    st.write("Task Duration Analysis")
    st.dataframe(df)

def create_app():
    st.title("Warehouse Workflow Analysis")

    # File uploader in sidebar
    st.sidebar.header("Data Input")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your log file", 
        type=['txt'],
        help="Upload a text file containing warehouse logs"
    )

    if uploaded_file is not None:
        try:
            # Read the uploaded file content
            content = uploaded_file.getvalue().decode()
            
            # Convert content to DataFrame using StringIO
            df = parse_log_file(StringIO(content))
            
            st.sidebar.success(f"Successfully loaded {len(df)} records!")
            
            # Show data preview option
            if st.sidebar.checkbox("Show Raw Data"):
                st.subheader("Raw Data Preview")
                st.dataframe(df.head())

            # Continue with the rest of your app...
            show_analysis(df)
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return
    else:
        st.info("Please upload a log file to begin analysis")
        return

def show_analysis(df):
    # Sidebar for controls
    view_type = st.sidebar.selectbox(
        "Select View",
        ["Overview", "Bottlenecks", "Zone Analysis", "Time Analysis"]
    )

    if view_type == "Overview":
        st.header("Warehouse Process Flow")
        fig = create_sankey_diagram()
        st.plotly_chart(fig)

    elif view_type == "Bottlenecks":
        st.header("Bottleneck Analysis")
        show_bottlenecks(df)

    elif view_type == "Zone Analysis":
        st.header("Zone Performance")
        show_zone_analysis(df)

    elif view_type == "Time Analysis":
        st.header("Time Analysis")
        show_time_analysis(df)

if __name__ == "__main__":
    create_app()