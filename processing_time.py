import numpy
import csv
worker_speed = numpy.loadtxt(open("worker.csv","rb"),delimiter=",",skiprows=0)
print(worker_speed)
product_station=numpy.loadtxt(open("data.csv","rb"),delimiter=",",skiprows=0)
print(product_station)
product=len(product_station)
station=len(product_station[0])
worker=len(worker_speed)
processing_time=[[[0 for i in range(station)] for i in range(worker) ] for i in range(product)]
print(processing_time)
for i in range(product):
    for w in range(worker):
        for f in range(station):
            processing_time[i][w][f]=round(product_station[i][f]*60/worker_speed[w][f],2)
print(processing_time)
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