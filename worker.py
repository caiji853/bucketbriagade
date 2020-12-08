import random
import numpy as np
import csv
worker=5
station=8
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 导入CSV安装包

# 1. 创建文件对象
f = open('worker.csv', 'w',newline='',encoding="utf-8")# 2. 基于文件对象构建 csv写入对象
csv_write= csv.writer(f)

# 3. 构建列表头
for i in range(worker):
    csv_write.writerow(np.random.randint(1,10,station))
    print(np.random.randint(1,10,station))
# 4. 写入csv文件内容
# csv_writer.writerow(["l",'18','男'])
# csv_writer.writerow(["c",'20','男'])
# csv_writer.writerow(["w",'22','女'])

# 5. 关闭文件
f.close()
