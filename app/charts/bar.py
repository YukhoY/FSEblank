#-*- coding:utf-8 -*-

from pyecharts.charts import Kline, Line, Page,Grid,Timeline
from pyecharts import options as opts
import tushare as ts
import pandas as pd
import re
import time
from datetime import datetime,timedelta

def stock_draw(labels,mode_combo,startdate,enddate,optInterval,width1, height1):

    startdate = startdate.replace("/", "-")  # 将参数日期转换为tushare的日期格式
    enddate = enddate.replace("/", "-")

    page = Page()


    for label in labels:  # 对于传入的labels一张张作图
        label1 = re.split("-", label)
        print(label1[0])
        print(label1[1])


        if mode_combo == "KLine":
            array = ts.get_k_data(label1[1], start=startdate, end=enddate, ktype=optInterval)
            # print(array)
            time = array['date'].tolist()  # array.date
            # 绘图方法

            if label1[2] == 'Kline':
                re_array = array[['open', 'close', 'high', 'low']]
                data_li = list(row.tolist() for index, row in re_array.iterrows())
                close = array['close'].tolist()
                #width=width1 * 10 / 11, height=(height1 * 10 / 11) / len(labels)

                kline = (
                    Kline()
                        .add_xaxis(time)
                        .add_yaxis(label1[0],data_li)
                        .set_global_opts(

                        xaxis_opts=opts.AxisOpts(is_scale=True),
                        yaxis_opts=opts.AxisOpts(
                            is_scale=True,
                            splitarea_opts=opts.SplitAreaOpts(
                                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                            ),
                        ),
                        datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
                        title_opts=opts.TitleOpts(title=label1[0] + "-" + optInterval)


                    )
                )


                # 计算移动平均
                if len(close) > 10:
                    ma10 = CalculateMA(close, 10)

                    line1 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA10", ma10)
                            #.set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )
                    kline.overlap(line1)

                if len(close) > 20:
                    ma20 = CalculateMA(close, 20)
                    line2 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA20", ma20)
                        # .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )
                    kline.overlap(line2)


                if len(close) > 30:
                    ma30 = CalculateMA(close, 30)

                    line3 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA30", ma30)
                        # .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )

                    kline.overlap(line3)

                page.add(kline)
            else:  # label1[2]==open/close/volume
                if label1[2] == 'Open':
                    list_aft = array['open'].tolist()
                elif label1[2] == 'Close':
                    list_aft = array['close'].tolist()
                elif label1[2] == 'High':
                    list_aft = array['high'].tolist()
                elif label1[2] == 'Low':
                    list_aft = array['low'].tolist()
                elif label1[2] == 'Volume':  # volume
                    list_aft = array['volume'].tolist()
                else:
                    list_aft = array['amount'].tolist()



                line = (
                    Line()
                        .add_xaxis(time)
                        .add_yaxis(label1[0] + "-" + label1[2], list_aft)
                        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                        yaxis_opts=opts.AxisOpts(
                                            is_scale=True,
                                            splitarea_opts=opts.SplitAreaOpts(
                                                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                            ),
                                        ),
                                        datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
                                        title_opts=opts.TitleOpts(title=label1[0] + "-" + label1[2]))
                        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

                )


                page.add(line)

    return page


def CalculateMA(date,DayCount):
    result=pd.DataFrame(data=date)
    result=result.rolling(DayCount).mean()
    #print(result)
    result_list=result[0].tolist()
    #print(result_list)
    for i in range(len(result_list)):
        result_list[i]=round(result_list[i],3)

    return result_list

def create_hs():

    #绘制market页面首页的沪深两张图


    curdate = time.strftime("%Y/%m/%d")  # 注意格式化参数 获取当前时间
    # print(curdate)

    dateobj = datetime.strptime(curdate, "%Y/%m/%d")  # 转换为datetime对象

    pastL = dateobj - timedelta(days=15)  # 前15天时间
    pasttimeL = datetime.strftime(pastL, "%Y/%m/%d")
    print(pasttimeL)
    print(curdate)
    labels=['上证指数-sh-Kline', '深证成指-sz-Kline','创业板-cyb-Kline','沪深300指数-hs300-Kline','上证50-sz50-Kline']
    mode_combo='KLine'
    startdate=pasttimeL
    enddate=curdate

    optInterval='5'
    width1=0
    length1=0

    grid = stock_draw_welcome(labels,mode_combo,startdate,enddate,optInterval)


    return grid

def stock_draw_welcome(labels,mode_combo,startdate,enddate,optInterval):

    startdate = startdate.replace("/", "-")  # 将参数日期转换为tushare的日期格式
    enddate = enddate.replace("/", "-")

    tl = Timeline(init_opts=opts.InitOpts(width="1100px",height="500px"))

    for label in labels:  # 对于传入的labels一张张作图
        label1 = re.split("-", label)
        print(label1[0])
        print(label1[1])
        if mode_combo == "KLine":
            array = ts.get_k_data(label1[1], start=startdate, end=enddate, ktype=optInterval)

            time = array['date'].tolist()  # array.date
            # 绘图方法

            if label1[2] == 'Kline':
                re_array = array[['open', 'close', 'high', 'low']]
                data_li = list(row.tolist() for index, row in re_array.iterrows())

                close = array['close'].tolist()
                #width=width1 * 10 / 11, height=(height1 * 10 / 11) / len(labels)

                kline = (
                    Kline(init_opts=opts.InitOpts(width="1100px",height="500px"))
                        .add_xaxis(time)
                        .add_yaxis(label1[0],data_li)

                        .set_global_opts(

                        xaxis_opts=opts.AxisOpts(is_scale=True),
                        yaxis_opts=opts.AxisOpts(
                            is_scale=True,
                            splitarea_opts=opts.SplitAreaOpts(
                            is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                            ),
                        ),
                        datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
                        title_opts=opts.TitleOpts(title=label1[0] + "-" + optInterval)

                    )
                )



                # 计算移动平均
                if len(close) > 10:
                    ma10 = CalculateMA(close, 10)

                    line1 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA10", ma10)
                            #.set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )
                    kline.overlap(line1)

                if len(close) > 20:
                    ma20 = CalculateMA(close, 20)
                    line2 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA20", ma20)
                        # .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )
                    kline.overlap(line2)


                if len(close) > 30:
                    ma30 = CalculateMA(close, 30)

                    line3 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA30", ma30)
                        # .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )

                    kline.overlap(line3)
                tl.add(kline,label1[0] + "-" + optInterval)

            else:  # label1[2]==open/close/volume
                if label1[2] == 'Open':
                    list_aft = array['open'].tolist()
                elif label1[2] == 'Close':
                    list_aft = array['close'].tolist()
                elif label1[2] == 'High':
                    list_aft = array['high'].tolist()
                elif label1[2] == 'Low':
                    list_aft = array['low'].tolist()
                elif label1[2] == 'Volume':  # volume
                    list_aft = array['volume'].tolist()
                else:
                    list_aft = array['amount'].tolist()



                line = (
                    Line()
                        .add_xaxis(time)
                        .add_yaxis(label1[0] + "-" + label1[2], list_aft)
                        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                        yaxis_opts=opts.AxisOpts(
                                            is_scale=True,
                                            splitarea_opts=opts.SplitAreaOpts(
                                                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                            ),
                                        ),
                                        datazoom_opts=[opts.DataZoomOpts(pos_bottom="-8%")],
                                        title_opts=opts.TitleOpts(title=label1[0] + "-" + label1[2]))
                        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

                )



    return tl

#not ok...
def listToHtml(result,title):
    #将数据转换为html的table
    #result是list[list1,list2]这样的结构
    #title是list结构；和result一一对应。titleList[0]对应resultList[0]这样的一条数据对应html表格中的一列
    d = {}
    index = 0
    for t in title:
        d[t]=result[index]
        index = index+1
    df = pd.DataFrame(d)
    df = df[title]
    h = df.to_html(index=False)
    return h
#no ok
def stock_info_html():

    data=ts.get_today_all()

    title=data.columns.values.tolist()
    re_array=data[['code', 'name', 'changepercent', 'trade','open','high','low','settlement','volume','turnoverratio']]
    data_li = list(row.tolist() for index, row in re_array.iterrows())
    #以上接口获取特别慢。。。