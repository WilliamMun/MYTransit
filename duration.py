import csv
from datetime import datetime, timedelta

# Function to get the next train time for a given station ID
def get_next_train_time(station_id):
    file_path = r"station_info.csv"   # Path to the CSV file containing station data
    
    try:
        # Get current device time and full datetime
        current_time = datetime.now().time()
        current_datetime = datetime.now()
        
        # Open the CSV file in read mode
        with open(file_path, newline="", encoding='latin-1') as f:
            reader = csv.DictReader(f)   # Read rows as dictionaries (column_name → value)
            
            # Loop through each row (station) in the CSV
            for row in reader:
                try:
                    row_id = int(row["station_id"])   # Convert station_id column to integer
                except ValueError:
                    continue   # Skip row if station_id is invalid (e.g., not a number)

                # Check if the current row matches the requested station_id
                if row_id == station_id:
                    name = row["station_name"]   # Get station name
                    starting_time_str = row["starting time"]   # First train starting time (string)
                    frequency = int(row["frequency"])   # Frequency (minutes) between trains
                    
                    # Parse the starting time string into a datetime.time object
                    try:
                        starting_time = datetime.strptime(starting_time_str, '%H%M').time()
                    except ValueError:
                        # Handle wrong time format (e.g., not HHMM format)
                        return f"Error: Invalid time format '{starting_time_str}' for station {station_id}"
                    
                    # Calculate the next train time based on current time, first train, and frequency
                    next_train_time = calculate_next_train(current_time, starting_time, frequency)
                    
                    # Format the output message with station info and train timing
                    return (
                        f"Station ID: {station_id} ({name})\n"
                        f"Current Time: {current_time.strftime('%H:%M')}\n"
                        f"Next Train: {next_train_time.strftime('%H:%M')}\n"
                        f"Frequency: Every {frequency} minutes"
                    )
                    
        # If no matching station_id was found in CSV
        return f"Station ID '{station_id}' not found."
        
    except Exception as e:
        # Catch errors like file not found or read issues
        return f"Error reading file: {e}"

# Helper function to calculate next train arrival time
def calculate_next_train(current_time, first_train_time, frequency_minutes):
    """Calculate the next train arrival time based on frequency and current time"""
    
    # Get the current full datetime (date + time)
    current_datetime = datetime.now()
    
    # Combine today's date with the first train's time
    first_train_datetime = datetime.combine(current_datetime.date(), first_train_time)
    
    # If the first train hasn’t started yet today, return the first train time
    if current_datetime < first_train_datetime:
        return first_train_datetime
    
    # Calculate minutes passed since the first train departed
    minutes_since_first_train = (current_datetime - first_train_datetime).total_seconds() / 60
    
    # Determine how many train intervals have already passed
    intervals_passed = minutes_since_first_train // frequency_minutes
    
    # Compute when the next train will arrive by adding one more interval
    next_train_minutes = (intervals_passed + 1) * frequency_minutes
    next_train_datetime = first_train_datetime + timedelta(minutes=next_train_minutes)
    
    # Return the datetime of the next train
    return next_train_datetime