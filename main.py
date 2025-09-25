import lib
import duration
from fare import calculate_fare
import time

#1: Welcome message 
lib.welcome_message()

while True:
    #2: Requesting input from user
    lib.typewriter_effect("Select your starting point and destination by entering respective numbers below:")
    time.sleep(1)
    lib.display_station()
    print("\n")
    start = int(input("Enter starting station ID: "))
    end = int(input("Enter destination station ID: "))
    print("\n")

#3: Output info 1- Suggested Route 
lib.typewriter_effect("="*60)
print("1. Suggested Route:")
print(lib.suggest_route(start, end))
fare, distance = calculate_fare(start, end)
print(f"\nTotal Distance: {distance:.1f} km")
print(f"Estimated Fare: RM {fare:.2f}")
lib.typewriter_effect("="*60)
    if 1<=start<=186 and 1<=end<=186:
        #3: Output info 1- Suggested Route 
        lib.typewriter_effect("="*60)
        print("1. Suggested Route:")
        print(lib.suggest_route(start, end))
        time.sleep(1)
        lib.typewriter_effect("="*60)

        #4: Output info 2- Fare 

        time.sleep(1)
        #lib.typewriter_effect("="*60)

        #5: Output info 3- Schedule 
        print("3. Schedule:")
        print(duration.get_next_train_time(start))
        lib.typewriter_effect("="*60)
        time.sleep(1)

        start_another=input("Would you like to start another journey? (Y/N)")
        if start_another == "Y" or start_another == "y":
            continue
        else:
            lib.typewriter_effect("Thanks for choosing MYTransit!")
            break
    else:
        print("Invalid input. Please enter number between a valid range!")
        time.sleep(1)