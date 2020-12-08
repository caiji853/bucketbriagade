import random
import numpy as np
import math
P=[]#产品i在工作站f的加工时间
D=[]#产品i在工作站f的阻塞时间
CP=[]#产品的累计加工时间，index为i,f
CD=[]#产品的累计阻塞时间，index为i,f
S=[]#工作站序列
time=[]#工人w在生产i产品时在工作站f的工作时间
start=[]#产品的开始时间
terminal=[]#产品i的交付时间
N#工人数量
station#工作站数量
order#产品数量


#计算D
def calculate_D(CP):
    D=np.zeros((order+1,station+1))
    CD=np.zeros((order+1,station+1))
    start=np.zeros((order+1))
    terminal=np.zeros((order+1))
   #初始化
    for f in range(station+1):
        D[1][f]=0
        CD[1][f]=0
    for i in range(1,order+1):
        D[i][station]=0
    start[1]=0

    for i in range(2,order+1):
        if i<=N:
            for f in range(station+1):
                if f==0:
                   D[i][f]=max(start[i-1]+CD[i-1][f+1]+CP[i-1][f+1],0)
                   CD[i][f]=D[i][f]
                elif f==1:
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                   start[i]=start[i-1]+CP[i-1][f]+CD[i-1][f]
                elif f<station:
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                else:
                   CD[i][f]=CD[i][f-1]
                   terminal[i]=start[i]+CP[i][f]+CD[i][f]
        else:
            start[i]=terminal[i-N]
            for f in range(station+1):
                if f==0:
                   D[i][f]=max(start[i-1]+CD[i-1][f+1]+CP[i-1][f+1],0)
                elif f==1:
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                elif f<station:
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                else:
                   CD[i][f]=CD[i][f-1]
                   terminal[i]=start[i]+CP[i][f]+CD[i][f]
#    for i in range(1,order+1):
#         if i==1:
#             start[i]=0
#         elif i<N:
#             start[i]=start[i-1]+CP[i-1][1]+CD[i-1][1]
#         else:
#             start[i]=terminal[i-n]                   

#目标函数
def calculate_ter(terminal):
       return max(terminal)
#计算P
def calculate_P():
    for i in range(1,order+1):
        for f in range(1,station+1):
            for w in range(1,N+1):
                P[i][f]=p[i][f]+time[w][i][f]
    return P
        
#计算CP
def calculate_CP(P):
    CP=np.zeros((order+1,station+1))
    for i in range(1,order+1):
        for f in range(1,station+1):
           if f==1:
               CP[i][f]=P[i][f]
           else:
               CP[i][f]=P[i][f]+CP[i][f-1]

    return CP
#计算CD   
def calculate_CD(D):
    CD=np.zeros((order+1,station+1))
    for i in range(1,order+1):
         for f in range(1,station+1):
             if f==0:
                 CD[i][f]=D[i][f]
             else:
                 CD[i][f]=D[i][f]+CD[i][f-1]

    return CD




