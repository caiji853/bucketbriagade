import numpy as np
import math
import random
import scipy.stats
import csv
worker=5
station=8
order=20
worker_speed=[]
product_station=[]
processing_time=[[[0 for i in range(station)] for i in range(worker) ] for i in range(order)]
worker_sequence=np.zeros((worker+1,station+1))
pos=random.sample(range(1,worker+1),worker)
P=np.zeros((order+1,station+1))
L=np.zeros((worker+1))
end=np.zeros((worker+1))
CP=np.zeros((order+1,station+1))
D=np.zeros((order+1,station+1))
CD=np.zeros((order+1,station+1))
start=np.zeros((order+1))
terminal=np.zeros((order+1))
leave=np.zeros((order+1,station+1))
#print(pos)
#print(pos[1])
def cal_station():
    lower = 0
    upper = 1
    sigma = 0.1
    mu = 1/station
    result=[]
    summary=0
    flag=0
    flag_new=0
    # o=0
    while  flag_new==0 or flag==1:
        if flag==1:
            result=[]
        for i in range(station-1):
        
            summary=0
            samples = scipy.stats.truncnorm.rvs(          (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=1)
            result.append(round(samples[0],2))
            # print(samples[0])
            for j in range(len(result)):
                summary+=result[j]
            # print(summary)    
            if summary>=1:
                flag=1
                break 
            elif i==station-2:
                flag=0
                flag_new=1
            else:
                pass
    result.append(round(1-summary,2))
    return result
def cal_worker_speed():
    #!/usr/bin/python3
    # -*- coding: utf-8 -*-
    # 导入CSV安装包
    # 1. 创建文件对象
    # i=0
    f = open('worker.csv', 'w',newline='',encoding="utf-8")# 2. 基于文件对象构建 csv写入对象
    csv_write= csv.writer(f)
    # 3. 构建列表
    for i in range(worker):
        csv_write.writerow(np.random.randint(1,10,station))
        print(np.random.randint(1,10,station))
    # 4. 写入csv文件内容
    # 5. 关闭文件
    f.close()
    worker_speed = np.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
    return worker_speed
def cal_station_data():
    # lower = 0
    # upper = 1
    # sigma = 0.1
    # mu = 1/station
    # result=[]
    # summary=0
    # flag=0
    # flag_new=0
    # o=0
    # while  flag_new==0 or flag==1:
    #     if flag==1:
    #         result=[]
    #     for i in range(station-1):
        
    #         summary=0
    #         samples = scipy.stats.truncnorm.rvs(          (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=1)
    #         result.append(round(samples[0],2))
    #         # print(samples[0])
    #         for j in range(len(result)):
    #             summary+=result[j]
    #         # print(summary)    
    #         if summary>=1:
    #             flag=1
    #             break 
    #         elif i==station-2:
    #             flag=0
    #             flag_new=1
    #         else:
    #             pass
    # result.append(round(1-summary,2))
    station_data=[]
    for o in range(order):
        result=cal_station()
        station_data.append(result)
    print(station_data)
    tmp = open('data.csv', 'w',newline='',encoding="utf-8") #a表示在最后一行后面追加 #newline以免出现写一行空一行 #encoding 解决不能写入的错误
    csv_write = csv.writer(tmp) 
    #csv_write.writerow(['id', 'eng_socre']) 写入列名
    for  item in station_data:
        if item !=None:
            csv_write.writerow(item)
    tmp.close()
    print('over')
    product_station=np.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
    print(product_station)
    return product_station
def cal_processing_time(worker_speed,product_station):
    # worker_speed = np.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
    # print(worker_speed)
    # product_station=np.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
    # print(product_station)
    order=len(product_station)
    station=len(product_station[0])
    worker=len(worker_speed)
    # processing_time=[[[0 for i in range(station)] for i in range(worker) ] for i in range(order)]
    # print(processing_time)
    for i in range(order):
       for w in range(worker):
            for f in range(station):
                processing_time[i][w][f]=round(product_station[i][f]*60/worker_speed[w][f],2)
    # print(processing_time)
    # numpy.savetxt('processing_time.csv', processing_time, delimiter = ',')
    tmp = open('processing_time.csv', 'w',newline='',encoding="utf-8") # a表示在最后一行后面追加  #newline以免出现写一行空一行 #encoding 解决不能写入的错误
    csv_write = csv.writer(tmp) #csv_write.writerow(['id', 'eng_socre']) 写入列名
    for  item in processing_time:
        csv_write.writerow(item)
    tmp.close()
    print('over')
    print(processing_time)
    return processing_time
def cal_worker_sequence():
    # worker_sequence=np.zeros((worker+1,station+1))
    # pos=random.sample(range(1,worker+1),worker)
    print(pos)
    worker_sequence[pos[worker-1]][station]=1
    for i in range(1,worker+1):
        #     pos=np.random.randint(1,worker+1,worker)
      count=0
      if i==1:
          start_pos=1
          end_pos=np.random.randint(1,station+1-(worker-i-1))
      elif i < worker:
          end_pos1=np.random.randint(end_pos,station-(worker-i-1)) 
          for j in range(1,worker+1):
              if worker_sequence[j][end_pos]==1:
                 count+=1
          if  count<2 and end_pos1-end_pos>=1:
              start_pos=np.random.randint(end_pos,end_pos+1)  
          elif count<2 and end_pos1==end_pos:
              start_pos=end_pos
          else:
              start_pos=end_pos+1
              end_pos1=np.random.randint(start_pos,station-(worker-i-1)) 
              print(start_pos)
          end_pos=end_pos1
      elif i==worker-1:
           end_pos1=np.random.randint(end_pos,station-1-(worker-i-1)) 
           for j in range(1,worker+1):
                  if worker_sequence[j][end_pos]==1:
                      count+=1
           if  count<2 and end_pos1-end_pos>=1:
               start_pos=np.random.randint(end_pos,end_pos+1)  
           elif count<2 and end_pos1==end_pos:
               start_pos=end_pos
           else:
               start_pos=end_pos+1
               end_pos1=np.random.randint(start_pos,station-(worker-i-1)) 
           end_pos=end_pos1
      else:
          for j in range(1,worker+1):
              if worker_sequence[j][end_pos]==1:
                 count+=1
          if  count<2 :
              start_pos=np.random.randint(end_pos,end_pos+1)
          else:
              start_pos=end_pos+1
            
          end_pos=station
      for j in range(start_pos,end_pos+1):
          worker_sequence[pos[i-1]][j]=1
    print(worker_sequence)
    return worker_sequence,pos
#计算P
def calculate_P(worker_sequence,pos,processing_time):
    # P=np.zeros((order+1,station+1))
    # L=np.zeros((worker+1))
    # end=np.zeros((worker+1))
    for m in range(worker-1,0,-1): 
            position=station
            print(pos[m])
            posi=int(worker_sequence[pos[m]][position])
            while posi==0:
                  position-=1
                  posi=int(worker_sequence[pos[m]][position])
            end[worker-m]=position
            print(position)
            for f in range(1,position):
                 P[worker-m][f]=np.round(processing_time[worker-m-1][pos[m]-1][f-1],2)
                 L[worker-m]+=P[worker-m][f]
            for o in range(1,worker+1):
                if o!=pos[m] and m!=worker-1:
                    for j in range(m+1,worker):
                        if o==pos[j] and worker_sequence[pos[j]][position]==1:
                            ran=random.random()
                            time=round(processing_time[worker-m-1][pos[m]-1][position-1]*ran,2)
                            P[worker-m][position]=time+round(processing_time[worker-m-1][pos[j]-1][position-1]*(1-ran),2)
                            L[worker-m]+=time
                elif m==worker-1:
                    P[worker-m][position]=np.round(processing_time[worker-m-1][pos[m]-1][position-1],2)
                    # L[worker-m]+=P[worker-m][position]
            for f in range(position+1,station+1):
                flag=0
                for o in range(1,worker+1):
                    for p in range(o+1,worker+1):
                        if worker_sequence[o][f]==1 and worker_sequence[p][f]==1 :
                            ran=random.random()
                            flag=1
                            P[worker-m][f]=np.round(processing_time[worker-m-1][o-1][f-1]*ran+processing_time[worker-m-1][p-1][f-1]*(1-ran),2)
                        elif  worker_sequence[o][f]==1 and worker_sequence[p][f]!=1:
                            flag=0
                            posi=o 
                if flag==0:
                    P[worker-m][f]=np.round(processing_time[worker-m-1][posi-1][f-1],2)
            if m==worker-1:
                    P[worker-m][position]=np.round(processing_time[worker-m-1][pos[m]-1][position-1],2)
                    L[worker-m]+=P[worker-m][position]
    
    position=station
    print(pos[0])
    posi=int(worker_sequence[pos[0]][position])
    while posi==0:
        position-=1
        posi=int(worker_sequence[pos[0]][position])
    end[worker]=position
    for i in range(worker,order+1):
        for f in range(1,station+1):
                flag=0
                for o in range(1,worker+1):
                    for p in range(o+1,worker+1):
                        if worker_sequence[o][f]==1 and worker_sequence[p][f]==1:
                            ran=random.random()
                            flag=1
                            time=round(processing_time[i-1][o-1][f-1]*ran,2)
                            P[i][f]=round(processing_time[i-1][o-1][f-1]*ran+processing_time[i-1][p-1][f-1]*(1-ran),2)
                            if i == worker:
                                L[i]+=time
                        elif  worker_sequence[o][f]==1 and worker_sequence[p][f]!=1:
                            flag=0
                            posi=o 
                if flag==0:
                    P[i][f]=np.round(processing_time[i-1][posi-1][f-1],2)
                    if i==worker:
                       L[i]+=P[i][f]    
    print(P)
    print(L)
    return P,L,end
#计算CP
def calculate_CP(P):
    # CP=np.zeros((order+1,station+1))
    for i in range(1,order+1):
        for f in range(1,station+1):
           if f==1:
               CP[i][f]=P[i][f]
           else:
               CP[i][f]=P[i][f]+CP[i][f-1]
    print("niuniu")
    print(CP)
    return CP 
   
def calculate_D(CP,L,end):
    # D=np.zeros((order+1,station+1))
    # CD=np.zeros((order+1,station+1))
    # start=np.zeros((order+1))
    # terminal=np.zeros((order+1))
    # leave=np.zeros((order+1,station+1))
   #初始化
    print(L)
    for f in range(station+1):
        D[1][f]=0
        CD[1][f]=0
        D[2][f]=0
        CD[2][f]=0
    for i in range(1,order+1):
        D[i][station]=0
    start[1]=0
    for i in range(2,worker+2):
        start[i]=start[i-1]+L[i-1]
    print(start)
    for i in range(3,worker+1):
        for f in range(int(end[i])):
            D[i][f]=0
    
    for i in range(1,order+1):
        if i<worker+1:
            for f in range(station+1):
                if f==0:
                   D[i][f]=0
                   CD[i][f]=D[i][f]
                elif f>=end[i] and i>2 and i<worker and f!=station :
                #    D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-start[i]-start[i]+start[i+1]-CP[i][f]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                #    start[i]=start[i-1]+CP[i-1][f]+CD[i-1][f]
                # elif f<station:
                #    D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                #    CD[i][f]=D[i][f]+CD[i][f-1]
                elif i==worker and f!=station:
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]+start[worker+1]-start[i]-CP[i][f]-start[i]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                elif f==station:
                   CD[i][f]=CD[i][f-1]
                   if i!=1:
                      terminal[i]=start[i]+CP[i][f]+CD[i][f]+start[worker+1]-start[i+1]
                   else:
                      terminal[i]=start[i]+CP[i][f]+CD[i][f]
                # leave[i][f]=start[i]+CP[i][f]+CD[i][f]

        # elif i>worker :
        #     for f in range(station+1):
        #         if f==0:
        #            D[i][f]=max(start[i-1]+CD[i-1][f+1]+CP[i-1][f+1],0)
        #            CD[i][f]=D[i][f]
        #         elif f==1:
        #            D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
        #            CD[i][f]=D[i][f]+CD[i][f-1]
        #            start[i]=start[i-1]+CP[i-1][f]+CD[i-1][f]
        #         elif f<station:
        #            D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
        #            CD[i][f]=D[i][f]+CD[i][f-1]
        #         else:
        #            CD[i][f]=CD[i][f-1]
        #            terminal[i]=start[i]+CP[i][f]+CD[i][f]
        #         leave[i][f]=start[i]+CP[i][f]+CD[i][f]
                
        else:
            print("niuniu")
            if i!=worker+1:
                start[i]=terminal[i-worker]
            for f in range(station+1):
                if f==0:
                   D[i][f]=max(start[i-1]+CD[i-1][f+1]+CP[i-1][f+1],0)
                   CD[i][f]=D[i][f] 
                elif f==1:
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                elif f<station:
                   D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                   CD[i][f]=D[i][f]+CD[i][f-1]
                else:
                   CD[i][f]=CD[i][f-1]
                   terminal[i]=start[i]+CP[i][f]+CD[i][f]
                leave[i][f]=start[i]+CP[i][f]+CD[i][f]
    print("leave")
    print(leave)
    # print(CD)
    # print(D)
    print(start)
    print(terminal)
    
#    for i in range(1,order+1):
#         if i==1:
#             start[i]=0
#         elif i<N:
#             start[i]=start[i-1]+CP[i-1][1]+CD[i-1][1]
#         else:
#             start[i]=terminal[i-n]                   
# def objective_function():
#     worker_speed=cal_worker_speed()
#     product_station=cal_station_data()
#     processing_time=cal_processing_time(worker_speed,product_station)
#     worker_sequence,pos=cal_worker_sequence()
#     P,L,end=calculate_P(worker_sequence,pos,processing_time)
#     CP=calculate_CP(P)
#     calculate_D(CP,L,end)
#     return terminal[order]
#目标函数
if __name__ == "__main__":
    worker_speed=cal_worker_speed()
    product_station=cal_station_data()
    processing_time=cal_processing_time(worker_speed,product_station)
    worker_sequence,pos=cal_worker_sequence()
    P,L,end=calculate_P(worker_sequence,pos,processing_time)
    CP=calculate_CP(P)
    calculate_D(CP,L,end)

    # worker_sequence=np.zeros((worker+1,station+1))
# np.savetxt("test.csv", worker_sequence, delimiter=",")

      
          

#     num2=np.random.randint(num,num+1)
#     for j in range()

