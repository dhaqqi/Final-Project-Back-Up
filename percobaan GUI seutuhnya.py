import tkinter as tk
import serial
import matplotlib.pyplot as plt
import csv


is_saving_data = False
data = []
header = ['x', 'y', 'range1', 'range2', 'range3']


class CartesianDiagram:
    def __init__(self, master, width, height):
        self.master = master
        self.canvas_width = width
        self.canvas_height = height
        self.padding = 20
        self.node_radius = 5
        self.x = 0
        self.y = 0

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(row=0, column=1)

        self.draw_axes()
        self.draw_node()

    def draw_axes(self):

        x_range = range(0, 51)  # Adjusted x-axis range
        y_range = range(0, 17)  # Adjusted y-axis range
    
        for x in x_range:
            x_pos = self.padding + x * (self.canvas_width - 2 * self.padding) / 50
            self.canvas.create_line(x_pos, self.padding, x_pos, self.canvas_height - self.padding, fill='lightgray')
            self.canvas.create_text(x_pos, self.canvas_height - self.padding + 10, text=str(x), anchor='n')
        
        for y in y_range:
            y_pos = self.canvas_height - self.padding - y * (self.canvas_height - 2 * self.padding) / 16
            self.canvas.create_line(self.padding, y_pos, self.canvas_width - self.padding, y_pos, fill='lightgray')
            self.canvas.create_text(self.padding - 10, y_pos, text=str(y), anchor='w', justify='right')

#        for x in range(self.padding, self.canvas_width - self.padding, 100):
#            self.canvas.create_line(x, self.padding, x, self.canvas_height - self.padding, fill='lightgray')
#  
#        for y in range(self.padding, self.canvas_height - self.padding, 100):
#            self.canvas.create_line(self.padding, y, self.canvas_width - self.padding, y, fill='lightgray')

    def draw_node(self):
        x_pos = self.padding + self.x
        y_pos = self.canvas_height - self.padding - self.y
        self.canvas.create_oval(x_pos - self.node_radius, y_pos - self.node_radius, x_pos + self.node_radius, y_pos + self.node_radius, fill="blue")

    def update_node(self, x, y):
        self.x = x
        self.y = y
        self.canvas.delete("all")


        x_range = 50  # Set the x-axis range from 0 to 15
        y_range = 16  # Set the y-axis range from 0 to 15

        x_pos = self.padding + (self.x / x_range) * (self.canvas_width - 2 * self.padding)
        y_pos = self.canvas_height - self.padding - (self.y / y_range) * (self.canvas_height - 2 * self.padding)

        self.canvas.create_oval(x_pos - self.node_radius, y_pos - self.node_radius,
                                x_pos + self.node_radius, y_pos + self.node_radius, fill="blue")


        self.draw_axes()
        self.draw_node()


# Declare ser as global variable
ser = None

# Declare x and y as global var
x = 0
y = 0

# Inisialisasi posisi masing-masing sensor
posisi_sensor = {
    'r_A1': (3, 3),
    'r_A2': (6, 3),
    'r_A3': (3, 9)
}


def save_positions():
    posisi_sensor['r_A1'] = (float(entry_A1_x.get()), float(entry_A1_y.get()))
    posisi_sensor['r_A2'] = (float(entry_A2_x.get()), float(entry_A2_y.get()))
    posisi_sensor['r_A3'] = (float(entry_A3_x.get()), float(entry_A3_y.get()))
    print("Positions saved:", posisi_sensor)


# Inisialisasi data jarak untuk masing-masing sensor
jarak_sensor = {
    'r_A1': None,
    'r_A2': None,
    'r_A3': None
}

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


 

def connect_serial():
    global ser # declare ser as a global variable
    port = serial_port_entry.get()
    baud_rate = baud_rate_entry.get()

    try:
        ser = serial.Serial(port, baud_rate)
        connect_btn.config(state="disabled")
        disconnect_btn.config(state="normal") #enable disconnect button
        read_serial_data(ser)
    except serial.SerialException:
        print(f"Failed to connect to {port} at {baud_rate} baud rate.")

def read_serial_data(ser):
    extract_range(ser)
    window.after(1, read_serial_data,ser)
#    data = ser.readline().decode('ascii').strip()
#    if data:
#        serial_monitor.insert(tk.END, data + '\n')
#        serial_monitor.see(tk.END)
#    serial_monitor.after(1, lambda: read_serial_data(ser))

def disconnect_serial(_=None):
    global ser 
    
    if ser and ser.is_open:
        ser.close()
        ser = None
        connect_btn.config(state="normal")
        disconnect_btn.config(state="disable") #disable disconnect button

def extract_range(ser):
    # set a timeout 0.1 seconds
    ser.timeout = 0.1
    data = ser.read_until().decode('ascii').strip()
    if data:
        try:
            data = ser.readline().decode('ascii').strip()
            address, range_value = data.split()
            address = int(address)
            range_value = float(range_value)
        
            # Mengisi data jarak untuk setiap sensor
            if address == 1781:
                jarak_sensor['r_A1'] = range_value
                update_value_label()
            elif address == 1782:
                jarak_sensor['r_A2'] = range_value
                update_value_label()
            elif address == 1783:
                jarak_sensor['r_A3'] = range_value
                update_value_label()
        except ValueError:
            pass
    # Call the trilateration function

    

    trilaterate_object_position()    


def update_value_label():
    value_label_1.config(text=f"Jarak r_A1: {jarak_sensor['r_A1']}")
    value_label_2.config(text=f"Jarak r_A2: {jarak_sensor['r_A2']}")
    value_label_3.config(text=f"Jarak r_A3: {jarak_sensor['r_A3']}")

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
    if data:
        save_data_to_csv()

# Function to save data to a CSV file
def save_data_to_csv():
    file_name = 'object_position.csv'
    header = ['x', 'y', 'range1', 'range2', 'range3']
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    print(f"Data extracted and saved to '{file_name}' successfully.")



# Create the main window
window = tk.Tk()
window.title("Serial Monitor")

# Create a label for displaying the jarak_sensor['r_A1'] value
value_label_1= tk.Label(window, text="Jarak r_A1: -")
value_label_1.grid(row=4, column=0)

value_label_2= tk.Label(window, text="Jarak r_A2: -")
value_label_2.grid(row=5, column=0)

value_label_3= tk.Label(window, text="Jarak r_A3: -")
value_label_3.grid(row=6, column=0)

# Create input fields for serial connection
serial_port_label = tk.Label(window, text="Serial Port:")
serial_port_label.grid(row=1, column=0, sticky=tk.W)
serial_port_entry = tk.Entry(window)
serial_port_entry.grid(row=1, column=1, sticky=tk.W)

baud_rate_label = tk.Label(window, text="Baud Rate:")
baud_rate_label.grid(row=2, column=0, sticky=tk.W)
baud_rate_entry = tk.Entry(window)
baud_rate_entry.grid(row=2, column=1, sticky=tk.W)

# Create a label for displaying the object position
object_position_label = tk.Label(window, text="Object Position: -")
object_position_label.grid(row=7, column=0)

# Create a button to connect to serial
connect_btn = tk.Button(window, text="Connect", command=connect_serial)
connect_btn.grid(row=3, column=0, sticky=tk.E)

# Create a button to disconnect from serial
disconnect_btn = tk.Button(window, text="Disconnect", state="disabled", command=lambda: disconnect_serial(ser))
disconnect_btn.grid(row=3, column=1, sticky=tk.W)

# Create a text widget for displaying the serial data
#serial_monitor = tk.Text(window, height=10, width=50)
#serial_monitor.grid(row=3, column=0, columnspan=2)

# Adjust column widths
# Configure column 0 with a minimum width of 100
window.columnconfigure(0, minsize=100)

# Configure column 1 with a minimum width of 200
window.columnconfigure(1, minsize=200)

# Configure column 2 with a minimum width of 150
window.columnconfigure(2, minsize=150)


# Create the input fields for sensor positions
label_A1 = tk.Label(window, text="Sensor A1:")
label_A1.grid(row=13, column=0, sticky=tk.W)
entry_A1_x = tk.Entry(window)
entry_A1_x.grid(row=13, column=1, sticky=tk.W)
entry_A1_y = tk.Entry(window)
entry_A1_y.grid(row=13, column=3, sticky=tk.W)

label_A2 = tk.Label(window, text="Sensor A2:")
label_A2.grid(row=14, column=0, sticky=tk.W)
entry_A2_x = tk.Entry(window)
entry_A2_x.grid(row=14, column=1, sticky=tk.W)
entry_A2_y = tk.Entry(window)
entry_A2_y.grid(row=14, column=3, sticky=tk.W)

label_A3 = tk.Label(window, text="Sensor A3:")
label_A3.grid(row=15, column=0, sticky=tk.W)
entry_A3_x = tk.Entry(window)
entry_A3_x.grid(row=15, column=1, sticky=tk.W)
entry_A3_y = tk.Entry(window)
entry_A3_y.grid(row=15, column=3, sticky=tk.W)

# Create a button to save the positions
save_button = tk.Button(window, text="Save Positions", command=save_positions)
save_button.grid(row=16, column=0, columnspan=1)

# Create the buttons using grid layout
start_button = tk.Button(window, text="Start Saving Data", command=start_saving_data)
start_button.grid(row=17, column=0, padx=10, pady=5)

stop_button = tk.Button(window, text="Stop Saving Data", command=stop_saving_data)
stop_button.grid(row=17, column=1, padx=10, pady=5)

# Cartesian diagram
canvas_width = 1300
canvas_height = 600
cartesian_diagram = CartesianDiagram(window, canvas_width, canvas_height)


# Start the Tkinter event loop
window.mainloop()

