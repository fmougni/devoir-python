import datetime
import time

# Specify the task information
pump1 = {"period": 5, "exec_time": 2, "production": 10}
pump2 = {"period": 15, "exec_time": 3, "production": 20}
machine1 = {"exec_time": 5, "oil_needed": 25, "product": "motor"}
machine2 = {"exec_time": 3, "oil_needed": 5, "product": "wheel"}
tank = {"capacity": 50, "oil": 0}
stocks = {"motor": 0, "wheel": 0}
max_priority = 0

# Define a task list that contains all tasks and their priorities
task_list = [(pump1, 0), (pump2, 0), (machine1, -1), (machine2, -1)]

def pump(period, exec_time, production):
    """
    The function for pump task.
    """
    while True:
        # Check if the tank is not full
        if tank["oil"] + production <= tank["capacity"]:
            # Extract oil from the tank
            tank["oil"] += production
            # Run the task for exec_time seconds
            time.sleep(exec_time)
        time.sleep(period)

def machine(exec_time, oil_needed, product):
    """
    The function for machine task.
    """
    while True:
        # Check if there is enough oil in the tank
        if tank["oil"] >= oil_needed:
            # Take the necessary oil from the tank
            tank["oil"] -= oil_needed
            # Run the task for exec_time seconds
            time.sleep(exec_time)
            # Add the product to the stock
            stocks[product] += 1
        time.sleep(1)

# Define a function to run the scheduler
def scheduler():
    """
    The function for scheduler.
    """
    start_time = datetime.datetime.now()
    while True:
        # Check the current time
        current_time = datetime.datetime.now()
        if (current_time - start_time).seconds >= 120:
            # Stop the scheduler after 2 minutes
            break

        highest_priority = -2
        next_task = None

        # Check each task in the task list
        for task in task_list:
            # If the task is a pump
            if task[0] in [pump1, pump2]:
                # If the tank is full, pump has a low priority
                        # Check each task in the task list
                for task in task_list:
            # If the task is a pump
                    if task in [pump1, pump2]:
                # If the tank is full, pump has a low priority
                       if tank["oil"] == tank["capacity"]:
                          continue
                # Otherwise, set the priority to 0
                          priority = 0
                    else:
                # If there are more wheels than motors, machine1 has a higher priority
                        if stocks["wheel"] / 4 > stocks["motor"]:
                           priority = 1
                # If there are more motors than wheels, machine2 has a higher priority
                        elif stocks["wheel"] / 4 < stocks["motor"]:
                             priority = 2
                # Otherwise, set the priority to -1
                        else:
                         priority = -1
            
            # If the task has a higher priority, set it as the next task to run
            if priority < 0:
                task_to_run = task
                max_priority = priority
        
        # If there is a task to run
        if task_to_run is not None:
            # Run the task
            if task_to_run in [pump1, pump2]:
                pump(task_to_run["period"], task_to_run["exec_time"], task_to_run["production"])
            else:
                machine(task_to_run["exec_time"], task_to_run["oil_needed"], task_to_run["product"])
        else:
            # Wait for a second
            time.sleep(1)

# Run the scheduler
scheduler()

# Create two threads for pump1 and pump2
pump1_thread = threading.Thread(target=pump, args=(pump1["period"], pump1["exec_time"], pump1["production"]))
pump2_thread = threading.Thread(target=pump, args=(pump2["period"], pump2["exec_time"], pump2["production"]))

# Start the pump threads
pump1_thread.start()
pump2_thread.start()

# Create two threads for machine1 and machine2
machine1_thread = threading.Thread(target=machine, args=(machine1[1], machine1["oil_needed"], machine1["product"]))
machine2_thread = threading.Thread(target=machine, args=(machine2[1], machine2["oil_needed"], machine2["product"]))

# Start the machine threads
machine1_thread.start()
machine2_thread.start()

# Wait for the pump threads to finish
pump1_thread.join()
pump2_thread.join()

# Wait for the machine threads to finish
machine1_thread.join()
machine2_thread.join()

# Print the final stock
print("Final stock:", stocks)


