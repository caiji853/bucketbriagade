import numpy as np
from ABC_indi import ABSIndividual
import random
import copy
import matplotlib.pyplot as plt


class ArtificialBeeSwarm:

    '''
    the class for artificial bee swarm algorithm
    '''

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
        self.foodSource = int(self.sizepop / 2)
        self.MAXGEN = MAXGEN
        self.params = params
        self.population = []
        # self.fitness = np.zeros((self.foodSource, 1))
        self.fitness_score=np.zeros((self.foodSource, 1))
        self.trace = np.zeros((self.MAXGEN, 2))

    def initialize(self):
        '''
        initialize the population of abs
        '''
        for i in range(0, self.foodSource):
            ind = ABSIndividual(self.worker,self.station,self.order)
            ind.initpopvfit()
            self.population.append(ind)

    def evaluation(self):
        '''
        evaluation the fitness of the population
        '''
        for i in range(0, self.foodSource):
            self.population[i].calculateFitness()
            self.fitness_score[i]=self.population[i].fitness
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
    def updatefood(self,i):
        '''
        employed bee phase
        '''
            # k = np.random.random_integers(0, self.vardim - 1)
        j = np.random.random_integers(0, self.foodSource - 1)
        while j == i:
            j = np.random.random_integers(0, self.foodSource - 1)
        vi = copy.deepcopy(self.population[i])
            # vi.chrom = vi.chrom + np.random.uniform(-1, 1, self.vardim) * (
            #     vi.chrom - self.population[j].chrom) + np.random.uniform(0.0, self.params[1], self.vardim) * (self.best.chrom - vi.chrom)
            # for k in xrange(0, self.vardim):
            #     if vi.chrom[k] < self.bound[0, k]:
            #         vi.chrom[k] = self.bound[0, k]
            #     if vi.chrom[k] > self.bound[1, k]:
            #         vi.chrom[k] = self.bound[1, k]
            # vi.chrom[
            #     k] += np.random.uniform(low=-1, high=1.0, size=1) * (vi.chrom[k] - self.population[j].chrom[k])
            # if vi.chrom[k] < self.bound[0, k]:
            #     vi.chrom[k] = self.bound[0, k]
            # if vi.chrom[k] > self.bound[1, k]:
            #     vi.chrom[k] = self.bound[1, k]
        ran=random.random()
        worker_sequence=self.func_abstract(ran,self.population[i].worker_sequence,self.population[j].worker_sequence)
        worker_sequence=self.func_add(self.population[i].worker_sequence,worker_sequence)
        begin,end,worker_sequence=self.worker_repair(worker_sequence,1)
        vi.worker_sequence=worker_sequence
        vi.pos,vi.begin,vi.end=self.func_pos(begin,end)
        vi.calculateFitness()
        if vi.fitness < self.population[i].fitness:
                self.population[i] = vi
                if vi.fitness < self.fitness_score[i]:
                    self.fitness_score[i]=vi.fitness
                    if vi.fitness < self.best.fitness:
                        self.best = vi
                self.population[i].trials=0
        else:
                self.population[i].trials += 1
    def employedBeePhase(self):
        for i in range(self.foodSource):
            self.updatefood(i)
    def onlookerBeePhase(self):
        '''
        onlooker bee phase
        '''
        # accuFitness = np.zeros((self.foodSource, 1))
        foodscore=[d.fitness for d in self.population]
        maxFitness = np.min(foodscore)

        # for i in range(0, self.foodSource):
        #     accuFitness[i] = 0.9 *  maxFitness/ self.fitness_score[i] + 0.1
        accuFitness=[(0.9*maxFitness/d+0.1,k) for k,d in enumerate(foodscore)] 
        for k in range(0, self.foodSource):
            i=random.choice([d[1] for d in accuFitness if d[0]>=random.random()])
            self.updatefood(i)
            # for fi in range(0, self.foodSource):
            #     r = random.random()
            #     if r < accuFitness[i]:
                    
            #         j = np.random.random_integers(0, self.foodSource - 1)
            #         while j == fi:
            #             j = np.random.random_integers(0, self.foodSource - 1)
            #         vi = copy.deepcopy(self.population[fi])
            #         # vi.chrom = vi.chrom + np.random.uniform(-1, 1, self.vardim) * (
            #         #     vi.chrom - self.population[j].chrom) + np.random.uniform(0.0, self.params[1], self.vardim) * (self.best.chrom - vi.chrom)
            #         # for k in xrange(0, self.vardim):
            #         #     if vi.chrom[k] < self.bound[0, k]:
            #         #         vi.chrom[k] = self.bound[0, k]
            #         #     if vi.chrom[k] > self.bound[1, k]:
            #         #         vi.chrom[k] = self.bound[1, k]
            #         ran=random.random()
            #         worker_sequence=self.func_abstract(ran,self.population[i].worker_sequence,self.population[j].worker_sequence)
            #         worker_sequence=self.func_add(self.population[i].worker_sequence,worker_sequence)
            #         begin,end,worker_sequence=self.worker_repair(worker_sequence,1)
            #         vi.worker_sequence=worker_sequence
            #         vi.pos,vi.begin,vi.end=self.func_pos(begin,end)
            #         vi.calculateFitness()
            #         if vi.fitness < self.population[fi].fitness:
            #             self.population[fi] = vi
            #             if vi.fitness < self.fitness_score[fi]:
            #                 self.fitness_score[fi]=vi.fitness
            #                 if vi.fitness < self.best.fitness:
            #                     self.best = vi
            #             self.population[fi].trials=0
            #         else:
            #             self.population[fi].trials += 1
            #         break

    def scoutBeePhase(self):
        '''
        scout bee phase
        '''
        for i in range(0, self.foodSource):
            if self.population[i].trials > self.params[0]:
                self.population[i].initpopvfit()
                self.population[i].trials = 0
                self.population[i].calculateFitness()
                self.fitness_score[i] = min(self.population[i].fitness,self.fitness_score[i])

    def solve(self):
        '''
        the evolution process of the abs algorithm
        '''
        self.t = 0
        self.initialize()
        self.evaluation()
        # best = np.min(self.fitness_score)
        bestIndex = np.argmin(self.fitness_score)
        self.best = copy.deepcopy(self.population[bestIndex])
        self.avefitness = np.mean(self.fitness_score)
        self.trace[self.t, 0] = (self.best.fitness-1) / self.best.fitness
        self.trace[self.t, 1] = (self.avefitness-1) / self.avefitness
        print("Generation %d: optimal function value is: %f; average function value is %f" % (
            self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        while self.t < self.MAXGEN - 1:
            self.t += 1
            print(self.fitness_score)
            self.employedBeePhase()
            self.onlookerBeePhase()
            self.scoutBeePhase()
            # print(self.fitness_score)
            # best = np.min(self.fitness_score)
            # print(best)
            print(self.best.fitness)
            # bestIndex = np.argmin(self.fitness_score)
            # if best < self.best.fitness:
            #     self.best = copy.deepcopy(self.population[bestIndex])
            #     self.fitness_score[bestIndex]=self.best.fitness
            print(self.best.fitness)
            self.avefitness = np.mean(self.fitness_score)
            self.trace[self.t, 0] = (self.best.fitness-1) / self.best.fitness
            self.trace[self.t, 1] = (self.avefitness-1) / self.avefitness
            print("Generation %d: optimal function value is: %f; average function value is %f" % (
                self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        print("Optimal function value is: %f; " % self.trace[self.t, 0])
        print("Optimal solution is:",self.best.worker_sequence)
        self.printResult()

    def printResult(self):
        '''
        plot the result of abs algorithm
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Artificial Bee Swarm algorithm for function optimization")
        plt.legend()
        plt.show()
if __name__ == "__main__":
    abc=ArtificialBeeSwarm(6,8,12,0.3,50,[20,0.5])
    abc.solve()