import pandas as pd
from pyecharts.charts import Kline, Line, Page,Grid,Timeline
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import tushare as ts
import re
import time
from datetime import datetime,timedelta


#result=pd.read_pickle('C:\\Users\\DELL\\result.pkl')

def draw_pfo_return(result):
    timeline=result['portfolio'].index
    timeline=[i.strftime("%Y/%m/%d") for i in timeline]
    #print(timeline)
    static_unit_net_value=result['portfolio']['static_unit_net_value'].tolist()
    pfo_rtn=[i-1 for i in static_unit_net_value]

    static_unit_net_value_b = result['benchmark_portfolio']['static_unit_net_value'].tolist()
    pfo_b_rtn = [round(i - 1,5) for i in static_unit_net_value_b]#benchmark

    rtn_line = (
        Line(init_opts=opts.InitOpts(width="1400px",height="500px"))
            .add_xaxis(timeline)
            .add_yaxis("回测收益", pfo_rtn,
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
            .add_yaxis("基准收益",pfo_b_rtn,
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
            .set_global_opts(title_opts=opts.TitleOpts(title="收益率"),
                             xaxis_opts=opts.AxisOpts(is_scale=True,type_='time'),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(pos_bottom="-1%")],
                             toolbox_opts=opts.ToolboxOpts(is_show=True),

                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    )

    return rtn_line

def draw_net_value(result):
    timeline = result['portfolio'].index
    timeline = [i.strftime("%Y/%m/%d") for i in timeline]

    # print(timeline)
    total_value = result['portfolio']['total_value'].tolist()

    total_value_b = result['benchmark_portfolio']['total_value'].tolist()

    rtn_line = (
        Line(init_opts=opts.InitOpts(width="1400px",height="500px"))
            .add_xaxis(timeline)
            .add_yaxis("回测总资产", total_value,
                       )
            .add_yaxis("基准总资产", total_value_b,
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title="总资产"),
                             xaxis_opts=opts.AxisOpts(is_scale=True, type_='time'),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(pos_bottom="-1%")],
                             toolbox_opts=opts.ToolboxOpts(is_show=True),

                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    )

    return rtn_line

def combine(graph1,graph2):
    page=Page()
    page.add(graph1)
    page.add(graph2)
    #page.render()
    return page

#line1=draw_pfo_return(result)
#line2=draw_net_value(result)
#page=combine(line1,line2)
#page.render()