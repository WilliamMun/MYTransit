import csv
from datetime import datetime, timedelta

def get_next_train_time(station_id):
    file_path = r"c:\Users\User\OneDrive\Desktop\MyTransit\MYTransit\station_info.csv"
    
    try:
        # Get current device time
        current_time = datetime.now().time()
        current_datetime = datetime.now()
        print(f"Current time: {current_time.strftime('%H:%M')}")
        
        with open(file_path, newline="", encoding='latin-1') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    row_id = int(row["station_id"])
                except ValueError:
                    continue

                if row_id == station_id:
                    name = row["station_name"]
                    starting_time_str = row["starting time"]
                    frequency = int(row["frequency"])
                    
                    # Parse starting time
                    try:
                        starting_time = datetime.strptime(starting_time_str, '%H%M').time()
                    except ValueError:
                        return f"Error: Invalid time format '{starting_time_str}' for station {station_id}"
                    
                    # Calculate next train time
                    next_train_time = calculate_next_train(current_time, starting_time, frequency)
                    
                    # Format the output
                    return (
                        f"Station ID: {station_id} ({name})\n"
                        f"Current Time: {current_time.strftime('%H:%M')}\n"
                        f"Next Train: {next_train_time.strftime('%H:%M')}\n"
                        f"Frequency: Every {frequency} minutes"
                    )
                    
        return f"Station ID '{station_id}' not found."
        
    except Exception as e:
        return f"Error reading file: {e}"

def calculate_next_train(current_time, first_train_time, frequency_minutes):
    """Calculate the next train arrival time"""
    # Get current datetime with today's date
    current_datetime = datetime.now()
    
    # Create datetime objects for comparison
    first_train_datetime = datetime.combine(current_datetime.date(), first_train_time)
    
    # If the first train hasn't started yet today, return first train time
    if current_datetime < first_train_datetime:
        return first_train_datetime
    
    # Calculate how many minutes have passed since first train
    minutes_since_first_train = (current_datetime - first_train_datetime).total_seconds() / 60
    
    # Calculate how many frequency intervals have passed
    intervals_passed = minutes_since_first_train // frequency_minutes
    
    # Calculate next train time
    next_train_minutes = (intervals_passed + 1) * frequency_minutes
    next_train_datetime = first_train_datetime + timedelta(minutes=next_train_minutes)
    
    return next_train_datetime

if __name__ == "__main__":
    try:
        user_input_raw = input("Enter Station ID: ")
        user_input = int(user_input_raw.strip())
        print("\n" + "="*40)
        result = get_next_train_time(user_input)
        print(result)
        print("="*40)
    except ValueError:
        print("Please enter a valid number for Station ID.")

import pandas as pd
from collections import deque

# Load station data
df = pd.read_csv("station_info.csv", encoding="cp1252")
df.columns = df.columns.str.strip()

# Build graph
graph = {}
station_lines = {}  # keep track of which line each station belongs to

for _, row in df.iterrows():
    sid = int(row["station_id"])
    name = row["station_name"].strip()
    line = row["line"].strip()

    station_lines[sid] = line

    if sid not in graph:
        graph[sid] = []

    # connect consecutive stations (same line)
    if sid > 1 and df.iloc[sid-2]["line"] == line:  
        prev_sid = int(df.iloc[sid-2]["station_id"])
        graph[sid].append(prev_sid)
        graph[prev_sid].append(sid)

    # connect interchange stations
    if pd.notna(row["interchange"]):
        for conn in str(row["interchange"]).split(","):
            conn = conn.strip()
            if conn.isdigit():
                conn_id = int(conn)
                graph[sid].append(conn_id)

    # connect “connecting” column
    if pd.notna(row["connecting"]):
        for conn in str(row["connecting"]).split(","):
            conn = conn.strip()
            if conn.isdigit():
                conn_id = int(conn)
                graph[sid].append(conn_id)

def bfs_route(start, end):
    """Find shortest path from start to end using BFS"""
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        visited.add(current)
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None

def suggest_route(start_id, end_id):
    path = bfs_route(start_id, end_id)
    if not path:
        return "No route found."

    output = []
    prev_line = None
    for i, sid in enumerate(path):
        station = df[df["station_id"] == sid].iloc[0]
        name = station["station_name"]
        line = station["line"]

        # detect interchange
        if prev_line and prev_line != line:
            output.append(f"--- Interchange at {name} ({prev_line} → {line}) ---")

        output.append(f"{name} [{line}]")
        prev_line = line

    return "\n".join(output)

if __name__ == "__main__":
    start = int(input("Enter starting station ID: "))
    end = int(input("Enter destination station ID: "))
    print("\nSuggested Route:\n")
    print(suggest_route(start, end))
