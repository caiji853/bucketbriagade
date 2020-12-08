import random
import numpy as np
import csv
def worker_speed():
    #!/usr/bin/python3
    # -*- coding: utf-8 -*-
    # 导入CSV安装包
    # 1. 创建文件对象
    f = open('worker.csv', 'w',newline='',encoding="utf-8")# 2. 基于文件对象构建 csv写入对象
    csv_write= csv.writer(f)
    # 3. 构建列表
    for i in range(worker):
        csv_write.writerow(np.random.randint(1,10,station))
        print(np.random.randint(1,10,station))
    # 4. 写入csv文件内容
    # 5. 关闭文件
    f.close()
