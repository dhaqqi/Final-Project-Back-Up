import serial
import math

# buka koneksi dengan Serial Monitor
ser = serial.Serial('COM3', 115200)

# inisialisasi variabel jarak_perangkat
jarak_perangkat = {'1781': 0, '1782': 0, '1783': 0}

# posisi setiap perangkat dalam satuan meter
posisi_perangkat = {'1781': (0, 0), '1782': (5, 0), '1783': (0, 5)}

jarak_perangkat = {}
received_addresses = set()

while True:
    data = Serial.readline().decode().strip()
    if data:
        address, jarak = data.split('\t')
        jarak_perangkat[address] = float(jarak[:-1])
        received_addresses.add(address)
        if len(received_addresses) == 3:
            if all(addr in jarak_perangkat for addr in ['1781', '1782', '1783']):
                koordinat = multilateration(r_A1, r_A2, r_A3, jarak_perangkat['1781'], jarak_perangkat['1782'], jarak_perangkat['1783'])
                print(koordinat)
                jarak_perangkat.clear()
                received_addresses.clear()
            else:
                jarak_perangkat.clear()
                received_addresses.clear()
    # lakukan trilaterasi untuk mendapatkan koordinat
    r_A1 = jarak_perangkat['1781']
    r_A2 = jarak_perangkat['1782']
    r_A3 = jarak_perangkat['1783']

    x1, y1 = posisi_perangkat['1781']
    x2, y2 = posisi_perangkat['1782']
    x3, y3 = posisi_perangkat['1783']

    A = 2 * x2 - 2 * x1
    B = 2 * y2 - 2 * y1
    C = r_A1**2 - r_A2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * x3 - 2 * x2
    E = 2 * y3 - 2 * y2
    F = r_A2**2 - r_A3**2 - x2**2 + x3**2 - y2**2 + y3**2

    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)

    print('Koordinat:', x, y)