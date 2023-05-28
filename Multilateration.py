
import numpy as np

msg = "Hello World"

summary = 3+5


#testing x and y variable
x = 23
y = 2

#anchor1 coordinate
x1=2
y1=30
z1=1.5
#anchor2 coordinate
x2=49
y2=47.5
z2=1.2
#anchor3 coordinate
x3=1.5
y3=2
z3=1.8
#anchor4 coordinate
x4=46.5
y4=0.5
z4=2



#input in range
range1 = 35.00357125
range2 = 52.41078133
range3 = 21.50093021
range4 = 23.54782368


#squared_range
rangeA=range1**2 
rangeB=range2**2    
rangeC=range3**2
rangeD=range4**2

#representing the left flank as v1,v2, and v3
v1=rangeA-rangeB-x1**2+x2**2-y1**2+y2**2-z1**2+z2**2
v2=rangeB-rangeC-x2**2+x3**2-y2**2+y3**2-z2**2+z3**2
v3=rangeC-rangeD-x3**2+x4**2-y3**2+y4**2-z3**2+z4**2

#representing the right flank into 9 variable
m11=(-2*x1+2*x2)
m12=(-2*y1+2*y2)
m13=(-2*z1+2*z2)
m21=(-2*x2+2*x3)
m22=(-2*y2+2*y3)
m23=(-2*z2+2*z3)
m31=(-2*x3+2*x4)
m32=(-2*y3+2*y4)
m33=(-2*z3+2*z4)

#matrix declaration
A = [[m11, m12, m13], 
     [m21, m22, m23],
     [m31, m32, m33]]

Ainv = (np.linalg.inv(A))


print(A)
print(Ainv)

B = [[x],
     [y],
     [1]]

C = [[v1],
     [v2],
     [v3]]







print("A[1][2] =", B[2][0])
print(msg) 
print(Ainv[0][0])
print("The summary is", summary, ", okay")
print("Terus kalo summary+summary hasilnya", summary+summary)

