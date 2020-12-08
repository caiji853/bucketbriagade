import numpy as np
import math
import random
import scipy.stats
import csv
class inputdata(object):
    def __init__(self,worker,station,order):
        self.worker=worker
        self.station=station
        self.order=order
    def cal_station(self):
        lower = 0.01
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
        # self.worker_speed = np.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
        # print(self.worker_speed)
        # return worker_speed
    def cal_station_data(self):
    
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
        # self.product_station=np.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
    def function(self):
        self.cal_worker_speed()
        self.cal_station_data()
if __name__ == "__main__":
    data=inputdata(6,10,24)
    data.function()