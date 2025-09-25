import pandas as pd
from lib import bfs_route  

# Load station data
df = pd.read_csv("station_info.csv", encoding="cp1252")
df.columns = df.columns.str.strip()

def calculate_fare(start_id, end_id):
    """
    Calculate total distance and fare between two stations.
    Returns (fare, total_distance).
    """
    path = bfs_route(start_id, end_id)
    if not path or len(path) < 2:
        return 0.0, 0.0

    total_distance = 0.0

    for i in range(len(path) - 1):
        sid1, sid2 = path[i], path[i + 1]
        try:
            row1 = df[df["station_id"] == sid1].iloc[0]
            row2 = df[df["station_id"] == sid2].iloc[0]

            dist1 = float(row1["distance"])
            dist2 = float(row2["distance"])
            total_distance += abs(dist2 - dist1)
        except Exception as e:
            print(f"Error reading distance between {sid1} and {sid2}: {e}")

    # Example fare rule (distance-based)
    base_fare = 1.20
    per_km = 0.15
    fare = base_fare + (total_distance * per_km)

    return round(fare, 2), round(total_distance, 1)
