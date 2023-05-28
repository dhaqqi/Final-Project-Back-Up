import matplotlib.pyplot as plt
from x_y_extract import get_serial_data

# Set up the plot
fig, ax = plt.subplots()
plt.xlim(0, 10)
plt.ylim(0, 10)
line, = ax.plot([], [], 'o')

def update_plot(x, y):
    # Update the plot with the new x and y values
    line.set_data(x, y)

    fig.canvas.draw()
    fig.canvas.flush_events()

# Get the serial data and plot it dynamically
serial_data = get_serial_data()
while True:
    x, y = next(serial_data)
    update_plot(x, y)