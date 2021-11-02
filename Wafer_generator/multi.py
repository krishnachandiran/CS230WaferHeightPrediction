# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:15:46 2021

@author: krishnr
"""

import time
import multiprocessing 

def basic_func(x):
    
    if x == 0:
        return 'zero'
    elif x%2 == 0:
        return 'even'
    else:
        return 'odd'

def multiprocessing_func(x):
    y = x*x
    return basic_func(y)
    
if __name__ == '__main__':
    
    starttime = time.time()
    pool = multiprocessing.Pool()
    total_successes =  pool.map(multiprocessing_func, range(0,10))
    pool.close()
    print(total_successes) 
    print('That took {} seconds'.format(time.time() - starttime))