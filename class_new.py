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
        self.worker_sequence=np.zeros((self.worker+1,self.station+1),dtype=int)
        self.pos=random.sample(range(1,self.worker+1),self.worker)
        self.P=np.zeros((self.order+1,self.station+1))
        self.L=np.zeros((self.worker+1),dtype=float)
        self.end=np.zeros((self.worker+1),dtype=int)
        self.begin=np.zeros((self.worker+1),dtype=int)
        self.CP=np.zeros((self.order+1,self.station+1))
        self.D=np.zeros((self.order+1,self.station+1))
        self.CD=np.zeros((self.order+1,self.station+1))
        self.start=np.zeros((self.order+1))
        self.terminal=np.zeros((self.order+1))
        self.leave=np.zeros((self.order+1,self.station+1))
        self.leaveT=np.zeros((self.order+1,self.station+1))
        self.PW=np.zeros((self.order+1,self.worker+1))
        self.ran=np.zeros((self.station+1))
        self.haltime=np.zeros((self.order+1))
        self.starvation=np.zeros((self.order+1))
        self.et=np.zeros((self.order+1,self.station+1),dtype=float)
        self.e=np.zeros((self.order+1,self.station+1))
        self.CPT=np.zeros((self.order+1,self.station+1))
        self.CDT=np.zeros((self.order+1,self.station+1))
        self.DT=np.zeros((self.order+1,self.station+1))
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
        # print(result)
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
            # 
            
        # 4. 写入csv文件内容
        # 5. 关闭文件
        f.close()
        self.worker_speed = np.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
        # print(self.worker_speed)
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
        # print(station_data)
        tmp = open('data.csv', 'w',newline='',encoding="utf-8") #a表示在最后一行后面追加 #newline以免出现写一行空一行 #encoding 解决不能写入的错误
        csv_write = csv.writer(tmp) 
        #csv_write.writerow(['id', 'eng_socre']) 写入列名
        for  item in station_data:
            if item !=None:
                csv_write.writerow(item)
        tmp.close()
        # print('over')
        self.product_station=np.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
        # print(self.product_station)
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
        # print(self.processing_time)
        # return processing_time
    def cal_worker_sequence(self):
        # worker_sequence=np.zeros((worker+1,station+1))
        # pos=random.sample(range(1,worker+1),worker)
        # print(self.pos)
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
            self.start[1]=0
            for i in range(1,3,1): 
                    # position=self.station
                    # # print(self.pos[m])
                    # # posi=int(self.worker_sequence[self.pos[m]][position])
                    # # while posi==0:
                    #     position-=1
                    #     posi=int(self.worker_sequence[self.pos[m]][position])
                    # self.end[self.worker-m]=position
                    # print(position)
                    for f in range(1,int(self.end[self.worker-i])):
                        self.P[i][f]=self.processing_time[i-1][self.pos[self.worker-i]-1][f-1]
                        # print(self.P)
                        self.update_CP(i,f)
                        self.update_e(i,f)
                        self.update_D(i,f)
                        self.update_CD(i,f)
                        self.update_leave(i,f)
                        self.L[i]+=self.P[i][f]
                        self.PW[i][self.pos[self.worker-i]]+=self.P[i][f]
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
                    if  i==1:
                        self.P[i][int(self.end[self.worker-i])]=self.processing_time[i-1][int(self.pos[self.worker-i])-1][f-1]
                        self.update_CP(i,self.end[self.worker-i])
                        self.update_e(i,self.end[self.worker-i])
                        self.update_D(i,self.end[self.worker-i])
                        self.update_CD(i,self.end[self.worker-i])
                        self.update_leave(i,self.end[self.worker-i])
                        self.L[i]+=self.P[i][int(self.end[self.worker-i])]
                    elif self.worker_sequence[int(self.pos[self.worker-1])][int(self.end[self.worker-i])]==1:
                        self.ran[int(self.end[self.worker-i])]=0
                        # time=round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1]*ran,2)
                        self.P[i][int(self.end[self.worker-i])]=round(self.processing_time[i-1][int(self.pos[self.worker-i])-1][int(self.end[self.worker-i])-1]*self.ran[int(self.end[self.worker-i])]+self.processing_time[i-1][int(self.pos[self.worker-1])-1][int(self.end[self.worker-i])-1]*(1-self.ran[int(self.end[self.worker-i])]),2)
                        self.update_CP(i,self.end[self.worker-i])
                        self.update_e(i,self.end[self.worker-i])
                        self.update_D(i,self.end[self.worker-i])
                        self.update_CD(i,self.end[self.worker-i])
                        self.update_leave(i,self.end[self.worker-i])
                        self.L[i]+=0
                            # self.PW[self.worker-m][self.pos[m]]+=time
                            # self.PW[self.worker-m][self.pos[o]]+=round(self.processing_time[self.worker-m-1][self.pos[o]-1][position-1]*(1-ran),2)                      
                    elif self.worker_sequence[int(self.pos[self.worker-1])][int(self.end[self.worker-i])]!=1:
                        self.P[i][self.end[self.worker-i]]=round(self.processing_time[i-1][self.pos[self.worker-i]-1][self.end[self.worker-i]-1],2)
                        self.update_CP(i,self.end[self.worker-i])
                        self.update_e(i,self.end[self.worker-i])
                        self.update_D(i,self.end[self.worker-i])
                        self.update_CD(i,self.end[self.worker-i])
                        self.update_leave(i,self.end[self.worker-i])
                        self.L[i]+=self.P[i][self.end[self.worker-i]]
                    for f in range(int(self.end[self.worker-i])+1,self.station+1):
                        self.P[i][f]=round(self.processing_time[i-1][self.pos[self.worker-1]-1][f-1],2) 
                        self.update_CP(i,f)
                        self.update_e(i,f)
                        self.update_D(i,f)
                        self.update_CD(i,f)
                        self.update_leave(i,f)
                        self.L[i]+=0
                    self.start[i+1]=self.start[i]+self.L[i]    
            for i in range(3,self.worker+1):
                    for f in range(1,self.end[self.worker-i]):
                        self.P[i][f]=round(self.processing_time[i-1][self.pos[self.worker-i]-1][f-1],2)
                        self.update_CP(i,f)
                        self.update_e(i,f)
                        self.update_D(i,f)
                        self.update_CD(i,f)
                        self.update_leave(i,f)
                        self.L[i]+=self.P[i][f]
                    if self.worker_sequence[self.pos[self.worker-i+1]][self.end[self.worker-i]]==1:
                        self.ran[self.end[self.worker-i]]=0
                            # time=round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1]*ran,2)
                        self.P[i][self.end[self.worker-i]]=round(self.processing_time[i-1][self.pos[self.worker-i]-1][self.end[self.worker-i]-1]*self.ran[self.end[self.worker-i]]+self.processing_time[i-1][self.pos[self.worker-i+1]-1][self.end[self.worker-i]-1]*(1-self.ran[self.end[self.worker-i]]),2)
                        self.update_CP(i,self.end[self.worker-i])
                        self.update_e(i,self.end[self.worker-i])
                        self.update_D(i,self.end[self.worker-i])
                        self.update_CD(i,self.end[self.worker-i])
                        self.update_leave(i,self.end[self.worker-i])
                        self.L[i]+=0
                            # self.ran[self.end[self.pos[self.worker-i]]]=0
                            # # time=round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1]*ran,2)
                            # self.P[i][self.end[self.pos[self.worker-i]]]=round(self.processing_time[i-1][self.pos[worker-i]-1][self.end[self.pos[self.worker-i]]-1]*ran+self.processing_time[i-1][self.pos[worker-1]-1][self.end[self.pos[self.worker-i]]-1]*(1-ran),2)
                            # self.L[i]+=0   
                    elif self.worker_sequence[self.pos[self.worker-i+1]][self.end[self.worker-i]]!=1:
                        self.P[i][self.end[self.worker-i]]=round(self.processing_time[i-1][self.pos[self.worker-i]-1][self.end[self.worker-i]-1],2) 
                        self.update_CP(i,self.end[self.worker-i])
                        self.update_e(i,self.end[self.worker-i])
                        self.update_D(i,self.end[self.worker-i])
                        self.update_CD(i,self.end[self.worker-i])
                        self.update_leave(i,self.end[self.worker-i])
                        self.L[i]+= self.P[i][self.end[self.worker-i]]
                    self.start[i+1]=self.start[i]+self.L[i]
            print(self.start)
            #         for f in range(position+1,self.station+1):
            #             flag=0
            #             for o in range(1,self.worker+1):
            #                 for p in range(o+1,self.worker+1):
            #                     if self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]==1 :
            #                         ran=random.random()
            #                         flag=1
            #                         self.P[self.worker-m][f]=np.round(self.processing_time[self.worker-m-1][o-1][f-1]*ran+self.processing_time[self.worker-m-1][p-1][f-1]*(1-ran),2)
            #                         self.PW[self.worker-m][o]+=round(self.processing_time[self.worker-m-1][o-1][f-1]*ran,2)
            #                         self.PW[self.worker-m][p]+=round(self.processing_time[self.worker-m-1][p-1][f-1]*(1-ran),2)
            #                     elif self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]!=1:
            #                         flag=0
            #                         posi=o 
            #             if flag==0:
            #                 self.P[self.worker-m][f]=np.round(self.processing_time[self.worker-m-1][posi-1][f-1],2)
            #                 self.PW[self.worker-m][posi]+=round(self.processing_time[self.worker-m-1][posi-1][f-1],2)
            #         if m==self.worker-1:
            #                 self.P[self.worker-m][position]=np.round(self.processing_time[self.worker-m-1][self.pos[m]-1][position-1],2)
            #                 self.L[self.worker-m]+=self.P[self.worker-m][position]
            #                 # self.PW[self.worker-m][self.pos[m]]+=self.P[self.worker-m][position]
            
            # position=self.station
            # # print(pos[0])
            # posi=int(self.worker_sequence[self.pos[0]][position])
            # while posi==0:
            #     position-=1
            #     posi=int(self.worker_sequence[self.pos[0]][position])
            # self.end[self.worker]=position
            # for i in range(self.worker,self.order+1):
            #     for f in range(1,self.station+1):
            #             flag=0
            #             for o in range(1,self.worker+1):
            #                 for p in range(o+1,self.worker+1):
            #                     if self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]==1:
            #                         ran=random.random()
            #                         flag=1
            #                         time=round(self.processing_time[i-1][o-1][f-1]*ran,2)
            #                         self.P[i][f]=round(self.processing_time[i-1][o-1][f-1]*ran+self.processing_time[i-1][p-1][f-1]*(1-ran),2)
            #                         self.PW[i][o]+=round(self.processing_time[i-1][o-1][f-1]*ran,2)
            #                         self.PW[i][p]+=round(self.processing_time[i-1][p-1][f-1]*(1-ran),2)
            
            #                         if i == self.worker:
            #                             self.L[i]+=time

            #                     elif  self.worker_sequence[o][f]==1 and self.worker_sequence[p][f]!=1:
            #                         flag=0
            #                         posi=o 
            #             if flag==0:
            #                 self.P[i][f]=np.round(self.processing_time[i-1][posi-1][f-1],2)
            #                 self.PW[i][posi]+=round(self.processing_time[i-1][posi-1][f-1],2)
            #                 if i==self.worker:
            #                     self.L[i]+=self.P[i][f]
            
        
        # return P,L,end
#计算CP
    def iteration(self):
        for i in range(3,self.order-self.worker+2):
            for w in range(self.worker-2,-1,-1):
                if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                   for f in range(self.begin[w]+1,self.end[w]+1):
                        self.update_CPT(i+self.worker-w-2,f,self.pos[w])
                        self.update_et(i+self.worker-w-2,f)
                        self.update_DT(i+self.worker-w-2,f)
                        self.update_CDT(i+self.worker-w-2,f)
                        self.update_leaveT(i+self.worker-w-2,f)
                   print("star=",self.starvation)

                else:
                    for f in range(self.begin[w],self.end[w]+1):
                        self.update_CPT(i+self.worker-w-2,f,self.pos[w])
                        self.update_et(i+self.worker-w-2,f)
                        self.update_DT(i+self.worker-w-2,f)
                        self.update_CDT(i+self.worker-w-2,f)
                        self.update_leaveT(i+self.worker-w-2,f)
                    print("star=",self.starvation)
                if w==self.worker-2:
                    time=self.leave[i-1][self.station]
                print("CDT=",self.CDT)
                print("CPT=",self.CPT)
                print("et=",self.et)
                print("leaveT=",self.leaveT)
                if self.et[i+self.worker-w-2][self.end[w]]<=time and self.end[w]!=self.end[w-1]:
                    self.haltime[i+self.worker-w-2]=self.haltime[i+self.worker-w-2]+time-self.et[i+self.worker-w-2][self.end[w]]
                    if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                        for f in range(self.begin[w]+1,self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)

                    else:
                        for f in range(self.begin[w],self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)
                elif  self.e[i+self.worker-w-2][self.end[w]]<=time and self.end[w]==self.end[w-1]:
                    self.haltime[i+self.worker-w-2]=self.haltime[i+self.worker-w-2]+time-self.et[i+self.worker-w-2][self.end[w]]
                elif  self.et[i+self.worker-w-2][self.end[w]]>time and self.worker_sequence[self.pos[w+1]][self.end[w]]==1 and self.end[w]-self.begin[w]>=1:
                    if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1 and self.leave[i+self.worker-w-2][self.end[w]-1]<=time:
                        self.ran[self.end[w]]=round((time-self.leave[i+self.worker-w-2][self.end[w]-1])/(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]),2)
                        print(time)
                        print(self.leaveT[i+self.worker-w-2][self.end[w]-1])
                        print(self.et[i+self.worker-w-2][self.end[w]])
                        print(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1])
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])
                    elif self.worker_sequence[self.pos[w-1]][self.begin[w]]!=1 and self.leaveT[i+self.worker-w-2][self.end[w]-1]<=time:
                        self.ran[self.end[w]]=round((time-self.leaveT[i+self.worker-w-2][self.end[w]-1])/(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]),2)
                        print(time)
                        print(self.leaveT[i+self.worker-w-2][self.end[w]-1])
                        print(self.et[i+self.worker-w-2][self.end[w]])
                        print(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1])
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])  
                    elif self.worker_sequence[self.pos[w-1]][self.begin[w]]!=1 and self.leaveT[i+self.worker-w-2][self.end[w]-1]>time:
                        #饥饿
                        print("饥饿")
                        if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=max(self.et[i+self.worker-w-2][self.end[w]-1]-time,0)
                        self.ran[self.end[w]]=0
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])  
                        time=self.e[i+self.worker-w-2][self.end[w]-1]#更新time        
                    elif self.worker_sequence[self.pos[w-1]][self.begin[w]]==1 and self.leave[i+self.worker-w-2][self.end[w]-1]>time:
                        #饥饿
                        print("饥饿")
                        if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=max(self.e[i+self.worker-w-2][self.end[w]-1]-time,0)
                        self.ran[self.end[w]]=0
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])  
                        time=self.e[i+self.worker-w-2][self.end[w]-1]#更新time 
                elif self.et[i+self.worker-w-2][self.end[w]]>time and self.worker_sequence[self.pos[w+1]][self.end[w]]==1 and self.end[w]-self.begin[w]==0:
                    self.ran[self.end[w]]=round((time-self.start[i+self.worker-2])/(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]),2)
                    self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]),2)
                    self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                    self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                    self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                    self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                    self.update_leave(i+self.worker-w-2,self.end[w])  
                elif self.et[i+self.worker-w-2][self.end[w]]>time and self.worker_sequence[self.pos[w+1]][self.end[w]]!=1 and self.end[w]-self.begin[w]>=1:
                    #饥饿
                    print("饥饿")
                    if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=self.et[i+self.worker-w-2][self.end[w]]-time
                    self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1],2)
                    if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                        for f in range(self.begin[w]+1,self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)
                            # self.P[i+worker-w-2][self.end[w]]=round(self.processing_time[i+worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            # self.update_CP(i+worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            # self.update_e(i+worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            # self.update_D(i+worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            # self.update_CD(i+worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            # self.update_leave(i+worker-w-2,self.end[w])   
                    else:
                        for f in range(self.begin[w],self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)
                            # self.P[i+worker-w-2][self.end[w]]=round(self.processing_time[i+worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            # self.update_CP(i+worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            # self.update_e(i+worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            # self.update_D(i+worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            # self.update_CD(i+worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            # self.update_leave(i+worker-w-2,self.end[w])  
                           
                    time=self.e[i+self.worker-w-2][self.end[w]]  
                else:
                    #饥饿 
                        print("饥饿")
                        if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=self.et[i+self.worker-w-2][self.end[w]]-time 
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]!=1:
                            for f in range(self.begin[w],self.end[w]+1):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                        time=self.e[i+self.worker-w-2][self.end[w]] 
                if w==self.worker-2:
                    if self.worker_sequence[self.pos[w+1]][self.end[w]]==1:
                            for f in range(self.begin[w+1]+1,self.end[w+1]+1):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                    else:
                            for f in range(self.begin[w+1],self.end[w+1]+1):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
    
            self.start[i+self.worker-1]=time
            print("ran=",self.ran)
        for i in range(self.order-self.worker+2,self.order+1):
            for w in range(self.worker-2,i-self.order+self.worker-3,-1):
                if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                   for f in range(self.begin[w]+1,self.end[w]+1):
                        self.update_CPT(i+self.worker-w-2,f,self.pos[w])
                        self.update_et(i+self.worker-w-2,f)
                        self.update_DT(i+self.worker-w-2,f)
                        self.update_CDT(i+self.worker-w-2,f)
                        self.update_leaveT(i+self.worker-w-2,f)

                else:
                    for f in range(self.begin[w],self.end[w]+1):
                        self.update_CPT(i+self.worker-w-2,f,self.pos[w])
                        self.update_et(i+self.worker-w-2,f)
                        self.update_DT(i+self.worker-w-2,f)
                        self.update_CDT(i+self.worker-w-2,f)
                        self.update_leaveT(i+self.worker-w-2,f)
                if w==self.worker-2:
                    time=self.leave[i-1][self.station]
                print("et=",self.et)
                print("leaveT=",self.leaveT)
                if self.et[i+self.worker-w-2][self.end[w]]<=time and self.end[w]!=self.begin[w]:
                    self.haltime[i+self.worker-w-2]=self.haltime[i+self.worker-w-2]+time-self.et[i+self.worker-w-2][self.end[w]]
                    if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                        for f in range(self.begin[w]+1,self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)

                    else:
                        for f in range(self.begin[w],self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)
                
                elif  self.et[i+self.worker-w-2][self.end[w]]>time and self.worker_sequence[self.pos[w+1]][self.end[w]]==1 and self.end[w]-self.begin[w]>=1:
                    if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1 and self.leave[i+self.worker-w-2][self.end[w]-1]<=time:
                        self.ran[self.end[w]]=round((time-self.leave[i+self.worker-w-2][self.end[w]-1])/(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]),2)
                        print(time)
                        print(self.leaveT[i+self.worker-w-2][self.end[w]-1])
                        print(self.et[i+self.worker-w-2][self.end[w]])
                        print(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1])
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])
                    elif self.worker_sequence[self.pos[w-1]][self.begin[w]]!=1 and self.leaveT[i+self.worker-w-2][self.end[w]-1]<=time:
                        self.ran[self.end[w]]=round((time-self.leaveT[i+self.worker-w-2][self.end[w]-1])/(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]),2)
                        print(time)
                        print(self.leaveT[i+self.worker-w-2][self.end[w]-1])
                        print(self.et[i+self.worker-w-2][self.end[w]])
                        print(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1])
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])  
                    elif self.worker_sequence[self.pos[w-1]][self.begin[w]]!=1 and self.leaveT[i+self.worker-w-2][self.end[w]-1]>time:
                        #饥饿
                        print("饥饿")
                        if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=max(self.et[i+self.worker-w-2][self.end[w]-1]-time,0)
                        self.ran[self.end[w]]=0
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])  
                        time=self.e[i+self.worker-w-2][self.end[w]-1]#更新time        
                    elif self.worker_sequence[self.pos[w-1]][self.begin[w]]==1 and self.leave[i+self.worker-w-2][self.end[w]-1]>time:
                        #饥饿
                        print("饥饿")
                        if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=max(self.e[i+self.worker-w-2][self.end[w]-1]-time,0)
                        self.ran[self.end[w]]=0
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                            for f in range(self.begin[w]+1,self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])   
                        else:
                            for f in range(self.begin[w],self.end[w]):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                            self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,self.end[w])  
                        time=self.e[i+self.worker-w-2][self.end[w]-1]#更新time 
                elif self.et[i+self.worker-w-2][self.end[w]]>time and self.worker_sequence[self.pos[w+1]][self.end[w]]==1 and self.end[w]-self.begin[w]==0:
                    self.ran[self.end[w]]=round((time-self.start[i+self.worker-2])/(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]),2)
                    self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]),2)
                    self.update_CP(i+self.worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                    self.update_e(i+self.worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                    self.update_D(i+self.worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                    self.update_CD(i+self.worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                    self.update_leave(i+self.worker-w-2,self.end[w])  
                elif self.et[i+self.worker-w-2][self.end[w]]>time and self.worker_sequence[self.pos[w+1]][self.end[w]]!=1 and self.end[w]-self.begin[w]>=1:
                    #饥饿
                    print("饥饿")
                    if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=self.et[i+self.worker-w-2][self.end[w]]-time
                    self.P[i+self.worker-w-2][self.end[w]]=round(self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][self.end[w]-1],2)
                    if self.worker_sequence[self.pos[w-1]][self.begin[w]]==1:
                        for f in range(self.begin[w]+1,self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)
                            # self.P[i+worker-w-2][self.end[w]]=round(self.processing_time[i+worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            # self.update_CP(i+worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            # self.update_e(i+worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            # self.update_D(i+worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            # self.update_CD(i+worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            # self.update_leave(i+worker-w-2,self.end[w])   
                    else:
                        for f in range(self.begin[w],self.end[w]+1):
                            self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                            self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                            self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                            self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                            self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                            self.update_leave(i+self.worker-w-2,f)
                            # self.P[i+worker-w-2][self.end[w]]=round(self.processing_time[i+worker-w-2-1][self.pos[w]-1][self.end[w]-1]*self.ran[self.end[w]]+self.processing_time[i+worker-w-2-1][self.pos[w+1]-1][self.end[w]-1]*(1-self.ran[self.end[w]]))
                            # self.update_CP(i+worker-w-2,self.end[w])#更新CP[i+worker-w-2][f]
                            # self.update_e(i+worker-w-2,self.end[w])#更新e[i+worker-w-2][f]
                            # self.update_D(i+worker-w-2,self.end[w])#更新D[i+worker-w-2][f]
                            # self.update_CD(i+worker-w-2,self.end[w]) #更新CD[i+worker-w-2][f]
                            # self.update_leave(i+worker-w-2,self.end[w])  
                           
                    time=self.e[i+self.worker-w-2][self.end[w]]  
                else:
                    #饥饿 
                        print("饥饿")
                        if w!=self.worker-2:
                            for j in range(w+1,self.worker-1,1):
                                self.starvation[i+self.worker-j-2]+=self.et[i+self.worker-w-2][self.end[w]]-time 
                        if self.worker_sequence[self.pos[w-1]][self.begin[w]]!=1:
                            for f in range(self.begin[w],self.end[w]+1):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                        time=self.e[i+self.worker-w-2][self.end[w]] 
                if w==self.worker-2:
                    if self.worker_sequence[self.pos[w+1]][self.end[w]]==1:
                            for f in range(self.begin[w+1]+1,self.end[w+1]+1):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                    else:
                            for f in range(self.begin[w+1],self.end[w+1]+1):
                                self.P[i+self.worker-w-2][f]=self.processing_time[i+self.worker-w-2-1][self.pos[w+1]-1][f-1]
                                self.update_CP(i+self.worker-w-2,f)#更新CP[i+worker-w-2][f]
                                self.update_e(i+self.worker-w-2,f)#更新e[i+worker-w-2][f]
                                self.update_D(i+self.worker-w-2,f)#更新D[i+worker-w-2][f]
                                self.update_CD(i+self.worker-w-2,f) #更新CD[i+worker-w-2][f]
                                self.update_leave(i+self.worker-w-2,f)
                print("ran=",self.ran)

    def cal_position(self):
        for m in range(self.worker):
            position=self.station
            posi=int(self.worker_sequence[self.pos[m]][position])
            while posi==0:
                position-=1
                posi=int(self.worker_sequence[self.pos[m]][position])
            self.end[m]=position
        for m in range(self.worker):
            position=1
            posi=int(self.worker_sequence[self.pos[m]][position])
            while posi==0:
                position+=1
                posi=int(self.worker_sequence[self.pos[m]][position])     
            self.begin[m]=position
    
    def update_CP(self,i,f):
        # CP=np.zeros((order+1,station+1)
                if f==1:
                    self.CP[int(i)][int(f)]=self.P[int(i)][int(f)]
                else:
                    self.CP[int(i)][int(f)]=self.P[int(i)][int(f)]+self.CP[int(i)][int(f)-1]
                # print(self.CP)
        # return CP 
    def update_CPT(self,i,f,w):
        if f==1:
            self.CPT[int(i)][int(f)]=self.processing_time[int(i)-1][int(w)-1][int(f)-1]

        else:
            self.CPT[int(i)][int(f)]=self.CPT[int(i)][int(f)-1]+self.processing_time[int(i)-1][int(w)-1][int(f)-1]
    def update_DT(self,i,f):
        if i<=2:
            self.DT[int(i)][int(f)]=0
        elif i<=self.worker and f<self.begin[self.worker-i+1]-1:
            self.DT[int(i)][int(f)]=0
        elif   f>=self.begin[self.worker-1] and f <=self.end[self.worker-1]:
            self.DT[int(i)][int(f)]=0
        else:
            self.DT[i][f]=max(self.leave[i-1][f+1]-self.et[i][f],0)
    def update_CDT(self,i,f):
        if f!=0:
            self.CDT[int(i)][int(f)]=self.CDT[int(i)][int(f)-1]+self.DT[int(i)][int(f)]
        else:
            self.CDT[int(i)][int(f)]=self.DT[int(i)][int(f)]
    def update_D(self,i,f):
        if i<=2:
            self.D[int(i)][int(f)]=0
        elif i<=self.worker and f<self.begin[self.worker-i+1]-1:
            self.D[int(i)][int(f)]=0
        elif   f>=self.begin[self.worker-1] and f <=self.end[self.worker-1]:
            self.D[int(i)][int(f)]=0
        else:
            self.D[i][f]=max(self.leave[i-1][f+1]-self.e[i][f],0)
    def update_CD(self,i,f):
        if f!=0:
            self.CD[int(i)][int(f)]=self.CD[int(i)][int(f)-1]+self.D[int(i)][int(f)]
        else:
            self.CD[int(i)][int(f)]=self.D[int(i)][int(f)]
    def update_et(self,i,f):
        if i==1:
            self.et[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)-1]

        elif i==2 and f<self.begin[self.worker-1]:
            self.et[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)-1]
        elif i==2 and f>=self.begin[self.worker-1]:
            self.et[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)-1]
        elif i<=self.worker and f<self.begin[self.worker-i+1]:
           self.et[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][f]+self.CDT[int(i)][int(f)-1]
        elif i<=self.worker and f>=self.begin[self.worker-i+1]:
            self.et[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)-1]+self.haltime[int(i)]+self.starvation[int(i)]
        elif i<=self.worker and f==0:
           self.et[int(i)][int(f)]=self.start[int(i)]
        elif i>self.worker and f==0:
            self.et[int(i)][int(f)]=self.start[int(i)]+self.CDT[int(i)][int(f)-1]
        else:
           self.et[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)-1]+self.haltime[int(i)]+self.starvation[int(i)]  
    def update_e(self,i,f):
        if i==1:
            self.e[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)-1]

        elif i==2 and f<self.begin[self.worker-1]:
            self.e[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)-1]
        elif i==2 and f>=self.begin[self.worker-1]:
            self.e[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)-1]
        elif i<=self.worker and f<self.begin[self.worker-i+1]:
           self.e[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][f]+self.CD[int(i)][int(f)-1]
        elif i<=self.worker and f>=self.begin[self.worker-i+1]:
            self.e[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)-1]+self.haltime[int(i)]+self.starvation[int(i)]
        elif i<=self.worker and f==0:
           self.e[int(i)][int(f)]=self.start[int(i)]
        elif i>self.worker and f==0:
            self.e[int(i)][int(f)]=self.start[int(i)]+self.CD[int(i)][int(f)-1]
        else:
           self.e[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)-1]+self.haltime[int(i)]+self.starvation[int(i)] 
    def update_leave(self,i,f):
        if i==1:
            self.leave[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)]

        elif i==2 and f<self.begin[self.worker-1]:
            self.leave[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)]
        elif i==2 and f>=self.begin[self.worker-1]:
            self.leave[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)]
        elif i<=self.worker and f<self.begin[self.worker-i+1]:
           self.leave[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][f]+self.CD[int(i)][int(f)]
        elif i<=self.worker and f>=self.begin[self.worker-i+1]:
            self.leave[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)]+self.haltime[int(i)]+self.starvation[int(i)]
        elif i<=self.worker and f==0:
           self.leave[int(i)][int(f)]=self.start[int(i)]
        elif i>self.worker and f==0:
            self.leave[int(i)][int(f)]=self.start[int(i)]+self.CD[int(i)][int(f)]
        else:
           self.leave[int(i)][int(f)]=self.start[int(i)]+self.CP[int(i)][int(f)]+self.CD[int(i)][int(f)]+self.haltime[int(i)]+self.starvation[int(i)]   
    def update_leaveT(self,i,f):
        if i==1:
            self.leaveT[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)]

        elif i==2 and f<self.begin[self.worker-1]:
            self.leaveT[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)]
        elif i==2 and f>=self.begin[self.worker-1]:
            self.leaveT[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)]
        elif i<=self.worker and f<self.begin[self.worker-i+1]:
           self.leaveT[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][f]+self.CDT[int(i)][int(f)]
        elif i<=self.worker and f>=self.begin[self.worker-i+1]:
            self.leaveT[int(i)][int(f)]=self.start[int(i)]+self.start[self.worker+1]-self.start[int(i)+1]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)]+self.haltime[int(i)]+self.starvation[int(i)]
        elif i<=self.worker and f==0:
           self.leaveT[int(i)][int(f)]=self.start[int(i)]
        elif i>self.worker and f==0:
            self.leaveT[int(i)][int(f)]=self.start[int(i)]+self.CDT[int(i)][int(f)]
        else:
           self.leaveT[int(i)][int(f)]=self.start[int(i)]+self.CPT[int(i)][int(f)]+self.CDT[int(i)][int(f)]+self.haltime[int(i)]+self.starvation[int(i)]   
    # def calculate_start(self):
    #     # D=np.zeros((order+1,station+1))
    #     # CD=np.zeros((order+1,station+1))
    #     # start=np.zeros((order+1))
    #     # terminal=np.zeros((order+1))
    #     # leave=np.zeros((order+1,station+1))
    #     #初始化
    #     # print(self.L)
    #     # for f in range(self.station+1):
    #     #     self.D[1][f]=0
    #     #     self.CD[1][f]=0
    #     #     self.D[2][f]=0
    #     #     self.CD[2][f]=0
    #     # for i in range(1,self.order+1):
    #     #     self.D[i][self.station]=0
    #     # self.start[1]=0
    #     for i in range(2,self.worker+2):
    #         self.start[i]=self.start[i-1]+self.L[i-1]
    #     print(self.start)
        # for i in range(3,self.worker+1):
        #     for f in range(int(self.end[i])):
        #         self.D[i][f]=0
        
        # for i in range(1,self.order+1):
        #     if i<self.worker+1:
        #         for f in range(self.station+1):
        #             if f==0:
        #                 self.D[i][f]=0
        #                 self.CD[i][f]=self.D[i][f]
        #             elif f>=self.end[i] and i>2 and i<self.worker and f!=self.station :
        #             #    D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
        #                 self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]-self.start[i]-self.start[i]+self.start[i+1]-self.CP[i][f]-self.CD[i][f-1],0)
        #                 self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
        #             #    start[i]=start[i-1]+CP[i-1][f]+CD[i-1][f]
        #             # elif f<station:
        #             #    D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
        #             #    CD[i][f]=D[i][f]+CD[i][f-1]
        #             elif i==self.worker and f!=self.station:
        #                 self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]+self.start[self.worker+1]-self.start[i]-self.CP[i][f]-self.start[i]-self.CD[i][f-1],0)
        #                 self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
        #             elif f==self.station:
        #                 self.CD[i][f]=self.CD[i][f-1]
        #             if i!=1:
        #                 self.terminal[i]=self.start[i]+self.CP[i][f]+self.CD[i][f]+self.start[self.worker+1]-self.start[i+1]
        #             else:
        #                 self.terminal[i]=self.start[i]+self.CP[i][f]+self.CD[i][f]
        #             # leave[i][f]=start[i]+CP[i][f]+CD[i][f]

        #     # elif i>worker :
        #     #     for f in range(station+1):
        #     #         if f==0:
        #     #            D[i][f]=max(start[i-1]+CD[i-1][f+1]+CP[i-1][f+1],0)
        #     #            CD[i][f]=D[i][f]
        #     #         elif f==1:
        #     #            D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
        #     #            CD[i][f]=D[i][f]+CD[i][f-1]
        #     #            start[i]=start[i-1]+CP[i-1][f]+CD[i-1][f]
        #     #         elif f<station:
        #     #            D[i][f]=max(start[i-1]+CP[i-1][f+1]+CD[i-1][f+1]-CP[i][f]-start[i]-CD[i][f-1],0)
        #     #            CD[i][f]=D[i][f]+CD[i][f-1]
        #     #         else:
        #     #            CD[i][f]=CD[i][f-1]
        #     #            terminal[i]=start[i]+CP[i][f]+CD[i][f]
        #     #         leave[i][f]=start[i]+CP[i][f]+CD[i][f]
                    
        #     else:
        #         print("niuniu")
        #         if i!=self.worker+1:
        #             self.start[i]=self.terminal[i-self.worker]
        #         for f in range(self.station+1):
        #             if f==0:
        #                 self.D[i][f]=max(self.start[i-1]+self.CD[i-1][f+1]+self.CP[i-1][f+1]-self.start[i],0)
        #                 self.CD[i][f]=self.D[i][f] 
        #             elif f==1:
        #                 self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]-self.CP[i][f]-self.start[i]-self.CD[i][f-1],0)
        #                 self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
        #             elif f<self.station:
        #                 self.D[i][f]=max(self.start[i-1]+self.CP[i-1][f+1]+self.CD[i-1][f+1]-self.CP[i][f]-self.start[i]-self.CD[i][f-1],0)
        #                 self.CD[i][f]=self.D[i][f]+self.CD[i][f-1]
        #             else:
        #                 self.CD[i][f]=self.CD[i][f-1]
        #                 self.terminal[i]=self.start[i]+self.CP[i][f]+self.CD[i][f]
        #             self.leave[i][f]=self.start[i]+self.CP[i][f]+self.CD[i][f]
        # print("leave")
        # print(self.leave)
        # print(self.CD)
        # # print(D)
        # print(self.start)
        # print(self.terminal)
    def objective_function(self):
          self.cal_worker_speed()
          self.cal_station_data()
          self.cal_processing_time()
          self.cal_worker_sequence()
          self.cal_position()
          self.calculate_P()
        #   self.calculate_start()
          self.iteration()
    #     # self.cal_processing_time()
    #     # print("niuniu")
    #     # self.cal_worker_speed()
    #     # # print("niuniu")
    #     # self.cal_station_data()
    #     # self.cal_processing_time()
    #     # self.cal_worker_sequence()
    #     # self.calculate_P()
    #     # self.calculate_CP()
    #     # self.calculate_D()
    #     # return self.terminal[self.order]
          print("CD=",self.CD)
          print("leave=",self.leave)
if __name__ == "__main__":
    bucket=Bucketbrigade(5,8,20)
    bucket.objective_function()
    # # obj=bucket.objective_function()
    # print(obj)