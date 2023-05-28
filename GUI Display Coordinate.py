import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Create label for COM port selection
        self.com_label = tk.Label(self, text="Select COM port:")
        self.com_label.pack(side="left")

        # Create Combobox for COM port selection
        self.port_combobox = ttk.Combobox(self, values=["COM1", "COM2", "COM3"])
        self.port_combobox.pack(side="left")

        # Create button for connecting to COM port
        self.connect_button = tk.Button(self, text="Connect", command=self.connect)
        self.connect_button.pack(side="left")

        # Create label for displaying coordinate
        self.coordinate_label = tk.Label(self, text="Coordinate: (0, 0)")
        self.coordinate_label.pack()

        # Create canvas for Cartesian diagram
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        # Draw x and y axes
        self.canvas.create_line(200, 0, 200, 400, width=2)
        self.canvas.create_line(0, 200, 400, 200, width=2)

    def connect(self):
        # Connect to selected COM port and start receiving data
        selected_port = self.port_combobox.get()
        # TODO: connect to COM port and receive data
        try:
            self.ser = serial.Serial(selected_port, baudrate=9600, timeout=0.5)

            self.receive_data()
        except serial.SerialException:
            messagebox.showerror("Error", "Failed to connect to selected COM port.")



    def update_coordinate(self, x, y):
        # Update coordinate label with new values
        self.coordinate_label.config(text=f"Coordinate: ({x:.2f}, {y:.2f})")

        # Clear previous drawing
        self.canvas.delete("point")

        # Convert Cartesian coordinates to canvas coordinates
        canvas_x = 200 + x * 20
        canvas_y = 200 - y * 20

        # Draw point on canvas
        self.canvas.create_oval(canvas_x-5, canvas_y-5, canvas_x+5, canvas_y+5, fill="red", tags="point")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
