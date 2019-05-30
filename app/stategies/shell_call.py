import os
from subprocess import call
import pandas as pd
import  subprocess
from app.stategies.pickle_draw import *

startdate='2016-06-01'
enddate='2016-12-01'
volume='100000'#开始总资产
#name='C:\\Users\\DELL\\.rqalpha\\examples\\buy_and_hold.py'#策略路径
name='./test.py'
result='result.pkl'
bench_mark='000300.XSHG'
bundle='C:\\Users\\DELL\\.rqalpha\\bundle\\' #rqalpha 的bundle路径
shell_str='rqalpha run -f '+name+' -d '+bundle+' -s '+startdate+' -e '+enddate+' --account stock '+volume+' --benchmark '+bench_mark+' -o '+result

print(shell_str)

return_code = subprocess.call(shell_str, shell=True)

result1=pd.read_pickle(result)
line1=draw_pfo_return(result1)
line2=draw_net_value(result1)
page=combine(line1,line2)
page.render()