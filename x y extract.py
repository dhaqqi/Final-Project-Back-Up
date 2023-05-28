import serial

def get_serial_data():
    ser = serial.Serial('COM8', 115200)
    x = 0
    y = 0
    address=0

    range_A1 = 0
    range_A2 = 0
    range_A3 = 0

    while True:
        try:
            data = ser.readline().decode('ascii').strip()
            address, range_value = data.split()
            address = int(address)
            range_value = float(range_value)

            if address == 1782:
                range_A2 = range_value
            elif address == 1783:
                range_A3 = range_value
            elif address == 1781:
                range_A1 = range_value    
        except ValueError:
            pass

        x1, y1 = (2,2)
        x2, y2 = (4,3)
        x3, y3 = (2,5)

        r1 = range_A1
        r2 = range_A2
        r3 = range_A3

        A = (2*x2 - 2*x1)
        B = (2*y2 - 2*y1)
        C = range_A1**2 - range_A2**2 - x1**2 + x2**2 - y1**2 + y2**2

        D = 2*x3 - 2*x2
        E = 2*y3 - 2*y2
        F = range_A2**2 - range_A3**2 - x2**2 + x3**2 - y2**2 + y3**2

        x = (C*E - F*B) / (E*A - B*D)
        y = (C*D - A*F) / (B*D - A*E)

        # Return the x and y values as a tuple
        yield x, y