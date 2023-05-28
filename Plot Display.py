import csv
import tkinter as tk

# Create the main window
window = tk.Tk()

# Global variables
x = 0.0
y = 0.0
is_saving_data = False
data = []

# Inisialisasi data jarak untuk masing-masing sensor
jarak_sensor = {
    'r_A1': None,
    'r_A2': None,
    'r_A3': None
}

posisi_sensor = {
    'r_A1': (2, 2),
    'r_A2': (4, 2),
    'r_A3': (2, 5)
}

# Function to trilaterate object position and save data
def trilaterate_object_position():
    global x, y, is_saving_data, data

    if all(jarak_sensor.values()):
        r1 = jarak_sensor['r_A1']
        r2 = jarak_sensor['r_A2']
        r3 = jarak_sensor['r_A3']
        x1, y1 = posisi_sensor['r_A1']
        x2, y2 = posisi_sensor['r_A2']
        x3, y3 = posisi_sensor['r_A3']

        A = 2 * x2 - 2 * x1
        B = 2 * y2 - 2 * y1
        C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
        D = 2 * x3 - 2 * x2
        E = 2 * y3 - 2 * y2
        F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2

        x = (C * E - F * B) / (E * A - B * D)
        y = (C * D - A * F) / (B * D - A * E)

        # Update the object position label
        object_position_label.config(text=f"Object Position: ({x:.2f}, {y:.2f})")
        cartesian_diagram.update_node(x, y)

        # Save data if flag is set
        if is_saving_data:
            data.append([x, y, r1, r2, r3])

    # Schedule the next trilateration
    window.after(1000, trilaterate_object_position)

# Function to start saving data
def start_saving_data():
    global is_saving_data, data
    is_saving_data = True
    data = []  # Reset the data list
    print("Data saving started.")

# Function to stop saving data
def stop_saving_data():
    global is_saving_data
    is_saving_data = False
    print("Data saving stopped.")

# Create the buttons
start_button = tk.Button(window, text="Start Saving Data", command=start_saving_data)
start_button.pack()

stop_button = tk.Button(window, text="Stop Saving Data", command=stop_saving_data)
stop_button.pack()

# Create the object position label and Cartesian diagram
object_position_label = tk.Label(window, text="Object Position: (0.00, 0.00)")
object_position_label.pack()

cartesian_diagram = tk.Canvas(window, width=400, height=400)
# Configure and draw the diagram

# Call the trilateration function to start the process
trilaterate_object_position()

# Start the main window's event loop
window.mainloop()
