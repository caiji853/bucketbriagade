import numpy as np
import random, math, copy
import matplotlib.pyplot as plt
from model_latest import Bucketbrigade 
 
class ABSIndividual:
    '''
    individual of artificial bee swarm algorithm
    '''

    def __init__(self,worker,station,order):
        '''
        vardim: dimension of variables
        bound: boundaries of variables
        '''
        self.vardim=worker
        self.worker=worker
        self.station=station
        self.order=order       
        self.score = 0
        self.invalidCount = 0
        self.worker_sequence=np.zeros((self.worker+1,self.station+1),dtype=int)
        self.pos=random.sample(range(1,self.worker+1),self.worker)
        self.L=np.zeros((self.worker+1),dtype=float)
        self.end=np.zeros((self.worker+1),dtype=int)
        self.begin=np.zeros((self.worker+1),dtype=int)
    # def generate(self):
    #     '''
    #     generate a random chromsome for artificial bee swarm algorithm
    #     '''
    #     len = self.vardim
    #     rnd = np.random.random(size=len)
    #     self.chrom = np.zeros(len)
    #     for i in range(0, len):
    #         self.chrom[i] = self.bound[0, i] + \
    #             (self.bound[1, i] - self.bound[0, i]) * rnd[i]
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

    def calculateFitness(self):
        '''
        calculate the fitness of the chromsome
        计算适应度值
        '''
        bucket=Bucketbrigade(self.vardim,self.station,self.order)
        self.score=bucket.objective_function(self.worker_sequence,self.begin,self.end,self.pos)
        
class ArtificialBeeSwarm:
    def __init__(self,worker,station,order,f,MAXGEN, params):
        '''
        sizepop: population sizepop
        vardim: dimension of variables
        bound: boundaries of variables
        MAXGEN: termination condition
        params: algorithm required parameters, it is a list which is consisting of[trailLimit, C]
        '''
        self.vardim = worker
        self.worker=worker
        self.station=station
        self.order=order
        self.sizepop =int(self.worker*self.station*self.worker/5) 
        self.f=f
        self.foodCount = int(self.sizepop / 2)
        self.MAXGEN = MAXGEN
        self.params = params    #最大无效次数
        self.foodList =[]   #初始化各蜜源
        self.foodScore =  np.zeros((self.foodCount, 1))                           #各蜜源最佳成绩
        self.initialize()
        self.evaluation()
        self.bestFood = self.foodList[np.argmin(self.foodScore)]                      #全局最佳蜜源
    def initialize(self):
        '''
        initialize the population of abs
        '''
        for i in range(0, self.foodCount):
            ind = ABSIndividual(self.worker,self.station,self.order)
            ind.initpopvfit()
            self.foodList.append(ind)

    def evaluation(self):
        '''
        evaluation the fitness of the population
        '''
        for i in range(0, self.foodCount):
            self.foodList[i].calculateFitness()
            self.foodScore[i]=self.foodList[i].score  
    def func_abstract(self,ran,worker_sequence1,worker_sequence2):
            abstract_population=np.zeros((self.worker+1,self.station+1),dtype=int)
            for w in range(self.worker+1):
                for f in range(self.station+1):
                    abstract_population[w][f]=worker_sequence1[w][f] and worker_sequence2[w][f]
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
    def updateFood(self, i):
        j = np.random.random_integers(0, self.foodCount - 1)                                                  #更新第i个蜜源
        while j==i:
            j = np.random.random_integers(0, self.foodCount - 1)  #随机选择另一蜜源作参考,j是其索引号
        vi = copy.deepcopy(self.foodList[i])
        # vi.chrom[k] += random.uniform(-1.0, 1.0) * (vi.chrom[k] - self.foodList[j].chrom[k]) #调整参数
        # vi.chrom[k] = np.clip(vi.chrom[k], self.bound[0, k], self.bound[1, k])               #参数不能越界
        ran=random.random()
        worker_sequence=self.func_abstract(ran,self.foodList[i].worker_sequence,self.foodList[j].worker_sequence)
        worker_sequence=self.func_add(self.foodList[i].worker_sequence,worker_sequence)
        begin,end,worker_sequence=self.worker_repair(worker_sequence,1)
        vi.worker_sequence=worker_sequence
        vi.pos,vi.begin,vi.end=self.func_pos(begin,end)
        vi.calculateFitness()
        if vi.score < self.foodList[i].score:           #如果成绩比当前蜜源好
            self.foodList[i] = vi
            if vi.score < self.foodScore[i]:            #如果成绩比历史成绩好（如重新初始化，当前成绩可能低于历史成绩）
                self.foodScore[i] = vi.score
                if vi.score < self.bestFood.score:      #如果成绩全局最优
                    self.bestFood = vi
            self.foodList[i].invalidCount = 0
        else:
            self.foodList[i].invalidCount += 1
            
    def employedBeePhase(self):
        for i in range(0, self.foodCount):              #各蜜源依次更新
            self.updateFood(i)            
 
    def onlookerBeePhase(self):
        # foodScore = [d.score for d in self.foodList]  
        # maxScore = np.min(foodScore)
        # print(foodScore)      
        # accuFitness = [(0.9*maxScore/d+0.1, k) for k,d in enumerate(foodScore)]        #得到各蜜源的 相对分数和索引号

        # for k in range(0, self.foodCount):
        #     i = random.choice([d[1] for d in accuFitness if d[0] >= random.random()])  #随机从相对分数大于随机门限的蜜源中选择跟随
        #     self.updateFood(i)
        accuFitness = np.zeros((self.foodCount, 1))
        maxFitness=min(self.foodScore)
        for i in range(0, self.foodCount):
            accuFitness[i] = 0.9 * self.foodScore[i]/maxFitness + 0.1
        # accuFitness=[(0.9*maxFitness/d+0.1,k) for k,d in enumerate(foodscore)] 
        # for k in range(0, self.foodSource):
        #     i=random.choice([d[1] for d in accuFitness if d[0]>=random.random()])
        #     self.updatefood(i)
        for i in range(0, self.foodCount):
            for fi in range(0, self.foodCount):
                r = random.random()
                if r < accuFitness[i]:
                    
                    j = np.random.random_integers(0, self.foodCount - 1)
                    while j == fi:
                        j = np.random.random_integers(0, self.foodCount - 1)
                    vi = copy.deepcopy(self.foodList[fi])
                    # vi.chrom = vi.chrom + np.random.uniform(-1, 1, self.vardim) * (
                    #     vi.chrom - self.population[j].chrom) + np.random.uniform(0.0, self.params[1], self.vardim) * (self.best.chrom - vi.chrom)
                    # for k in xrange(0, self.vardim):
                    #     if vi.chrom[k] < self.bound[0, k]:
                    #         vi.chrom[k] = self.bound[0, k]
                    #     if vi.chrom[k] > self.bound[1, k]:
                    #         vi.chrom[k] = self.bound[1, k]
                    ran=random.random()
                    worker_sequence=self.func_abstract(ran,self.foodList[i].worker_sequence,self.foodList[j].worker_sequence)
                    worker_sequence=self.func_add(self.foodList[i].worker_sequence,worker_sequence)
                    begin,end,worker_sequence=self.worker_repair(worker_sequence,1)
                    vi.worker_sequence=worker_sequence
                    vi.pos,vi.begin,vi.end=self.func_pos(begin,end)
                    vi.calculateFitness()
                    if vi.score < self.foodList[fi].score:           #如果成绩比当前蜜源好
                        self.foodList[fi] = vi
                        if vi.score < self.foodScore[fi]:            #如果成绩比历史成绩好（如重新初始化，当前成绩可能低于历史成绩）
                            self.foodScore[fi] = vi.score
                            if vi.score < self.bestFood.score:      #如果成绩全局最优
                                self.bestFood = vi
                        self.foodList[fi].invalidCount = 0
                    else:
                        self.foodList[fi].invalidCount += 1
                    break
    def scoutBeePhase(self):
        for i in range(0, self.foodCount):
            if self.foodList[i].invalidCount > self.params[0]:                    #如果该蜜源没有更新的次数超过指定门限，则重新初始化
                self.foodList[i] = ABSIndividual(self.worker,self.station,self.order)
                self.foodList[i].initpopvfit()
                self.foodList[i].invalidCount = 0
                self.foodList[i].calculateFitness()
                self.foodScore[i] = min(self.foodScore[i], self.foodList[i].score)
 
    def solve(self):
        trace = []
        trace.append(self.bestFood.score)
        # print(trace)
        for k in range(self.MAXGEN):
            self.employedBeePhase()
            self.onlookerBeePhase()
            self.scoutBeePhase()
            trace.append(self.bestFood.score)
            print(self.bestFood.score)
        print(self.bestFood.score)
        print(self.bestFood.worker_sequence)
        bucket=Bucketbrigade(self.worker,self.station,self.order)
        begin,end,self.bestFood.worker_sequence=self.worker_repair(self.bestFood.worker_sequence,0)
        pos,begin,end=self.func_pos(begin,end)
        bucket.solve(self.bestFood.worker_sequence,begin,end,pos)
        # self.printResult(np.array(trace))
        return trace
 
    def printResult(self, trace):
        t = np.array([t for t in range(0, self.MAXGEN)])
        # plt.plot(x, [(d-1)/d for d in trace[:, 0]], 'r', label='optimal value')
        plt.plot(t, trace, 'r', label='ABC algorithmn')
        # plt.plot(x, [(d-1)/d for d in trace[:, 1]], 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Artificial Bee Swarm algorithm for function optimization")
        plt.legend()
        plt.show()

 
# if __name__ == "__main__":
#     abc=ArtificialBeeSwarm(6,8,36,0.1,100,[20,0.5])
#     abc.solve()