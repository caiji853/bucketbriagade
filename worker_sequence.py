import numpy as np
import math
import random
worker=6
station=10
order=20
#print(pos)
#print(pos[1])
worker_sequence=np.zeros((worker+1,station+1))
start_pos=np.zeros((worker+1),dtype=int)
end_pos=np.zeros((worker+1),dtype=int)
pos=random.sample(range(1,worker+1),worker)
print(pos)
worker_sequence[pos[worker-1]][station]=1
for i in range(1,worker+1):
#     pos=np.random.randint(1,worker+1,worker)
      count=0
      if i==1:
          start_pos[i]=1
          end_pos[i]=np.random.randint(1,station+1-(worker-i-1))
      elif i==2:
          if end_pos[i-1]!=start_pos[i-1]:
            end_pos1=np.random.randint(end_pos[i-1],station+1-(worker-i-1))
          else:
            end_pos1=np.random.randint(end_pos[i-1]+1,station+1-(worker-i-1))   
          for j in range(1,worker+1):
              if worker_sequence[j][end_pos[i-1]]==1:
                 count+=1
          if  count<2 and end_pos1-end_pos[i-1]>=1:
              start_pos[i]=np.random.randint(start_pos[i-1],end_pos[i-1]+2)  
          elif count<2 and end_pos1==end_pos[i-1] and end_pos[i-1]-end_pos[i-2]>=2:
                   start_pos[i]=np.random.randint(end_pos[i-2]+2,end_pos[i-1]+1)
          elif count<2 and end_pos1==end_pos[i-1] and end_pos[i-1]-end_pos[i-2]<2:
               start_pos[i]=np.random.randint(end_pos[i-2]+1,end_pos[i-1]+1)    
          else:
              start_pos[i]=end_pos[i-1]+1
              end_pos1=np.random.randint(start_pos[i],station+1-(worker-i-1)) 
              print(start_pos[i])
          end_pos[i]=end_pos1
      elif i < worker-1:
          if end_pos[i-1]!=start_pos[i-1]:
                end_pos1=np.random.randint(end_pos[i-1],station+1-(worker-i-1))
          else:
                end_pos1=np.random.randint(end_pos[i-1]+1,station+1-(worker-i-1))  
          for j in range(1,worker+1):
              if worker_sequence[j][end_pos[i-1]]==1:
                 count+=1
          if  count<2 and end_pos1-end_pos[i-1]>=1:
              start_pos[i]=np.random.randint(end_pos[i-2]+1,end_pos[i-1]+2)  
          elif count<2 and end_pos1==end_pos[i-1] and end_pos[i-1]-end_pos[i-2]>=2:
                   start_pos[i]=np.random.randint(end_pos[i-2]+2,end_pos[i-1]+1)
          elif count<2 and end_pos1==end_pos[i-1] and end_pos[i-1]-end_pos[i-2]<2:
               start_pos[i]=np.random.randint(end_pos[i-2]+1,end_pos[i-1]+1)    
          else:
              start_pos[i]=end_pos[i-1]+1
              end_pos1=np.random.randint(start_pos[i],station+1-(worker-i-1)) 
              print(start_pos[i])
          end_pos[i]=end_pos1
      elif i==worker-1:
           if end_pos[i-1]!=start_pos[i-1]:
                end_pos1=np.random.randint(end_pos[i-1],station-(worker-i-1))
           else:
                end_pos1=np.random.randint(end_pos[i-1]+1,station-(worker-i-1))   
           for j in range(1,worker+1):
                  if worker_sequence[j][end_pos[i-1]]==1:
                      count+=1
           if  count<2 and end_pos1-end_pos[i-1]>=1:
               start_pos[i]=np.random.randint(end_pos[i-2]+1,end_pos[i-1]+2) 
           elif count<2 and end_pos1==end_pos[i-1] and end_pos[i-1]-end_pos[i-2]>=2:
               start_pos[i]=np.random.randint(end_pos[i-2]+2,end_pos[i-1]+1)
           elif count<2 and end_pos1==end_pos[i-1] and end_pos[i-1]-end_pos[i-2]<2:
               start_pos[i]=np.random.randint(end_pos[i-2]+1,end_pos[i-1]+1)    
           else:
               start_pos[i]=end_pos[i-1]+1
               end_pos1=np.random.randint(start_pos[i],station-(worker-i-1)) 
           end_pos[i]=end_pos1
      else:
          for j in range(1,worker+1):
              if worker_sequence[j][end_pos[i-1]]==1:
                 count+=1
          if  count<2 :
              if end_pos[i-1]!=station:
                 start_pos[i]=np.random.randint(end_pos[i-2]+1,end_pos[i-1]+2)
              else:
                 start_pos[i]=np.random.randint(end_pos[i-2]+1,end_pos[i-1]+1)  
          else:
              start_pos[i]=end_pos[i-1]+1
            
          end_pos[i]=station
      for j in range(start_pos[i],end_pos[i]+1):
          worker_sequence[pos[i-1]][j]=1
print(worker_sequence)
print(start_pos)
print(end_pos)



    # worker_sequence=np.zeros((worker+1,station+1))
# np.savetxt("test.csv", worker_sequence, delimiter=",")

      
          

#     num2=np.random.randint(num,num+1)
#     for j in range()

