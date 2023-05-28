import math

# define posisi keempat anchor
sensor1_pos = [10, 10]
sensor2_pos = [50, 10]
sensor3_pos = [10, 50]
sensor4_pos = [50, 50]

# define jarak yang terukur secara manual
range1 = 32.757
range2 = 36.235
range3 = 20.809
range4 = 25.942

# menghitung koordinat menggunakan multilaterasi
A = 2 * sensor2_pos[0] - 2 * sensor1_pos[0]
B = 2 * sensor2_pos[1] - 2 * sensor1_pos[1]
C = range1*2 - range2*2 - sensor1_pos[0]**2 + sensor2_pos[0]**2 - sensor1_pos[1]**2 + sensor2_pos[1]**2

D = 2 * sensor3_pos[0] - 2 * sensor2_pos[0]
E = 2 * sensor3_pos[1] - 2 * sensor2_pos[1]
F = range2*2 - range3*2 - sensor2_pos[0]**2 + sensor3_pos[0]**2 - sensor2_pos[1]**2 + sensor3_pos[1]**2

G = 2 * sensor4_pos[0] - 2 * sensor2_pos[0]
H = 2 * sensor4_pos[1] - 2 * sensor2_pos[1]
I = range3*2 - range4*2 - sensor3_pos[0]**2 + sensor4_pos[0]**2 - sensor3_pos[1]**2 + sensor4_pos[1]**2

x = (C*E - F*B) / (E*A - B*D)
y = (C*D - A*F) / (B*D - A*E)

print("Target coordinates: ({:.2f}, {:.2f})".format(x,y))
print(sensor4_pos[0], range1)