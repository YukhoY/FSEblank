import os
from subprocess import call
import pandas as pd
import  subprocess
from strategy_run.pickle_draw import *

def shell_call(name,
               bench_mark='000300.XSHG',
               bundle='C:\\Users\\DELL\\.rqalpha\\bundle\\',
               startdate='2016-06-01',enddate='2016-12-01',volume='100000',):
    result = name + '_result.pkl'
    shell_str = 'rqalpha run -f ' + name + ' -d ' + bundle + ' -s ' + startdate + ' -e ' + enddate + ' --account stock ' + volume + ' --benchmark ' + bench_mark + ' -o ' + result
    print(shell_str)
    return_code = subprocess.call(shell_str, shell=True)
    result1=pd.read_pickle(result)
    summary=result1['summary']
    line1=draw_pfo_return(result1)
    line2=draw_net_value(result1)
    page=combine(line1,line2)
    return page,summary