import tkinter as tk
import serial

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
        for x in range(self.padding, self.canvas_width - self.padding, 20):
            self.canvas.create_line(x, self.padding, x, self.canvas_height - self.padding, fill='lightgray')
        for y in range(self.padding, self.canvas_height - self.padding, 20):
            self.canvas.create_line(self.padding, y, self.canvas_width - self.padding, y, fill='lightgray')

    def draw_node(self):
        x_pos = self.padding + self.x
        y_pos = self.canvas_height - self.padding - self.y
        self.canvas.create_oval(x_pos - self.node_radius, y_pos - self.node_radius, x_pos + self.node_radius, y_pos + self.node_radius, fill="blue")

    def update_node(self, x, y):
        self.x = x
        self.y = y
        self.canvas.delete("all")
        self.draw_axes()
        self.draw_node()


def connect_serial(com_port, baud_rate, cartesian_diagram):
    try:
        ser = serial.Serial(com_port, baud_rate)
        while True:
            line = ser.readline().decode().strip()
            if line:
                x, y = map(int, line.split())
                cartesian_diagram.update_node(x, y)
    except serial.SerialException:
        print("Failed to connect to serial port.")


def connect_button_clicked():
    com_port = com_port_entry.get()
    baud_rate = int(baud_rate_entry.get())

    connect_serial(com_port, baud_rate, cartesian_diagram)


# Create the main window
window = tk.Tk()
window.title("Cartesian Diagram")

# Serial settings frame
serial_frame = tk.Frame(window)
serial_frame.grid(row=0, column=0, padx=10, pady=10)

com_port_label = tk.Label(serial_frame, text="COM Port:")
com_port_label.grid(row=0, column=0, sticky=tk.W)

com_port_entry = tk.Entry(serial_frame)
com_port_entry.grid(row=0, column=1, padx=5)

baud_rate_label = tk.Label(serial_frame, text="Baud Rate:")
baud_rate_label.grid(row=1, column=0, sticky=tk.W)

baud_rate_entry = tk.Entry(serial_frame)
baud_rate_entry.grid(row=1, column=1, padx=5)

connect_button = tk.Button(serial_frame, text="Connect", command=connect_button_clicked)
connect_button.grid(row=2, column=0, columnspan=2, pady=5)

# Cartesian diagram
canvas_width = 400
canvas_height = 400
cartesian_diagram = CartesianDiagram(window, canvas_width, canvas_height)

# Start the Tkinter event loop
window.mainloop()
