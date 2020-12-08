import numpy as np
import math
import random
import scipy.stats
import csv
class population(object):
    def __init__(self,worker,station):
        self.worker=worker
        self.station=station
        self.worker_speed=[]
        self.product_station=[]
        self.worker_sequence=np.zeros((self.worker+1,self.station+1),dtype=int)
        self.pos=random.sample(range(1,self.worker+1),self.worker)
        self.L=np.zeros((self.worker+1),dtype=float)
        self.end=np.zeros((self.worker+1),dtype=int)
        self.begin=np.zeros((self.worker+1),dtype=int)        
    def cal_worker_sequence(self):
            # worker_sequence=np.zeros((worker+1,station+1))
            # pos=random.sample(range(1,worker+1),worker)
            # print(self.pos)
            self.worker_sequence[self.pos[self.worker-1]][self.station]=1
            for i in range(0,self.worker):
            #     pos=np.random.randint(1,worker+1,worker)
                count=0
                if i==0:
                    self.begin[i]=1
                    self.end[i]=np.random.randint(1,self.station-(self.worker-i-1))
                elif i==1:
                    if self.end[i-1]!=self.begin[i-1]:
                        end_pos1=np.random.randint(self.end[i-1],self.station-(self.worker-i-1))
                    else:
                        end_pos1=np.random.randint(self.end[i-1]+1,self.station-(self.worker-i-1))    
                    for j in range(1,self.worker+1):
                        if self.worker_sequence[j][self.end[i-1]]==1:
                            count+=1
                    if  count<2 and end_pos1-self.end[i-1]>=1:
                        self.begin[i]=np.random.randint(self.begin[i-1],self.end[i-1]+2)  
                    elif count<2 and end_pos1==self.end[i-1] and self.end[i-1]-self.end[i-2]>=2:
                        self.begin[i]=np.random.randint(self.end[i-2]+2,self.end[i-1]+1)
                    elif count<2 and end_pos1==self.end[i-1] and self.end[i-1]-self.end[i-2]<2:
                        self.begin[i]=np.random.randint(self.end[i-2]+1,self.end[i-1]+1)    
                    else:
                        self.begin[i]=self.end[i-1]+1
                        end_pos1=np.random.randint(self.begin[i],self.station-(self.worker-i-1)) 
                        print(self.begin[i])
                    if self.worker!=2:    
                        self.end[i]=end_pos1
                    else:
                        self.end[i]=self.station
                elif i < self.worker-2:
                    if self.end[i-1]!=self.begin[i-1]:
                        end_pos1=np.random.randint(self.end[i-1],self.station-(self.worker-i-1))
                    else:
                        end_pos1=np.random.randint(self.end[i-1]+1,self.station-(self.worker-i-1)) 
                    for j in range(1,self.worker+1):
                        if self.worker_sequence[j][self.end[i-1]]==1:
                            count+=1
                    if  count<2 and end_pos1-self.end[i-1]>=1:
                        self.begin[i]=np.random.randint(self.end[i-2]+1,self.end[i-1]+2)  
                    elif count<2 and end_pos1==self.end[i-1] and self.end[i-1]-self.end[i-2]>=2:
                        self.begin[i]=np.random.randint(self.end[i-2]+2,self.end[i-1]+1)
                    elif count<2 and end_pos1==self.end[i-1] and self.end[i-1]-self.end[i-2]<2:
                        self.begin[i]=np.random.randint(self.end[i-2]+1,self.end[i-1]+1)    
                    else:
                        self.begin[i]=self.end[i-1]+1
                        end_pos1=np.random.randint(self.begin[i],self.station-(self.worker-i-1)) 
                        print(self.begin[i])
                    self.end[i]=end_pos1
                elif i==self.worker-2:
                    if self.end[i-1]!=self.begin[i-1]:
                        end_pos1=np.random.randint(self.end[i-1],self.station+1-(self.worker-i-1))
                    else:
                        end_pos1=np.random.randint(self.end[i-1]+1,self.station+1-(self.worker-i-1)) 
                    for j in range(1,self.worker+1):
                        if self.worker_sequence[j][self.end[i-1]]==1:
                            count+=1
                    if  count<2 and end_pos1-self.end[i-1]>=1:
                        self.begin[i]=np.random.randint(self.end[i-2]+1,self.end[i-1]+2)  
                    elif count<2 and end_pos1==self.end[i-1] and self.end[i-1]-self.end[i-2]>=2:
                        self.begin[i]=np.random.randint(self.end[i-2]+2,self.end[i-1]+1)
                    elif count<2 and end_pos1==self.end[i-1] and self.end[i-1]-self.end[i-2]<2:
                        self.begin[i]=np.random.randint(self.end[i-2]+1,self.end[i-1]+1)    
                    else:
                        self.begin[i]=self.end[i-1]+1
                        end_pos1=np.random.randint(self.begin[i],self.station+1-(self.worker-i-1)) 
                        print(self.begin[i])
                    self.end[i]=end_pos1
                else:
                    for j in range(1,self.worker+1):
                        if self.worker_sequence[j][self.end[i-1]]==1:
                            count+=1
                    if  count<2 :
                        if self.end[i-1]!=self.station:
                            self.begin[i]=np.random.randint(self.end[i-2]+1,self.end[i-1]+2)
                        else:
                            self.begin[i]=np.random.randint(self.end[i-2]+1,self.end[i-1]+1)
                    else:
                        self.begin[i]=self.end[i-1]+1
                        
                    self.end[i]=self.station
                for j in range(self.begin[i],self.end[i]+1):
                    self.worker_sequence[self.pos[i]][j]=1
            return self.worker_sequence
    def func(self):
        worker_sequence=self.cal_worker_sequence()
        worker_sequence2=np.copy(worker_sequence)  
        print(worker_sequence2)     
        for i in range(1,self.worker+1):
            for j in range(1,self.station+1):
                self.worker_sequence[i][j]=0
        self.pos=random.sample(range(1,self.worker+1),self.worker)
        worker_sequence3=self.cal_worker_sequence()
        print(worker_sequence3)
        worker_sequence4= worker_sequence2 & worker_sequence3
        print(worker_sequence4)

        
if __name__ == "__main__":
    bucket=population(3,5)
    bucket.func()        
        