import numpy as np
import math
import random
import scipy.stats
import csv
import matplotlib.pyplot as plt
from model_latest import Bucketbrigade
    # print(obj)
class population(object):
    def __init__(self,worker,station,order,f,CR,generation):
        self.worker=worker
        self.station=station
        self.order=order
        self.f=f
        self.CR=CR
        self.generation=generation
        self.NP=int(self.worker*self.station*self.worker/10)
        self.population=[[[0 for i in range(self.station+1)] for i in range(self.worker+1) ] for i in range(self.NP)]
        self.mid_population=[[[0 for i in range(self.station+1)] for i in range(self.worker+1) ] for i in range(self.NP)]
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
    def initpopvfit(self):
            worker_sequence=self.cal_worker_sequence() 
            return worker_sequence
        
    def func_abstract(self,worker_sequence1,worker_sequence2):
        abstract_population=np.zeros((self.worker+1,self.station+1),dtype=int)
        for w in range(self.worker+1):
            for f in range(self.station+1):
                abstract_population[w][f]=worker_sequence1[w][f] and worker_sequence2[w][f]
        ran=random.random()
        position=random.randint(1,self.worker)
        if ran>self.f:
            position_new=random.randint(1,self.worker)
            while position_new==position:
                position_new=random.randint(1,self.worker)
            worker_newsequence=np.zeros((1,self.station+1),dtype=int)
            worker_newsequence[0][:self.station+1]=abstract_population[position][:self.station+1]
            abstract_population[position][:self.station+1]=abstract_population[position_new][:self.station+1]
            abstract_population[position_new][:self.station+1]=worker_newsequence[0][:self.station+1]
        
        return abstract_population
    def func_add(self,worker_sequence1,worker_sequence2):
        add_population=np.zeros((self.worker+1,self.station+1),dtype=int)
        for w in range(self.worker+1):
            for f in range(self.station+1):
                add_population[w][f]=worker_sequence1[w][f] or worker_sequence2[w][f]
        return add_population     
    def func_variation(self,population):
        v_population=[[[0 for i in range(self.station+1)] for i in range(self.worker+1) ] for i in range(self.NP)]
        for i in range(self.NP):
            r1=random.randint(0,self.NP-1)
            while r1==i:
                r1=random.randint(0,self.NP-1)
            r2=random.randint(0,self.NP-1)
            while r2==r1 or r2==i:
                r2=random.randint(0,self.NP-1)
            r3=random.randint(0,self.NP-1)
            while r3==r2 or r3==r1 or r3==i:
                r3=random.randint(0,self.NP-1)
            v_population[i]=self.func_add(population[r1],self.func_abstract(population[r2],population[r3]))

        return v_population
    def func_crossover(self,population,v_population):
        u_population=[[[0 for i in range(self.station+1)] for i in range(self.worker+1) ] for i in range(self.NP)]
        for i in range(0,self.NP):
            for j in range(1,self.worker+1):
                if random.random()<=self.CR or j==random.randint(1,self.worker):
                    u_population[i][j][:self.station+1]=v_population[i][j][:self.station+1]
                    
                else:
                    u_population[i][j][:self.station+1]=population[i][j][:self.station+1]
            pos_start,pos_end,u_population[i]=self.worker_repair(u_population[i],1)
        return u_population
    def func_selection(self,u_population,population):
        for i in range(0,self.NP):
            pos_start,pos_end,population[i]=self.worker_repair(population[i],0)
            newpos,pos_newstart,pos_newend=self.func_pos(pos_start,pos_end)
            bucket=Bucketbrigade(self.worker,self.station,self.order)
            bucket_population=bucket.objective_function(population[i],pos_newstart,pos_newend,newpos)
            pos_start,pos_end,u_population[i]=self.worker_repair(u_population[i],0)
            newpos,pos_newstart,pos_newend=self.func_pos(pos_start,pos_end)
            bucket=Bucketbrigade(self.worker,self.station,self.order)
            bucket_u_population=bucket.objective_function(u_population[i],pos_newstart,pos_newend,newpos)
            if bucket_u_population <= bucket_population:
                population[i]=u_population[i]
            else:
                population[i]=population[i]
        return population
    
    def worker_repair(self,worker_sequence,flag_change):
        print("niuniu=",worker_sequence)
        flag_new=0
        while flag_new==0 :
            for i in range(1,self.worker+1):
                pos_begin=0
                pos_end=self.station+1
                for f in range(1,self.station+1):
                    if worker_sequence[i][f]==1:
                        pos_begin=f
                        break
                for f in range(self.station,0,-1):
                    if worker_sequence[i][f]==1:
                        pos_end=f
                        break
                if pos_begin==0 and pos_end==self.station+1:
                    pos_begin=random.randint(1,3)
                    pos_end=random.randint(pos_begin,3)
                    for f in range(pos_begin,pos_end+1):
                        worker_sequence[i][f]=1
                    
                else:
                    for f in range(pos_begin,pos_end+1):
                        worker_sequence[i][f]=1
    
            fflag=1
            while fflag==1:
                for f in range(1,self.station+1):
                    pos_worker=[]
                    pos_count=0
                    for i in range(1,self.worker+1):
                        if worker_sequence[i][f]==1:
                            pos_worker.append(i)
                            pos_count+=1
                    if pos_count>2 and f!=self.station:
                        pos=0
                        while pos_count>2:
                            for f in range(1,f+1):
                                worker_sequence[pos_worker[pos]][f]=0
                            pos+=1
                            pos_count-=1
                        fflag=0
                    elif pos_count>=2 and f==self.station:
                        pos=0
                        while pos_count>=2:
                            worker_sequence[pos_worker[pos]][f]=0
                            pos+=1
                            pos_count-=1
                        fflag=0
                    elif pos_count==0:
                        pos=random.randint(1,self.worker)
                        print("pos=",pos)
                        worker_sequence[pos][f]=1
                        for ff in range(1,self.station+1):
                                if worker_sequence[pos][ff]==1:
                                    pos_begin=ff
                                    break
                        for ff in range(self.station,0,-1):
                                if worker_sequence[pos][ff]==1:
                                    pos_end=ff
                                    break
                        for ff in range(pos_begin,pos_end+1):
                                worker_sequence[pos][ff]=1
                        fflag=1
                        break
                    else:
                        fflag=0           
            for i in range(1,self.worker+1):
                pos_begin=0
                pos_end=self.station+1
                for f in range(1,self.station+1):
                    if worker_sequence[i][f]==1:
                        pos_begin=f
                        break
                for f in range(self.station,0,-1):
                    if worker_sequence[i][f]==1:
                        pos_end=f
                        break

                if pos_begin==0 and pos_end==self.station+1:
                    flag_new=0
                    break
                else:
                    flag_new=1
            if flag_new==0:
                for f in range(1,4):
                    for i in range(1,self.worker+1):
                        worker_sequence[i][f]=0
        flag_new_new=0
        while flag_new_new==0:
            flag_new=0
            while flag_new==0 :
                for i in range(1,self.worker+1):
                    pos_begin=0
                    pos_end=self.station+1
                    for f in range(1,self.station+1):
                        if worker_sequence[i][f]==1:
                            pos_begin=f
                            break
                    for f in range(self.station,0,-1):
                        if worker_sequence[i][f]==1:
                            pos_end=f
                            break
                    if pos_begin==0 and pos_end==self.station+1:
                        pos_begin=random.randint(1,3)
                        pos_end=random.randint(pos_begin,3)
                        for f in range(pos_begin,pos_end+1):
                            worker_sequence[i][f]=1
                        
                    else:
                        for f in range(pos_begin,pos_end+1):
                            worker_sequence[i][f]=1
        
                fflag=1
                while fflag==1:
                    for f in range(1,self.station+1):
                        pos_worker=[]
                        pos_count=0
                        for i in range(1,self.worker+1):
                            if worker_sequence[i][f]==1:
                                pos_worker.append(i)
                                pos_count+=1
                        if pos_count>2 and f!=self.station:
                            pos=0
                            while pos_count>2:
                                for f in range(1,f+1):
                                    worker_sequence[pos_worker[pos]][f]=0
                                pos+=1
                                pos_count-=1
                            fflag=0
                        elif pos_count>=2 and f==self.station:
                            pos=0
                            while pos_count>=2:
                                worker_sequence[pos_worker[pos]][f]=0
                                pos+=1
                                pos_count-=1
                            fflag=0
                        elif pos_count==0:
                            pos=random.randint(1,self.worker)
                            print("pos=",pos)
                            worker_sequence[pos][f]=1
                            for ff in range(1,self.station+1):
                                    if worker_sequence[pos][ff]==1:
                                        pos_begin=ff
                                        break
                            for ff in range(self.station,0,-1):
                                    if worker_sequence[pos][ff]==1:
                                        pos_end=ff
                                        break
                            for ff in range(pos_begin,pos_end+1):
                                    worker_sequence[pos][ff]=1
                            fflag=1
                            break
                        else:
                            fflag=0           
                for i in range(1,self.worker+1):
                    pos_begin=0
                    pos_end=self.station+1
                    for f in range(1,self.station+1):
                        if worker_sequence[i][f]==1:
                            pos_begin=f
                            break
                    for f in range(self.station,0,-1):
                        if worker_sequence[i][f]==1:
                            pos_end=f
                            break

                    if pos_begin==0 and pos_end==self.station+1:
                        flag_new=0
                        break
                    else:
                        flag_new=1
                if flag_new==0:
                    for f in range(1,4):
                        for i in range(1,self.worker+1):
                            worker_sequence[i][f]=0
            ffflag=1
            while ffflag==1:       
                for i in range(1,self.worker+1):
                    for j in range(1,self.worker+1):
                        pos=1
                        flag=0
                        for f in range(1,self.station+1):
                            if worker_sequence[j][f]==1:
                                pos_begin=f
                                break
                        for f in range(self.station,0,-1):
                            if worker_sequence[j][f]==1:
                                pos_end=f
                                break
                        if worker_sequence[i][pos_begin]!=1 and worker_sequence[i][pos_end]!=1:
                            for f in range(pos_begin+1,pos_end):
                                if worker_sequence[i][f]==1 and worker_sequence[j][f]==1:
                                    flag=1
                                    pos=f
                            if flag==1:
                                count=0
                                for m in range(1,self.worker+1):
                                    if worker_sequence[m][pos_begin]==1:
                                        count+=1
                                if count>=2:
                                    count=0
                                    for m in range(1,self.worker+1):
                                        if worker_sequence[m][pos_end]==1:
                                            count+=1
                                    if count<2 and pos_end!=self.station:
                                        for f in range(pos,pos_end+1):
                                            worker_sequence[i][f]=1
                                    else:
                                        for f in range(pos_begin,pos):
                                            worker_sequence[j][f]=0
                                else:
                                    for f in range(pos_begin,pos+1):
                                        worker_sequence[i][f]=1
                        pos=1
                        flag=0
                        for f in range(1,self.station+1):
                            if worker_sequence[i][f]==1:
                                pos_begin=f
                                break
                        for f in range(self.station,0,-1):
                            if worker_sequence[i][f]==1:
                                pos_end=f
                                break
                        if worker_sequence[j][pos_begin]!=1 and worker_sequence[j][pos_end]!=1:
                            for f in range(pos_begin+1,pos_end):
                                if worker_sequence[i][f]==1 and worker_sequence[j][f]==1:
                                    flag=1
                                    pos=f
                            if flag==1:
                                count=0
                                for m in range(1,self.worker+1):
                                    if worker_sequence[m][pos_begin]==1:
                                        count+=1
                                if count>=2:
                                    count=0
                                    for m in range(1,self.worker+1):
                                        if worker_sequence[m][pos_end]==1:
                                            count+=1
                                    if count<2 and pos_end!=self.station:
                                        for f in range(pos,pos_end+1):
                                            worker_sequence[j][f]=1
                                    else:
                                        for f in range(pos_begin,pos):
                                            worker_sequence[i][f]=0

                                else:
                                    for f in range(pos_begin,pos+1):
                                        worker_sequence[j][f]=1
                print("new=",worker_sequence)
                fflag=1
                while fflag==1:
                        for f in range(1,self.station+1):
                            pos_worker=[]
                            pos_count=0
                            for i in range(1,self.worker+1):
                                if worker_sequence[i][f]==1:
                                    pos_worker.append(i)
                                    pos_count+=1
                            if pos_count>2 and f!=self.station:
                                pos=0
                                while pos_count>2:
                                    for f in range(1,f+1):
                                        worker_sequence[pos_worker[pos]][f]=0
                                    pos+=1
                                    pos_count-=1
                                fflag=0
                            elif pos_count>=2 and f==self.station:
                                pos=0
                                while pos_count>=2:
                                    worker_sequence[pos_worker[pos]][f]=0
                                    pos+=1
                                    pos_count-=1
                                fflag=0
                            elif pos_count==0:
                                pos=random.randint(1,self.worker)
                                print("pos=",pos)
                                worker_sequence[pos][f]=1
                                for ff in range(1,self.station+1):
                                        if worker_sequence[pos][ff]==1:
                                            pos_begin=ff
                                            break
                                for ff in range(self.station,0,-1):
                                        if worker_sequence[pos][ff]==1:
                                            pos_end=ff
                                            break
                                for ff in range(pos_begin,pos_end+1):
                                        worker_sequence[pos][ff]=1
                                fflag=1
                                break
                            else:
                                fflag=0
                for i in range(1,self.worker+1):
                    for j in range(1,self.worker+1):
                        ffflag=0
                        for f in range(1,self.station+1):
                            if worker_sequence[j][f]==1:
                                pos_begin=f
                                break
                        for f in range(self.station,0,-1):
                            if worker_sequence[j][f]==1:
                                pos_end=f
                                break
                        if worker_sequence[i][pos_begin]!=1 and worker_sequence[i][pos_end]!=1:
                            for f in range(pos_begin+1,pos_end):
                                if worker_sequence[i][f]==1 and worker_sequence[j][f]==1:
                                    ffflag=1
                                    break  
                        if ffflag==1:
                            break
                        else:
                            for f in range(1,self.station+1):
                                if worker_sequence[i][f]==1:
                                    pos_begin=f
                                    break
                            for f in range(self.station,0,-1):
                                if worker_sequence[i][f]==1:
                                    pos_end=f
                                    break
                            if worker_sequence[j][pos_begin]!=1 and worker_sequence[j][pos_end]!=1:
                                for f in range(pos_begin+1,pos_end):
                                    if worker_sequence[i][f]==1 and worker_sequence[j][f]==1:
                                        ffflag=1
                                        break
                            if ffflag==1:
                                break
                    if ffflag==1:
                        break

            for i in range(1,self.worker+1):
                    pos_begin=0
                    pos_end=self.station+1
                    for f in range(1,self.station+1):
                        if worker_sequence[i][f]==1:
                            pos_begin=f
                            break
                    for f in range(self.station,0,-1):
                        if worker_sequence[i][f]==1:
                            pos_end=f
                            break

                    if pos_begin==0 and pos_end==self.station+1:
                        flag_new_new=0
                        break
                    else:
                        flag_new_new=1
            if flag_new_new==0:
                    for f in range(1,4):
                        for i in range(1,self.worker+1):
                            worker_sequence[i][f]=0
        for i in range(1,self.worker+1):
            for f in range(1,self.station+1):
                if worker_sequence[i][f]==1:
                    break
            if f==self.station and worker_sequence[i][self.station]==0:
                worker_sequence[i][1]=1

                for m in range(1,self.worker+1):
                    if m!=i and worker_sequence[m][1]==1 and worker_sequence[m][2]!=1:
                        count=0
                        pos_worker=[]
                        for i in range(1,self.worker+1):
                            if worker_sequence[i][2]==1:
                                count+=1
                                pos_worker.append(i)
                        if count>=2:
                            pos=0
                            while count>=2:
                                
                                worker_sequence[pos_worker[pos]][2]=0
                                pos+=1
                                count-=1
                            worker_sequence[m][2]=1
                        else:
                            worker_sequence[m][2]=1
                    elif m!=i and worker_sequence[m][1]==1 and worker_sequence[m][2]==1:
                        worker_sequence[m][1]=0
        pos_start=np.zeros((self.worker+1),dtype=int)
        pos_end=np.zeros((self.worker+1),dtype=int)
        ran=random.random()
        position=random.randint(1,self.worker)
        if ran>self.f and flag_change==1:
            position_new=random.randint(1,self.worker)
            while position_new==position:
                position_new=random.randint(1,self.worker)
            worker_newsequence=np.zeros((1,self.station+1),dtype=int)
            worker_newsequence[0][:self.station+1]=worker_sequence[position][:self.station+1]
            worker_sequence[position][:self.station+1]=worker_sequence[position_new][:self.station+1]
            worker_sequence[position_new][:self.station+1]=worker_newsequence[0][:self.station+1]


        for i in range(1,self.worker+1):
            for f in range(1,self.station+1):
                if worker_sequence[i][f]==1:
                    pos_start[i-1]=f
                    break
            for f in range(self.station,0,-1):
                if worker_sequence[i][f]==1:
                    pos_end[i-1]=f
                    break
        for i in range(0,self.worker):
            for j in range(i+1,self.worker):
                if pos_start[i]==pos_start[j] and pos_end[i]==pos_end[j]:
                    worker_sequence[i+1][pos_start[i]]=0
                    pos_start[i]+=1
        print("sdsd=",worker_sequence)
        print("start=",pos_start)
        print("end=",pos_end)
        return pos_start,pos_end,worker_sequence
    def func_pos(self,pos_start,pos_end):
        pos=np.zeros((self.worker),dtype=int)
        for i in range(self.worker):
            pos[i]=1

        for i in range(0,self.worker):
            for j in range(i+1,self.worker):
                if pos_start[i]<pos_start[j]:
                    pos[j]+=1
                elif pos_start[i]==pos_start[j]:
                    if pos_end[i]>pos_end[j]:
                        pos[i]+=1
                    else:
                        pos[j]+=1
                else:
                    pos[i]+=1
        print("pos=",pos)
        # for i in range(self.worker):
        #     pos[self.worker-i-1],pos[i]=pos[i],pos[self.worker-i-1]
        newpos=np.zeros((self.worker),dtype=int)
        for i in range(0,self.worker):
            newpos[pos[i]-1]=i+1
        pos_newstart=np.zeros((self.worker+1),dtype=int)
        pos_newend=np.zeros((self.worker+1),dtype=int)
        for i in range(0,self.worker):
            pos_newstart[pos[i]-1]=pos_start[i]
            pos_newend[pos[i]-1]=pos_end[i]
        print("newstart=",pos_newstart)
        print("newend=",pos_newend)
        print("newpos=",newpos)
        return newpos,pos_newstart,pos_newend
    def func_main(self):
        min_x=[]
        min_f=[]
        xx=[]
        for i in range(self.NP):
            worker_sequence=self.initpopvfit()
            for w in range(self.worker+1):
                for f in range(self.station+1):
                    self.population[i][w][f]=worker_sequence[w][f]   
            for i in range(1,self.worker+1):
                for j in range(1,self.station+1):
                    self.worker_sequence[i][j]=0
            bucket=Bucketbrigade(self.worker,self.station,self.order)
            xx.append(bucket.objective_function(self.population[i],self.begin,self.end,self.pos))
            for i in range(self.worker+1):
                self.begin[i]=0
            for j in range(self.worker+1):
                self.end[j]=0
            self.pos=random.sample(range(1,self.worker+1),self.worker)      
        print("niuniuxx=",xx)
        print("pop=",self.population)
        min_f.append(min(xx))
        min_x.append(self.population[xx.index(min(xx))])
        for i in range(0,self.generation):
            v_population=self.func_variation(self.population)
            print("pop=",self.population)
            for j in range(self.NP):
                pos_start,pos_end,v_population[j]=self.worker_repair(v_population[j],1)
                newpos,pos_newstart,pos_newend=self.func_pos(pos_start,pos_end)
            u_population=self.func_crossover(self.population,v_population)
            print("u=",u_population)
            self.population=self.func_selection(u_population,self.population)
            print("popnew=",self.population)
            xx=[]
            for j in range(self.NP):
                pos_start,pos_end,self.population[j]=self.worker_repair(self.population[j],0)
                newpos,pos_newstart,pos_newend=self.func_pos(pos_start,pos_end)
                bucket=Bucketbrigade(self.worker,self.station,self.order)
                xx.append(bucket.objective_function(self.population[j],pos_newstart,pos_newend,newpos))
    
            print("xx=",xx)
            min_f.append(min(xx))
            min_x.append(self.population[xx.index(min(xx))])
        min_ff=min(min_f)
        min_xx=min_x[min_f.index(min_ff)]
        print("x=",min_xx)
        print("y=",min_ff)
        print("min=",min_f)
        # x_label=np.arange(0,self.generation+1,1)
        # plt.plot(x_label,min_f,color='green',label='DE algorithmn')
        # plt.xlabel('iteration')
        # plt.ylabel('fx')
        # print("NP=",self.NP)
        # plt.legend()
        # plt.show()
        bucket=Bucketbrigade(self.worker,self.station,self.order)
        begin,end,min_xx=self.worker_repair(min_xx,0)
        pos,begin,end=self.func_pos(begin,end)
        bucket.solve(min_xx,begin,end,pos)
        return min_f



    # def func(self):
    #     self.initpopvfit()
    #     v_population=self.func_variation(self.population)
    #     for i in range(0,self.NP):
    #         pos_start,pos_end=self.worker_repair(v_population[i])
    #         self.func_pos(pos_start,pos_end)


if __name__ == "__main__":
        bucket=population(6,10,90,0.2,0.6,100)
        bucket.func_main()