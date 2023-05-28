import math

# mendefinisikan posisi anchor 
sensor1_pos = [5, 0]
sensor2_pos = [1, 0]
sensor3_pos = [0.5, 4]

#mendefinisikan jarak dari sensor
range1 = 5.5
range2 = 1.0
range3 = 1.2

# melakukan kalkulasi menggunakan triangulasi
A = 2 * sensor2_pos[0] - 2 * sensor1_pos[0]
B = 2 * sensor2_pos[1] - 2 * sensor1_pos[1]

C = range1*2 - range2*2 - sensor1_pos[0]**2 + sensor2_pos[0]**2 - sensor1_pos[1]**2 + sensor2_pos[1]**2

D = 2 * sensor3_pos[0] - 2 * sensor2_pos[0]
E = 2 * sensor3_pos[1] - 2 * sensor2_pos[1]

F = range2*2 - range3*2 - sensor2_pos[0]**2 + sensor3_pos[0]**2 - sensor2_pos[1]**2 + sensor3_pos[1]**2
x = (C*E - F*B) / (E*A - B*D)
y = (C*D - A*F) / (B*D - A*E)

print("Target coordinates: ({:.2f}, {:.2f})".format(x,y))