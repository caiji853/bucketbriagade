import numpy as np
import math
import random
import csv
worker=5
station=8
order=20
#print(pos)
#print(pos[1])
def processing_time():
    worker_speed = np.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
    print(worker_speed)
    product_station=np.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
    print(product_station)
    product=len(product_station)
    station=len(product_station[0])
    worker=len(worker_speed)
    processing_time=[[[0 for i in range(station)] for i in range(worker) ] for i in range(product)]
    # print(processing_time)
    for i in range(product):
       for w in range(worker):
            for f in range(station):
                processing_time[i][w][f]=round(product_station[i][f]*60/worker_speed[w][f],2)
    # print(processing_time)
# numpy.savetxt('processing_time.csv', processing_time, delimiter = ',')
    tmp = open('processing_time.csv', 'w',newline='',encoding="utf-8") # a表示在最后一行后面追加
                                                            #newline以免出现写一行空一行
                                                            #encoding 解决不能写入的错误
    
    csv_write = csv.writer(tmp) 
#csv_write.writerow(['id', 'eng_socre']) 写入列名
    for  item in processing_time:
        csv_write.writerow(item)
    tmp.close()
    print('over')
    print(processing_time)
    return processing_time
def worker_sequence():
    worker_sequence=np.zeros((worker+1,station+1))
    pos=random.sample(range(1,worker+1),worker)
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
def calculate_P(worker_sequence,pos,processing_time):
    P=np.zeros((order+1,station+1))
    for m in range(worker-1,0,-1): 
            position=station
            print(pos[m])
            posi=int(worker_sequence[pos[m]][position])
            while posi==0:
                  position-=1
                  posi=int(worker_sequence[pos[m]][position])
            print(position)
            for f in range(1,position):
                 P[worker-m][f]=np.round(processing_time[worker-m-1][pos[m]-1][f-1],2)
            for o in range(1,worker+1):
                if o!=pos[m] and m!=worker-1:
                    for j in range(m+1,worker):
                        if o==pos[j] and worker_sequence[pos[j]][position]==1:
                            ran=random.random()
                            P[worker-m][position]=np.round(processing_time[worker-m-1][pos[m]-1][position-1]*ran+processing_time[worker-m-1][pos[j]-1][position-1]*(1-ran),2)
                elif m==worker-1:
                    P[worker-m][position]=np.round(processing_time[worker-m-1][pos[m]-1][position-1],2)
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
    for i in range(worker,order+1):
        for f in range(1,station+1):
                flag=0
                for o in range(1,worker+1):
                    for p in range(o+1,worker+1):
                        if worker_sequence[o][f]==1 and worker_sequence[p][f]==1:
                            ran=random.random()
                            flag=1
                            P[i][f]=np.round(processing_time[i-1][o-1][f-1]*ran+processing_time[i-1][p-1][f-1]*(1-ran),2)
                        elif  worker_sequence[o][f]==1 and worker_sequence[p][f]!=1:
                            flag=0
                            posi=o 
                if flag==0:
                    P[i][f]=np.round(processing_time[i-1][posi-1][f-1],2)
    print(P)
    return P
#计算D
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
            

#目标函数
if __name__ == "__main__":
    processing_time=processing_time()
    worker_sequence,pos=worker_sequence()
    calculate_P(worker_sequence,pos,processing_time)

    # worker_sequence=np.zeros((worker+1,station+1))
# np.savetxt("test.csv", worker_sequence, delimiter=",")

      
          

#     num2=np.random.randint(num,num+1)
#     for j in range()

