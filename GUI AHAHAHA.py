import tkinter as tk
import serial

# Declare ser as global variable
ser = None

# Inisialisasi posisi masing-masing sensor
posisi_sensor = {
    'r_A1': (2, 2),
    'r_A2': (4, 2),
    'r_A3': (2, 5)
}

# Inisialisasi data jarak untuk masing-masing sensor
jarak_sensor = {
    'r_A1': None,
    'r_A2': None,
    'r_A3': None
}

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

def update_value_label():
    value_label_1.config(text=f"Jarak r_A1: {jarak_sensor['r_A1']}")
    value_label_2.config(text=f"Jarak r_A2: {jarak_sensor['r_A2']}")
    value_label_3.config(text=f"Jarak r_A3: {jarak_sensor['r_A3']}")

# Create the main window
window = tk.Tk()
window.title("Serial Monitor")

# Create a label for displaying the jarak_sensor['r_A1'] value
value_label_1= tk.Label(window, text="Jarak r_A1: -")
value_label_1.grid(row=4, column=0, columnspan=2)

value_label_2= tk.Label(window, text="Jarak r_A2: -")
value_label_2.grid(row=5, column=0, columnspan=2)

value_label_3= tk.Label(window, text="Jarak r_A3: -")
value_label_3.grid(row=6, column=0, columnspan=2)

# Create input fields for serial connection
serial_port_label = tk.Label(window, text="Serial Port:")
serial_port_label.grid(row=0, column=0)
serial_port_entry = tk.Entry(window)
serial_port_entry.grid(row=0, column=1)

baud_rate_label = tk.Label(window, text="Baud Rate:")
baud_rate_label.grid(row=1, column=0)
baud_rate_entry = tk.Entry(window)
baud_rate_entry.grid(row=1, column=1)

# Create a button to connect to serial
connect_btn = tk.Button(window, text="Connect", command=connect_serial)
connect_btn.grid(row=2, column=0, columnspan=2)

# Create a button to disconnect from serial
disconnect_btn = tk.Button(window, text="Disconnect", state="disabled", command=lambda: disconnect_serial(ser))
disconnect_btn.grid(row=2, column=2, columnspan=2)

# Create a text widget for displaying the serial data
#serial_monitor = tk.Text(window, height=10, width=50)
#serial_monitor.grid(row=3, column=0, columnspan=2)

# Start the Tkinter event loop
window.mainloop()
