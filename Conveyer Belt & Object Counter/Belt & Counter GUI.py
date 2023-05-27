import tkinter as tk
from tkinter import messagebox
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Serial communication settings
SERIAL_PORT = 'COM9'  # Update with your Arduino's serial port
BAUD_RATE = 9600

# Create a serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Data for object count and time
object_count_data = []
time_data = []


# Flag variable to track motor state
motor_running = False

# Function to start the motor with the specified speed
def start_motor():
    global motor_running
    speed = speed_slider.get()
    ser.write(str(speed).encode())
    motor_running = True
    read_serial()

# Function to stop the motor
def stop_motor():
    global motor_running
    ser.write(b'0')
    motor_running = False

# Function to read and update the label with Arduino data
def read_serial():
    if ser.in_waiting > 0:
        # Read the data from Arduino
        data = ser.readline().decode('utf-8').rstrip()

        # Check if the received data is the object count
        if data.startswith("Object Detected:"):
            object_count = int(data.split(":")[1].strip())
            object_count_data.append(object_count)
            time_data.append(len(object_count_data))
            count_label.config(text="Object Count: " + str(object_count))
            update_graph()
        else:
            data_label.config(text="Arduino data: " + data)

    # Schedule the next read after 100 milliseconds if motor is still running
    if motor_running:
        win.after(100, read_serial)

# Function to update the graph
def update_graph():
    # Clear the previous graph
    graph_ax.clear()

    # Plot the object count over time
    graph_ax.plot(time_data, object_count_data)

    # Set the x and y labels
    graph_ax.set_xlabel('Time')
    graph_ax.set_ylabel('Object Count')

    # Update the graph canvas
    graph_canvas.draw()

# Function to display the 'About' message
def about_message():
    messagebox.showinfo("About", "Created by Rupan 2019T00403 @ UOC FOT, All rights Reserved")

# Function to quit the application
def quit_application():
    stop_motor()
    win.destroy()
    
#window close
def on_window_close():
    stop_motor()
    ser.write(b'0')  # Send command to turn off the motor
    ser.close()  # Close the serial connection
    win.destroy()
# Create the main window
win = tk.Tk()
win.title("Conveyor Belt & Object Counter Controller")
win.geometry("700x700")
win.resizable(True, True)

# Create a label to display the Arduino data
data_label = tk.Label(win, text="Conveyor Belt speed controls and Counting Data", font=("Arial", 16))
data_label.pack(pady=20)

# Scale widget for motor speed control
speed_slider = tk.Scale(win, bd=5, from_=35, to=50, orient=tk.HORIZONTAL, length=200)
speed_slider.pack()

# Label widget for motor speed
tk.Label(win, text="Speed of the Belt", font=("Arial", 12)).pack(pady=10)

# Button widgets
blue_btn = tk.Button(win, bd=5, bg='#89CFF0', text="Start Motor", font=("Arial", 12), command=start_motor)
blue_btn.pack(pady=10)

red_btn = tk.Button(win, bd=5, bg='red', text="Stop Motor", font=("Arial", 12), command=stop_motor)
red_btn.pack(pady=10)


# Create a label to display the object count
count_label = tk.Label(win, text="Object Count: 0", fg="Green", font=("Arial", 18))
count_label.pack(pady=20, padx=20)

#Create a figure for the graph
figure = Figure(figsize=(4, 3), dpi=100)
graph_ax = figure.add_subplot(111)

#Create a canvas for the graph
graph_canvas = FigureCanvasTkAgg(figure, master=win)
graph_canvas.draw()
graph_canvas.get_tk_widget().pack()

#about
about_btn = tk.Button(win, text="About", font=("Arial", 12), command=about_message)
about_btn.pack(pady=10)

#Quit
quit_btn = tk.Button(win, text="Quit", font=("Arial", 12), command=quit_application)
quit_btn.pack(pady=10)


# Bind the on_window_close function to the window's close event
win.protocol("WM_DELETE_WINDOW", on_window_close)

# Start the GUI main loop
win.mainloop()
