def condition():
        # L=np.zeros((worker+1))
        # end=np.zeros((worker+1))
    # for i in range(2,self.order-self.worker+2):
    #     for j in range(2,self.worker+1):
    #         if PW[i][self.pos[worker-1]]-PW[i+j-1][self.pos[worker-j]]<0:
    while 1:
        count=0
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
                        self.PW[self.worker-m][posi]+=round(self.processing_time[self.worker-m-1][posi-1][f-1]*(1-ran),2)
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
        count+=1
        for i in range(2,self.order-self.worker+2):
            for j in range(2,self.worker+1):
                if PW[i][self.pos[worker-1]]-PW[i+j-1][self.pos[worker-j]]<0:
                    exit=1
                    break
            if exit==1:
                break

        if exit==1 or count>1000:
            break
    print(self.P)
    print(self.L)
    print(self.PW)