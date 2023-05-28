import serial

ser = serial.Serial('COM3', 115200)

address=0
r_A1 = None
r_A2 = None
r_A3 = None

while True:
    try:
        data = ser.readline().decode('ascii').strip()
        address, range_value = data.split()
        address = int(address)
        range_value = float(range_value)
        
        if address == 1782:
            r_A2 = range_value
        elif address == 1783:
            r_A3 = range_value
        elif address == 1781:
            r_A1 = range_value    
    except ValueError:
        pass

    # do something with the address and range values
    print(f" Anchor 1 = {r_A1} Anchor 2 = {r_A2} Anchor 3 = {r_A3}")