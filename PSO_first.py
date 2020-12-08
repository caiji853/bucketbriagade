# coding: utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
from model_latest import Bucketbrigade
 

class PSO():
	# PSO参数设置
    def __init__(self,worker,station,order,max_iter):
        self.w = 0.1
        # self.c1 = 2
        # self.c2 = 2
        self.r1 = 0.1
        self.r2 = 0.1
        self.worker=worker
        self.station=station
        self.order=order
        self.pN=int(self.worker*self.station*self.worker/10)
        # self.dim = dim  # 搜索维度
        self.max_iter = max_iter  # 迭代次数
          # 所有粒子的位置和速度
        self.X=[[[0 for i in range(self.station+1)] for i in range(self.worker+1) ] for i in range(self.pN)]
        self.V = [[[0 for i in range(self.station+1)] for i in range(self.worker+1) ] for i in range(self.pN)]
        self.pbest = [[[0 for i in range(self.station+1)] for i in range(self.worker+1) ] for i in range(self.pN)]  # 个体经历的最佳位置和全局最佳位置
        self.gbest = np.zeros((self.worker+1,self.station+1))
        self.p_fit = np.zeros(self.pN)  # 每个个体的历史最佳适应值
        self.fit = 1e10  # 全局最佳适应值
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

    def function(self, X,begin,end,pos):
        bucket=Bucketbrigade(self.worker,self.station,self.order)
        return bucket.objective_function(X,begin,end,pos)
    #初始化种群
    
    def init_Population(self):
        for i in range(self.pN):
            self.pos=random.sample(range(1,self.worker+1),self.worker)
            self.V[i]=self.cal_worker_sequence()
        for i in range(self.pN):      #因为要随机生成pN个数据，所以需要循环pN次
            self.pos=random.sample(range(1,self.worker+1),self.worker)
            print(self.pos)
            self.X[i]=self.cal_worker_sequence()
            self.pbest[i] = self.X[i]     #其实就是给self.pbest定值
            tmp = self.function(self.X[i],self.begin,self.end,self.pos)  #得到现在最优
            self.p_fit[i] = tmp    #这个个体历史最佳的位置
            if tmp < self.fit:   #得到现在最优和历史最优比较大小，如果现在最优大于历史最优，则更新历史最优
                self.fit = tmp
                self.gbest = self.X[i]
    def worker_repair(self,worker_sequence,flag_change):
            # print("niuniu=",worker_sequence)
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
                        # print("pos=",pos)
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
                            # print("pos=",pos)
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
                # print("new=",worker_sequence)
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
                                # print("pos=",pos)
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
        if ran>self.w and flag_change==1:
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
        # print("sdsd=",worker_sequence)
        # print("start=",pos_start)
        # print("end=",pos_end)
        return pos_start,pos_end,worker_sequence
    # 更新粒子位置
    def func_abstract(self,worker_sequence1,worker_sequence2,f):
        abstract_population=np.zeros((self.worker+1,self.station+1),dtype=int)
        for w in range(self.worker+1):
            for f in range(self.station+1):
                abstract_population[w][f]=worker_sequence1[w][f] and worker_sequence2[w][f]
        ran=random.random()
        position=random.randint(1,self.worker)
        if ran>f:
            position_new=random.randint(1,self.worker)
            while position_new==position:
                position_new=random.randint(1,self.worker)
            worker_newsequence=np.zeros((1,self.station+1),dtype=int)
            worker_newsequence[0][:self.station+1]=abstract_population[position][:self.station+1]
            abstract_population[position][:self.station+1]=abstract_population[position_new][:self.station+1]
            abstract_population[position_new][:self.station+1]=worker_newsequence[0][:self.station+1]
        
        return abstract_population
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
        # print("pos=",pos)
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
        # print("newstart=",pos_newstart)
        # print("newend=",pos_newend)
        # print("newpos=",newpos)
        return newpos,pos_newstart,pos_newend

        
    def func_add(self,worker_sequence1,worker_sequence2):
        add_population=np.zeros((self.worker+1,self.station+1),dtype=int)
        for w in range(self.worker+1):
            for f in range(self.station+1):
                add_population[w][f]=worker_sequence1[w][f] or worker_sequence2[w][f]
        ran=random.random()
        position=random.randint(1,self.worker)
        if ran>self.w:
            position_new=random.randint(1,self.worker)
            while position_new==position:
                position_new=random.randint(1,self.worker)
            worker_newsequence=np.zeros((1,self.station+1),dtype=int)
            worker_newsequence[0][:self.station+1]=add_population[position][:self.station+1]
            add_population[position][:self.station+1]=add_population[position_new][:self.station+1]
            add_population[position_new][:self.station+1]=worker_newsequence[0][:self.station+1]
        return add_population
    def iterator(self):
        fitness = []
        for t in range(self.max_iter):    #迭代次数，不是越多越好
            for i in range(self.pN):  # 更新gbest\pbest
                pos_start,pos_end,self.X[i]=self.worker_repair(self.X[i],1)
                newpos,pos_newstart,pos_newend=self.func_pos(pos_start,pos_end)
                temp = self.function(self.X[i],pos_newstart,pos_newend,newpos)
                if temp < self.p_fit[i]:  # 更新个体最优
                    self.p_fit[i] = temp
                    self.pbest[i] = self.X[i]
                    if self.p_fit[i] < self.fit:  # 更新全局最优
                        self.gbest = self.X[i]
                        self.fit = self.p_fit[i]
            for i in range(self.pN):
                # self.V[i] = self.w * self.V[i] +  self.r1 * (self.pbest[i] - self.X[i]) +self.r2 * (self.gbest - self.X[i])
                worker_sequence=self.func_abstract(self.gbest,self.X[i],self.r2)
                worker_sequence_first=self.func_abstract(self.pbest[i],self.X[i],self.r1)
                worker_sequence_first=self.func_add(worker_sequence,worker_sequence_first)
                print("sds=",worker_sequence_first)
                worker_sequence_second=np.zeros((self.worker+1,self.station+1))
                worker_sequence_second=self.func_abstract(self.V[i],worker_sequence_second,self.w)
                self.V[i]=self.func_add(worker_sequence_first,worker_sequence_second)
                self.X[i] =self.func_add(self.X[i],self.V[i])
                pos_start,pos_end,self.X[i]=self.worker_repair(self.X[i],1)
            fitness.append(self.fit)
            print(self.gbest, end=" ")
            print(self.fit)  # 输出最优值
        # plt.title("Figure1")
        # plt.xlabel("iterators", size=14)
        # plt.ylabel("fitness", size=14)
        # t = np.array([t for t in range(0, 100)])
        # fitness = np.array(fitness)
        # plt.plot(t, fitness, color='b')
        # plt.legend()
        # plt.show()    
        
        return fitness
if __name__ == "__main__":
        #程序
    maxinter=100
    my_pso = PSO(6,8,72,maxinter)
    my_pso.init_Population()
    fitness = my_pso.iterator()
    # 画图
    plt.figure(1)
    plt.title("Figure1")
    plt.xlabel("iterators", size=14)
    plt.ylabel("fitness", size=14)
    t = np.array([t for t in range(0, maxinter)])
    fitness = np.array(fitness)
    plt.plot(t, fitness, color='b')
    plt.show()
