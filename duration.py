import csv
from datetime import datetime, timedelta

def get_next_train_time(station_id):
    file_path = r"station_info.csv"
    
    try:
        # Get current device time
        current_time = datetime.now().time()
        current_datetime = datetime.now()
        
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