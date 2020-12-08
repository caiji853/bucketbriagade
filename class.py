import numpy as np
import math
import random
import scipy.stats
import csv
class Bucketbrigade(object):
    # self.worker_speed=[]
    # self.product_station=[]
    # self.processing_time=[[[0 for i in range(self.station)] for i in range(self.worker) ] for i in range(self.order)]
    # self.worker_sequence=np.zeros((self.worker+1,self.station+1))
    # self.pos=random.sample(range(1,self.worker+1),self.worker)
    # self.P=np.zeros((self.order+1,self.station+1))
    # self.L=np.zeros((self.worker+1))
    # self.end=np.zeros((self.worker+1))
    # self.CP=np.zeros((self.order+1,self.station+1))
    # self.D=np.zeros((self.order+1,self.station+1))
    # self.CD=np.zeros((self.order+1,self.station+1))
    # self.start=np.zeros((self.order+1))
    # self.terminal=np.zeros((self.order+1))
    # self.leave=np.zeros((self.order+1,self.station+1))
    def __init__(self,worker,station,order):
        self.worker=worker
        self.station=station
        self.order=order
        self.worker_speed=[]
        self.product_station=[]
        self.processing_time=[[[0 for i in range(self.station)] for i in range(self.worker) ] for i in range(self.order)]
        self.worker_sequence=np.zeros((self.worker+1,self.station+1))
        self.pos=random.sample(range(1,self.worker+1),self.worker)
        self.P=np.zeros((self.order+1,self.station+1))
        self.L=np.zeros((self.worker+1))
        self.end=np.zeros((self.worker+1))
        self.CP=np.zeros((self.order+1,self.station+1))
        self.D=np.zeros((self.order+1,self.station+1))
        self.CD=np.zeros((self.order+1,self.station+1))
        self.start=np.zeros((self.order+1))
        self.terminal=np.zeros((self.order+1))
        self.leave=np.zeros((self.order+1,self.station+1))
        self.PW=np.zeros((self.order+1,self.worker+1))
    def cal_station(self):
        lower = 0
        upper = 1
        sigma = 0.1
        mu = 1/self.station
        result=[]
        summary=0
        flag=0
        flag_new=0
        # o=0
        while  flag_new==0 or flag==1:
            if flag==1:
                result=[]
            for i in range(self.station-1):
            
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
                elif i==self.station-2:
                    flag=0
                    flag_new=1
                else:
                    pass
        result.append(round(1-summary,2))
        print(result)
        return result
    def cal_worker_speed(self):
        #!/usr/bin/python3
        # -*- coding: utf-8 -*-
        # 导入CSV安装包
        # 1. 创建文件对象
        # i=0
        f = open('worker.csv', 'w',newline='',encoding="utf-8")# 2. 基于文件对象构建 csv写入对象
        csv_write= csv.writer(f)
        # 3. 构建列表
        for i in range(self.worker):
            csv_write.writerow(np.random.randint(1,10,self.station))
            print(np.random.randint(1,10,self.station))
        # 4. 写入csv文件内容
        # 5. 关闭文件
        f.close()
        self.worker_speed = np.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
        print(self.worker_speed)
        # return worker_speed
    def cal_station_data(self):
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
        for o in range(self.order):
            result=self.cal_station()
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
        self.product_station=np.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
        print(self.product_station)
        # return product_station
    def cal_processing_time(self):
        # worker_speed = np.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
        # print(worker_speed)
        # product_station=np.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
        # print(product_station)
        self.order=len(self.product_station)
        self.station=len(self.product_station[0])
        self.worker=len(self.worker_speed)
        # processing_time=[[[0 for i in range(station)] for i in range(worker) ] for i in range(order)]
        # print(processing_time)
        for i in range(self.order):
            for w in range(self.worker):
                for f in range(self.station):
                    self.processing_time[i][w][f]=round(self.product_station[i][f]*60/self.worker_speed[w][f],2)
        # print(processing_time)
        # numpy.savetxt('processing_time.csv', processing_time, delimiter = ',')
        tmp = open('processing_time.csv', 'w',newline='',encoding="utf-8") # a表示在最后一行后面追加  #newline以免出现写一行空一行 #encoding 解决不能写入的错误
        csv_write = csv.writer(tmp) #csv_write.writerow(['id', 'eng_socre']) 写入列名
        for  item in self.processing_time:
            csv_write.writerow(item)
        tmp.close()
        print('over')
        print(self.processing_time)
        # return processing_time
    def cal_worker_sequence(self):
        # worker_sequence=np.zeros((worker+1,station+1))
        # pos=random.sample(range(1,worker+1),worker)
        print(self.pos)
        self.worker_sequence[self.pos[self.worker-1]][self.station]=1
        for i in range(1,self.worker+1):
            #     pos=np.random.randint(1,worker+1,worker)
            count=0
            if i==1:
                start_pos=1
                end_pos=np.random.randint(1,self.station+1-(self.worker-i-1))
            elif i < self.worker:
                end_pos1=np.random.randint(end_pos,self.station-(self.worker-i-1)) 
                for j in range(1,self.worker+1):
                    if self.worker_sequence[j][end_pos]==1:
                        count+=1
                if  count<2 and end_pos1-end_pos>=1:
                    start_pos=np.random.randint(end_pos,end_pos+1)  
                elif count<2 and end_pos1==end_pos:
                    start_pos=end_pos
                else:
                    start_pos=end_pos+1
                    end_pos1=np.random.randint(start_pos,self.station-(self.worker-i-1)) 
                    print(start_pos)
                end_pos=end_pos1
            elif i==self.worker-1:
                end_pos1=np.random.randint(end_pos,self.station-1-(self.worker-i-1)) 
                for j in range(1,self.worker+1):
                        if self.worker_sequence[j][end_pos]==1:
                            count+=1
                if  count<2 and end_pos1-end_pos>=1:
                    start_pos=np.random.randint(end_pos,end_pos+1)  
                elif count<2 and end_pos1==end_pos:
                    start_pos=end_pos
                else:
                    start_pos=end_pos+1
                    end_pos1=np.random.randint(start_pos,self.station-(self.worker-i-1)) 
                end_pos=end_pos1
            else:
                for j in range(1,self.worker+1):
                    if self.worker_sequence[j][end_pos]==1:
                        count+=1
                if  count<2 :
                    start_pos=np.random.randint(end_pos,end_pos+1)
                else:
                    start_pos=end_pos+1
                    
                end_pos=self.station
            for j in range(start_pos,end_pos+1):
                self.worker_sequence[self.pos[i-1]][j]=1
        print(self.worker_sequence)
        # return worker_sequence,pos
#计算P
    def calculate_P(self):
        # P=np.zeros((order+1,station+1))
        # L=np.zeros((worker+1))
        # end=np.zeros((worker+1))
       
            for m in range(self.worker-1,0,-1): 
                    position=self.station
                    print(self.pos[m])
                    posi=int(self.worker_sequence[self.pos[m]][position])
                    while posi==0:
                        position-=1
                        posi=int(self.worker_sequence[self.pos[m]][position])
                    self.end[self.worker-m]=position
                    print(position)
                    for f in range(1,position):
                        self.P[self.worker-m][f]=np.round(self.processing_time[self.worker-m-1][self.pos[m]-1][f-1],2)
                        self.L[self.worker-m]+=self.P[self.worker-m][f]
                        self.PW[self.worker-m][self.pos[m]]+=self.P[self.worker-m][f]
                    # for o in range(1,self.worker+1):
                    #     if o!=self.pos[m] and m!=self.worker-1:
                    #         for j in range(m+1,self.worker):
                    #             if o==self.pos[j] and self.worker_sequence[self.pos[j]][position]==1:
                    #                 ran=random.random()
                    #                 time=round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1]*ran,2)
                    #                 self.P[self.worker-m][position]=time+round(self.processing_time[self.worker-m-1][self.pos[j]-1][position-1]*(1-ran),2)
                    #                 self.L[self.worker-m]+=time
                    #     elif m==self.worker-1:
                    #         self.P[self.worker-m][position]=np.round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1],2)
                            # L[worker-m]+=P[worker-m][position]
                    for o in range(m+1,self.worker):
                        if self.worker_sequence[self.pos[o]][position]==1:
                            ran=random.random()
                            time=round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1]*ran,2)
                            self.P[self.worker-m][position]=time+round(self.processing_time[self.worker-m-1][self.pos[o]-1][position-1]*(1-ran),2)
                            self.L[self.worker-m]+=time
                            self.PW[self.worker-m][self.pos[m]]+=time
                            self.PW[self.worker-m][self.pos[o]]+=round(self.processing_time[self.worker-m-1][self.pos[o]-1][position-1]*(1-ran),2)                      

                    for f in range(position+1,self.station+1):
                        flag=0
                        for o in range(1,self.worker+1):
                            for p in range(o+1,self.worker+1):
                                if self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]==1 :
                                    ran=random.random()
                                    flag=1
                                    self.P[self.worker-m][f]=np.round(self.processing_time[self.worker-m-1][o-1][f-1]*ran+self.processing_time[self.worker-m-1][p-1][f-1]*(1-ran),2)
                                    self.PW[self.worker-m][o]+=round(self.processing_time[self.worker-m-1][o-1][f-1]*ran,2)
                                    self.PW[self.worker-m][p]+=round(self.processing_time[self.worker-m-1][p-1][f-1]*(1-ran),2)
                                elif self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]!=1:
                                    flag=0
                                    posi=o 
                        if flag==0:
                            self.P[self.worker-m][f]=np.round(self.processing_time[self.worker-m-1][posi-1][f-1],2)
                            self.PW[self.worker-m][posi]+=round(self.processing_time[self.worker-m-1][posi-1][f-1],2)
                    if m==self.worker-1:
                            self.P[self.worker-m][position]=np.round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1],2)
                            self.L[self.worker-m]+=self.P[self.worker-m][position]
                            self.PW[self.worker-m][self.pos[m]]+=self.P[self.worker-m][position]
            
            position=self.station
            # print(pos[0])
            posi=int(self.worker_sequence[self.pos[0]][position])
            while posi==0:
                position-=1
                posi=int(self.worker_sequence[self.pos[0]][position])
            self.end[self.worker]=position
            for i in range(self.worker,self.order+1):
                for f in range(1,self.station+1):
                        flag=0
                        for o in range(1,self.worker+1):
                            for p in range(o+1,self.worker+1):
                                if self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]==1:
                                    ran=random.random()
                                    flag=1
                                    time=round(self.processing_time[i-1][o-1][f-1]*ran,2)
                                    self.P[i][f]=round(self.processing_time[i-1][o-1][f-1]*ran+self.processing_time[i-1][p-1][f-1]*(1-ran),2)
                                    self.PW[i][o]+=round(self.processing_time[i-1][o-1][f-1]*ran,2)
                                    self.PW[i][p]+=round(self.processing_time[i-1][p-1][f-1]*(1-ran),2)
            
                                    if i == self.worker:
                                        self.L[i]+=time

                                elif  self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]!=1:
                                    flag=0
                                    posi=o 
                        if flag==0:
                            self.P[i][f]=np.round(self.processing_time[i-1][posi-1][f-1],2)
                            self.PW[i][posi]+=round(self.processing_time[i-1][posi-1][f-1],2)
                            if i==self.worker:
                                self.L[i]+=self.P[i][f]
            
        
        # return P,L,end
#计算CP
    def calculate_CP(self):
        # CP=np.zeros((order+1,station+1))
        for i in range(1,self.order+1):
            for f in range(1,self.station+1):
                if f==1:
                    self.CP[i][f]=self.P[i][f]
                else:
                    self.CP[i][f]=self.P[i][f]+self.CP[i][f-1]
        print("niuniu")
        print(self.CP)
        # return CP 
   
    def calculate_D(self):
        # D=np.zeros((order+1,station+1))
        # CD=np.zeros((order+1,station+1))
        # start=np.zeros((order+1))
        # terminal=np.zeros((order+1))
        # leave=np.zeros((order+1,station+1))
        #初始化
        print(self.L)
        for f in range(self.station+1):
            self.D[1][f]=0
            self.CD[1][f]=0
            self.D[2][f]=0
            self.CD[2][f]=0
        for i in range(1,self.order+1):
            self.D[i][self.station]=0
        self.start[1]=0
        for i in range(2,self.worker+2):
            self.start[i]=self.start[i-1]+self.L[i-1]
        print(self.start)
        for i in range(3,self.worker+1):
            for f in range(int(self.end[i])):
                self.D[i][f]=0
        
        for i in range(1,self.order+1):
            if i<self.worker+1:
                for f in range(self.station+1):
                    if f==0:
                        self.D[i][f]=0
                        self.CD[i][f]=self.D[i][f]
                    elif f>=self.end[i] and i>2 and i<self.worker and f!=self.station :
                    #    D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                        self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]-self.start[i]-self.start[i]+self.start[i+1]-self.CP[i][f]-self.CD[i][f-1],0)
                        self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
                    #    start[i]=start[i-1]+CP[i-1][f]+CD[i-1][f]
                    # elif f<station:
                    #    D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
                    #    CD[i][f]=D[i][f]+CD[i][f-1]
                    elif i==self.worker and f!=self.station:
                        self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]+self.start[self.worker+1]-self.start[i]-self.CP[i][f]-self.start[i]-self.CD[i][f-1],0)
                        self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
                    elif f==self.station:
                        self.CD[i][f]=self.CD[i][f-1]
                    if i!=1:
                        self.terminal[i]=self.start[i]+self.CP[i][f]+self.CD[i][f]+self.start[self.worker+1]-self.start[i+1]
                    else:
                        self.terminal[i]=self.start[i]+self.CP[i][f]+self.CD[i][f]
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
                if i!=self.worker+1:
                    self.start[i]=self.terminal[i-self.worker]
                for f in range(self.station+1):
                    if f==0:
                        self.D[i][f]=max(self.start[i-1]+self.CD[i-1][f+1]+self.CP[i-1][f+1]-self.start[i],0)
                        self.CD[i][f]=self.D[i][f] 
                    elif f==1:
                        self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]-self.CP[i][f]-self.start[i]-self.CD[i][f-1],0)
                        self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
                    elif f<self.station:
                        self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]-self.CP[i][f]-self.start[i]-self.CD[i][f-1],0)
                        self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
                    else:
                        self.CD[i][f]=self.CD[i][f-1]
                        self.terminal[i]=self.start[i]+self.CP[i][f]+self.CD[i][f]
                    self.leave[i][f]=self.start[i]+self.CP[i][f]+self.CD[i][f]
        print("leave")
        print(self.leave)
        print(self.CD)
        # print(D)
        print(self.start)
        print(self.terminal)
    def objective_function(self):
        # print("niuniu")
        self.cal_worker_speed()
        # print("niuniu")
        self.cal_station_data()
        self.cal_processing_time()
        self.cal_worker_sequence()
        self.calculate_P()
        self.calculate_CP()
        self.calculate_D()
        return self.terminal[self.order]
if __name__ == "__main__":
    bucket=Bucketbrigade(5,8,20)
    obj=bucket.objective_function()
    # obj=bucket.objective_function()
    print(obj)