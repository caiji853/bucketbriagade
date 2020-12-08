import math
delta =1e-8
eps = 1e-8
def cal_val(fun, a, b):
    n=1
    fa= fun(a)
    print(fa)
    fb= fun(b)
    print(fb)
    c=(a+b)/2
    while True:
        if fa*fb > 0:
            print("不能用二分法求解!")
            break
        c=(a+b)/2
        fc=fun(c)
        print('二分次数',"{0:.2f}".format(n),'c=',"{0:.8f}".format(c),'f(c)',"{0:.8f}".format(fc),'f(a)',"{0:.8f}".format(fa),'f(b)',"{0:.8f}".format(fb))
        n=n+1

        if fa*fc <0:
            b=c
            fb=fc
        else:
            a=c
            fa=fc
        if b-a<eps:
            break
    return c
def fun(x):
    return x-pow(2,-x)
x=cal_val(fun,0,1)
print('方程的根为x=',"{0:.8f}".format(x))

print("{0:80f}".format(eps))

