import csv

def get_station_schedule_by_id(station_id):
    file_path = r"c:\Users\User\OneDrive\Desktop\MyTransit\MYTransit\station_info.csv"
    
    try:
        with open(file_path, newline="", encoding='latin-1') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    row_id = int(row["station_id"])
                except ValueError:
                    continue

                if row_id == station_id:
                    name = row["station_name"]
                    starting_time = row["starting time"]
                    frequency = row["frequency"]
                    return (
                        f"Station ID: {station_id} ({name})\n"
                        f"Starting Time: {starting_time}\n"
                        f"Frequency: {frequency} minutes"
                    )
                    
        return f"Station ID '{station_id}' not found."
        
    except Exception as e:
        return f"Error reading file: {e}"


if __name__ == "__main__":
    try:
        user_input_raw = input("Enter Station ID: ")
        user_input = int(user_input_raw.strip())
        print(get_station_schedule_by_id(user_input))
    except ValueError:
        print("Please enter a valid number for Station ID.")