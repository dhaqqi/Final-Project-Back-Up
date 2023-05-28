import math

# Inisialisasi posisi masing-masing perangkat
posisi_perangkat = {
    'r_A1': (2, 2),
    'r_A2': (4, 2),
    'r_A3': (2, 5)
}

# Inisialisasi data jarak untuk masing-masing perangkat
jarak_perangkat = {
    'r_A1': 5.385,
    'r_A2': 3.731,
    'r_A3': 4.796
}

# Implementasi metode trilaterasi untuk mendapatkan koordinat 2 dimensi
def trilaterasi(posisi_perangkat, jarak_perangkat):
    x1, y1 = posisi_perangkat['r_A1']
    x2, y2 = posisi_perangkat['r_A2']
    x3, y3 = posisi_perangkat['r_A3']
    
    r1 = jarak_perangkat['r_A1']
    r2 = jarak_perangkat['r_A2']
    r3 = jarak_perangkat['r_A3']
    
    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    
    return (x, y)

# Panggil metode trilaterasi dan tampilkan hasilnya
koordinat = trilaterasi(posisi_perangkat, jarak_perangkat)
print("Koordinat titik yang ditentukan adalah:", koordinat)