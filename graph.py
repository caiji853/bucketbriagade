import numpy as np
import math
import matplotlib.pyplot as plt
x = np.arange(0, 1, 0.000001)
y = []
for t in x:
    y_1 = x-pow(2,-x)
    y.append(y_1)
plt.plot(x, y, label="graph")
plt.xlabel("x")
plt.ylabel("y")
plt.ylim(0, 1)
plt.legend()
plt.show()
