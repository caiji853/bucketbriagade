import numpy as np
import pandas as pd
import os
 
#UTF-8编码格式csv文件数据读取
df = pd.read_csv('test.csv') #返回一个DataFrame的对象，这个是pandas的一个数据结构
df.columns=["S1","S2","S3","S4"]
 
X = df[["S1","S2","S3","S4"]]#抽取前七列作为训练数据的各属性值
X = np.array(X)
print(X)
 
# y1 = df["Col8"] #最后一列作为每行对应的标签label
# #Y = df["Col8"].map(lambda y1:float(y1.rstrip(";")))
# Y = np.array(y1) 
# print Y
