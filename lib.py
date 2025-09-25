import sys
import time
import csv
import pandas as pd

def typewriter_effect(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)  #Print every character at the same line 
        sys.stdout.flush() #Immediately print out the text 
        time.sleep(delay) #Small delay after printed each line
    print()  

def welcome_message():
    text_lines = ["------------------------------------------------------------",
                  "Welcome to MYTransit!",
                  "------------------------------------------------------------"]
    for line in text_lines:
        typewriter_effect(line)
        time.sleep(0.3)

def display_station():
    df = pd.read_csv("station_info.csv", encoding="cp1252")
    df.columns = df.columns.str.strip()
    df_clean = df[["station_id", "station_name", "type_of_train"]]
    df_clean = df_clean.drop_duplicates(subset=["station_name"])
    df_clean["formatted"] = df_clean["station_id"].astype(str) + ": " + df_clean["type_of_train"] + "- " + df_clean["station_name"]
    station_list = df_clean["formatted"].tolist()
    for station in station_list:
        print(station)

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