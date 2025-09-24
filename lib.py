import sys
import time

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
