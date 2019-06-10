import tushare as ts
import time
from app.models import News
import threading
from app import db
pro = ts.pro_api('1271fb1250f168b75ba0b4cb017370dbb22885fa387936ac1a60dca3')
from datetime import date, time, datetime, timedelta


def runTask(func):
   # Init time
   global timer
   timer = threading.Timer(20, func)
   timer.start()



def get_news():
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d')
    print(strnow)
    # First next run time
    '''
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print(strnext_time)
    '''
    pasttime = now - timedelta(days=1)
    paststr = pasttime.strftime('%Y-%m-%d')
    print(paststr)

    strnow.replace("/", "-")
    paststr.replace("/", "-")

    df = pro.news(src='sina', start_date=strnow, end_date=paststr)

    print(df)
    for index, row in df.iterrows():

        news=News()
        news.timestamp=index
        news.title=row['title']
        news.body=row['content']
        news.author='default'
        db.session.add(news)
        db.session.commit()
    newss=News.query.all()
    for n in newss:
        print(n.id, n.body)

