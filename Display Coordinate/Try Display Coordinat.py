import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

x = [2, 2, 14, 14, 5]
y = [2, 40, 40, 2, 25]

plt.plot(x, y, 'r*')
plt.axis([0, 15, 0, 45])

for i, j in zip(x, y):
   plt.text(i, j+0.5, '({}, {})'.format(i, j))

plt.show()