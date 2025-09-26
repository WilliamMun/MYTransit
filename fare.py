import pandas as pd
from lib import bfs_route  # Import custom BFS route-finding function

# Load station data from CSV
# cp1252 encoding is used for compatibility with special characters
df = pd.read_csv("station_info.csv", encoding="cp1252")

# Strip whitespace from column headers (e.g. " station_id " → "station_id")
df.columns = df.columns.str.strip()


def calculate_fare(start_id, end_id):
    """
    Calculate the fare and total travel distance between two stations.
    
    Parameters:
        start_id (int or str): Station ID of the starting station.
        end_id (int or str): Station ID of the destination station.

    Returns:
        tuple: (fare, total_distance)
            fare (float) → calculated ticket fare in RM
            total_distance (float) → total travel distance in km
    """

    # Find path between start and end station using BFS (ensures shortest path by hops)
    path = bfs_route(start_id, end_id)

    # If no valid path is found, return zeros
    if not path or len(path) < 2:
        return 0.0, 0.0

    # Initialize total travel distance
    total_distance = 0.0

    # Iterate over station pairs along the path
    for i in range(len(path) - 1):
        sid1, sid2 = path[i], path[i + 1]

        try:
            # Get row info for current and next station
            row1 = df[df["station_id"] == sid1].iloc[0]
            row2 = df[df["station_id"] == sid2].iloc[0]

            # Distance is stored in "distance" column of the CSV
            dist1 = float(row1["distance"])
            dist2 = float(row2["distance"])

            # Accumulate absolute distance difference between stations
            total_distance += abs(dist2 - dist1)

        except Exception as e:
            # Catch errors (e.g., station not found in CSV) and log them
            print(f"Error reading distance between {sid1} and {sid2}: {e}")

    # Fare calculation model
    base_fare = 1.20     # Fixed starting charge (minimum fare)
    per_km = 0.15        # Charge per km traveled

    # Final fare = base fare + distance charge
    fare = base_fare + (total_distance * per_km)

    # Round results for neat output (fare to 2 dp, distance to 1 dp)
    return round(fare, 2), round(total_distance, 1)