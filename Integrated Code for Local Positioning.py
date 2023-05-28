import tkinter as tk
import serial
import matplotlib.pyplot as plt


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
    port = serial_port_entry.get()
    baud_rate = baud_rate_entry.get()

    try:
        ser = serial.Serial(port, baud_rate)
        connect_btn.config(state="disabled")
        read_serial_data(ser)
    except serial.SerialException:
        print(f"Failed to connect to {port} at {baud_rate} baud rate.")


def read_serial_data(ser):
    data = ser.readline().decode('ascii').strip()
    if data:
        serial_monitor.insert(tk.END, data + '\n')
        serial_monitor.see(tk.END)
        
        # Process the received data for trilateration
        process_data(data)
        
    serial_monitor.after(1, lambda: read_serial_data(ser))


def process_data(data,ser):

    try:
        data = ser.readline().decode('ascii').strip()
        address, range_value = data.split()
        address = int(address)
        range_value = float(range_value)
        # Mengisi data jarak untuk setiap sensor
        if address == 1781:
            jarak_sensor['r_A1'] = range_value
        elif address == 1782:
            jarak_sensor['r_A2'] = range_value
        elif address == 1783:
            jarak_sensor['r_A3'] = range_value
      
        # Jika sudah ada data jarak untuk ketiga sensor, lakukan trilaterasi
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
    # Display the result
            result_label.config(text=f"Posisi objek: ({x:.2f}, {y:.2f})")
    except ValueError:
        pass

# Create the main window
window = tk.Tk()
window.title("Serial Monitor")

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

# Create a text widget for displaying the serial data
serial_monitor = tk.Text(window, height=10, width=50)
serial_monitor.grid(row=3, column=0, columnspan=2)

# Create a label for displaying the trilateration result
result_label = tk.Label(window, text="Posisi objek: -")
result_label.grid(row=4, column=0, columnspan=2)

# Store anchor ranges
anchor_ranges = {
    1781: None,
    1782: None,
    1783: None
}

# Sensor positions
posisi_sensor = {
    'r_A1': (2, 2),
    'r_A2': (5, 2),
    'r_A3': (4, 5)
}

# Run the GUI event loop
window.mainloop()