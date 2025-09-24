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
