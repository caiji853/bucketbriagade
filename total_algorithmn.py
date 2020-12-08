import numpy as np
import random, math, copy
import matplotlib.pyplot as plt
import scipy.stats
import csv
from model_latest import Bucketbrigade
from PSO_first import  PSO
from ABC_second import ABSIndividual
from ABC_second import ArtificialBeeSwarm
from DE_first import population
if __name__ == "__main__":
    my_pso = PSO(6,10,24,100)
    my_pso.init_Population()
    fitness = my_pso.iterator()
    # 画图
    # plt.figure(1)
    # plt.title("Figure1")
    # plt.xlabel("iterators", size=14)
    # plt.ylabel("fitness", size=14)
    t = np.array([t for t in range(0, 100)])
    fitness = np.array(fitness)
    print(fitness)
    bucket=population(6,10,24,0.4,0.6,100)
    min_f=bucket.func_main()
    abc=ArtificialBeeSwarm(6,10,24,0.1,100,[20,0.5])
    # print("niuniu")
    trace=abc.solve()
    trace=np.array(trace)
    min_f=np.array(min_f)
    plt.plot(t, fitness, color='b', label= 'PSO algorithmn')
    plt.legend()
    plt.show()
    tnew = np.array([tnew for tnew in range(0, 101)])
    plt.plot(tnew,trace, 'r', label='ABC algorithmn')
    plt.legend()
    plt.show()
    plt.plot(tnew,min_f,color='green',label='DE algorithmn')
    plt.legend()
    plt.show()
    plt.plot(t, fitness, color='b', label= 'PSO algorithmn')
    plt.plot(tnew,trace, 'r', label='ABC algorithmn')
    plt.plot(tnew,min_f,color='green',label='DE algorithmn')
    plt.xlabel("Iteration")
    plt.ylabel("function value")
    plt.legend()
    plt.show() 