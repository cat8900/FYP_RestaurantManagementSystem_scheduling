import easygui
import tkinter as tk

class ProcessBox:
    def __init__(self, root, i):
        self.pid_label = tk.Label(root, text=f"Process {i+1} ID:")
        self.pid_label.grid(row=i, column=0)
        self.pid_entry = tk.Entry(root)
        self.pid_entry.grid(row=i, column=1)

        self.bt_label = tk.Label(root, text=f"Burst Time:")
        self.bt_label.grid(row=i, column=2)
        self.bt_entry = tk.Entry(root)
        self.bt_entry.grid(row=i, column=3)

        self.priority_label = tk.Label(root, text=f"Priority:")
        self.priority_label.grid(row=i, column=4)
        self.priority_entry = tk.Entry(root)
        self.priority_entry.grid(row=i, column=5)

    def get_values(self):
        pid = self.pid_entry.get()
        bt = int(self.bt_entry.get())
        priority = int(self.priority_entry.get())
        return [pid, bt, priority]

def priority_scheduling_gui():
    root = tk.Tk()

    n_label = tk.Label(root, text="Number of processes:")
    n_label.grid(row=0, column=0)
    n_entry = tk.Entry(root)
    n_entry.grid(row=0, column=1)

    def on_submit():
        n = int(n_entry.get())
        proc_boxes = [ProcessBox(root, i) for i in range(n)]
        submit_button.destroy()

        def on_done():
            proc = [box.get_values() for box in proc_boxes]
            priorityScheduling(proc, n)
            root.destroy()

        done_button = tk.Button(root, text="Done", command=on_done)
        done_button.grid(row=n+1, column=0, columnspan=6)

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=0, column=2, columnspan=2)

    root.mainloop()

def shortest_remaining_time_gui():
    root = tk.Tk()

    n_label = tk.Label(root, text="Number of processes:")
    n_label.grid(row=0, column=0)
    n_entry = tk.Entry(root)
    n_entry.grid(row=0, column=1)

    def on_submit():
        n = int(n_entry.get())
        proc_boxes = [ProcessBox(root, i) for i in range(n)]
        submit_button.destroy()

        def on_done():
            processes = [box.get_values() for box in proc_boxes]
            n = len(processes)
            wt = [0] * n
            tat = [0] * n
            findWaitingTime(processes, n, wt)
            findTurnAroundTime(processes, n, wt, tat)
            findavgTime(processes, n)
            root.destroy()

        done_button = tk.Button(root, text="Done", command=on_done)
        done_button.grid(row=n+1, column=0, columnspan=6)

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=0, column=2, columnspan=2)

    root.mainloop()


# Prompt user to choose between the two codes
choice = easygui.buttonbox("Choose the algorithm to run:",
                           choices=["Priority Scheduling",
                                    "Shortest Job First Scheduling"])

# Execute the chosen code
if choice == "Priority Scheduling":
    # Prompt user for the number of processes to schedule
    n = int(easygui.enterbox("Enter the number of processes to schedule:"))

    # Prompt user to enter the process details
    proc = []
    for i in range(n):
        pid = easygui.enterbox(f"Enter process {i+1} ID:")
        bt = int(easygui.enterbox(f"Enter process {i+1} burst time:"))
        priority = int(easygui.enterbox(f"Enter process {i+1} priority (higher value means higher priority):"))
        proc.append([pid, bt, priority])

    # Function to calculate waiting time
    def findWaitingTime(processes, n, wt):
        wt[0] = 0

        # calculating waiting time
        for i in range(1, n):
            wt[i] = processes[i - 1][1] + wt[i - 1]

    # Function to calculate turn around time
    def findTurnAroundTime(processes, n, wt, tat):
        # Calculating turnaround time by
        # adding bt[i] + wt[i]
        for i in range(n):
            tat[i] = processes[i][1] + wt[i]

    # Function to calculate average waiting
    # and turn-around times.
    def findavgTime(processes, n):
        wt = [0] * n
        tat = [0] * n

        # Function to find waiting time
        # of all processes
        findWaitingTime(processes, n, wt)

        # Function to find turn around time
        # for all processes
        findTurnAroundTime(processes, n, wt, tat)

        # Calculate average waiting time and turn-around time
        total_wt = sum(wt)
        total_tat = sum(tat)
        avg_wt = total_wt / n
        avg_tat = total_tat / n

        # Display results in a message box
        msg = "Processes\tBurst Time\tWaiting Time\tTurn-Around Time\n"
        for i in range(n):
            msg += f"{processes[i][0]}\t\t{processes[i][1]}\t\t{wt[i]}\t\t{tat[i]}\n"
        msg += f"\nAverage waiting time = {avg_wt:.2f}\nAverage turn-around time = {avg_tat:.2f}"
        easygui.msgbox(msg, title="Priority Scheduling Results")

    def priorityScheduling(proc, n):

        # Sort processes by priority
        proc = sorted(proc, key=lambda proc: proc[2],
                      reverse=True)

        print("Order in which processes gets executed")
        for i in proc:
            print(i[0], end=" ")
        findavgTime(proc, n)
    
    # Call the priorityScheduling() function to schedule the processes
    priorityScheduling(proc, n)

else:
    # Shortest Remaining Time First
    # Prompt user for the number of processes to schedule
    n = int(easygui.enterbox("Enter the number of processes to schedule:"))

    # Prompt user to enter the process details
    proc = []
    for i in range(n):
        pid = easygui.enterbox(f"Enter process {i+1} ID:")
        bt = int(easygui.enterbox(f"Enter process {i+1} burst time:"))
        proc.append([pid, bt])
# Function to calculate waiting time
def findWaitingTime(processes, n, wt):
    rt = [0] * n

    # Copy the burst times into rt[]
    for i in range(n):
        rt[i] = processes[i][1]

    complete = 0
    t = 0
    minm = 999999999
    short = 0
    check = False

    # Process until all processes are completed
    while complete != n:

        # Find the process with minimum remaining time at a given time t
        for j in range(n):
            if (processes[j][1] > 0 and processes[j][1] < minm and processes[j][1] <= t):
                minm = processes[j][1]
                short = j
                check = True

        if not check:
            t += 1
            continue

        # Reduce remaining time by 1
        rt[short] -= 1

        # Update minimum
        minm = rt[short]
        if minm == 0:
            minm = 999999999

        # If a process gets completely executed
        if rt[short] == 0:
            # Increment complete
            complete += 1
            check = False

            # Calculate waiting time
            wt[short] = t - processes[short][1] + 1

            if wt[short] < 0:
                wt[short] = 0

        # Increment time
        t += 1

# Function to calculate turn around time
def findTurnAroundTime(processes, n, wt, tat):
    # Calculating turnaround time by adding bt[i] + wt[i]
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

# Function to calculate average waiting
# and turn-around times.
def findavgTime(processes, n):
    wt = [0] * n
    tat = [0] * n

    # Function to find waiting time
    # of all processes
    findWaitingTime(processes, n, wt)

    # Function to find turn around time
    # for all processes
    findTurnAroundTime(processes, n, wt, tat)

    # Calculate average waiting time and turn-around time
    total_wt = sum(wt)
    total_tat = sum(tat)
    avg_wt = total_wt / n
    avg_tat = total_tat / n

    # Display results in a message box
    msg = "Processes\tBurst Time\tWaiting Time\tTurn-Around Time\n"
    for i in range(n):
        msg += f"{processes[i][0]}\t\t{processes[i][1]}\t\t{wt[i]}\t\t{tat[i]}\n"
    msg += f"\nAverage waiting time = {avg_wt:.2f}\nAverage turn-around time = {avg_tat:.2f}"
    easygui.msgbox(msg, title="Shortest Job First Scheduling Results")

# Call the sjfScheduling() function to schedule the processes
sjfScheduling(proc, n)
