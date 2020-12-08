#第三题牛顿法
import math
import numpy as np
import matplotlib.pyplot as plt
def obj(x):
    return x-2*math.sin(x+math.pi/3)
def fdj(x):
    return 1-2*math.cos(x+math.pi/3)
x=1e-8
x0=1
while math.fabs(x-x0)>=1e-8 :
        x0 = x
        f=obj(x0)
        fd=fdj(x0)
        if fd!=0:
            x = x0 - f / fd;
        print('x=','{:.8f}'.format(x))  
print('x=','root={:.8f}'.format(x))
print(obj(1.35204421))

a=np.linspace(0,10,100)
xx=[]
y=[]
for i in a:
    xx.append(i)
    y.append(obj(i))
plt.plot(xx,y)
plt.show()