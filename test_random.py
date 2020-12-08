import scipy.stats
import csv
lower = 0
upper = 1
mu = 1/8
sigma = 0.1
order=20
N = 10
worker=5
station=8
def init():
  result=[]
  summary=0
  flag=0
  flag_new=0
  while  flag_new==0 or flag==1:
    if flag==1:
        result=[]
    for i in range(7):
        
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
        elif i==6:
           flag=0
           flag_new=1
        else:
           pass
  result.append(round(1-summary,2))
  print(result)
  return  result
if __name__ == "__main__":
    station=[]
    for o in range(order):
        result=init()
        station.append(result)
    print(station)
    tmp = open('data.csv', 'w',newline='',encoding="utf-8") # a表示在最后一行后面追加
                                                            #newline以免出现写一行空一行
                                                            #encoding 解决不能写入的错误
    
    csv_write = csv.writer(tmp) 
    #csv_write.writerow(['id', 'eng_socre']) 写入列名
    for  item in station:
        if item !=None:
            csv_write.writerow(item)
    tmp.close()
    print('over')

       
