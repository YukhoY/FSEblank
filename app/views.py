#coding: utf8
from flask import render_template, flash, redirect, session, url_for, request, g
import app.charts as charts
from flask_login import login_user, logout_user, current_user, login_required
from .forms import *
from .models import *
from . import app, db, lm
import time, datetime
from strategy_run import shell_call as sc

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html", title='index', us=g.user)


@app.route("/login", methods=['GET', 'POST'])
@app.route("/login.html", methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title='login', form=LoginForm(), us=g.user)

filename=''#global
@app.route("/strategy", methods=['GET', 'POST'])
@app.route("/strategy.html", methods=['GET', 'POST'])
@login_required
def strategy():
    if request.method == 'GET':
        return render_template('strategy.html', title='strategy', us=g.user)
    if request.method == 'POST':
        print(request.form)
        print(request.form.get("strname"))
        print(request.form.get("strcodes"))
        #global is a little dangerous
        filename = './strategies/' + g.user.username + '_' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) +  '_' + request.form.get("strname").replace(" ", "%20") + ".py"
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(request.form.get("strcodes").replace("\r\n", "\n"))


        graph,summary=sc.shell_call(filename)

        return render_template('StrategyBack.html', title='strategy', us=g.user,
                               myechart=graph.render_embed(),alpha=summary['alpha'],beta=summary['beta'],
                               sharpe=summary['sharpe'],info_ratio=summary['information_ratio'],
                               sortino=summary['sortino'],total_returns=summary['total_returns'],
                               annualized_returns=summary['annualized_returns'],
                               benchmark_total_returns=summary['benchmark_total_returns'],
                               benchmark_annualized_returns=summary['benchmark_annualized_returns'],
                               volatility=summary['volatility'],
                               max_drawdown=summary['max_drawdown'],tracking_error=summary['tracking_error'],
                               downside_risk=summary['downside_risk'],total_value=summary['total_value']
                               )



@app.route("/MyStrategy", methods=['GET', 'POST'])
@app.route("/MyStrategy.html", methods=['GET', 'POST'])
@login_required
def MyStrategy():
    if request.method == 'GET':
        return render_template('MyStrategy.html', title='MyStrategy', us=g.user)
    if request.method == 'POST':  #
        return render_template('StrategyBack.html',us=g.user)


@app.route("/community", methods=['GET', 'POST'])
@app.route("/community.html", methods=  ['GET', 'POST'])
@login_required
def community():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('community.html', title='community', us=g.user, posts=posts, pagination=pagination, endpoint=page)

@app.route("/community-content/<int:contentnum>", methods=['GET', 'POST'])
@app.route("/community-content.html", methods=  ['GET', 'POST'])
@login_required
def community_content(contentnum):
    if request.method == 'POST':
        newcom = request.form.get('comment_content')
        post = Post.query.get(contentnum)
        print(newcom)
        newcomment = Comment(body=newcom, author= g.user, originpost=post, timestamp=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())))
        db.session.add(newcomment)
        db.session.commit()
        comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.id.desc())
        return render_template('community-content.html', title='strategy', us=g.user, post = post, comment = comments)
    if request.method == 'GET':
        post = Post.query.get(contentnum)
        comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.id.desc())
        return render_template('community-content.html', title='strategy', us=g.user, post = post, comment = comments)



@app.route("/write-article", methods=['GET', 'POST'])
@app.route("/write-article.html", methods=  ['GET', 'POST'])
@login_required
def writearticle():
    if request.method == 'POST':
        artititle = request.form.get('articletitle')
        artcont = request.form.get('articlecontent')
        print(artititle, artcont)
        newart = Post(title=artititle, body=artcont, author=g.user, timestamp=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())))
        db.session.add(newart)
        db.session.commit()
        return redirect(url_for('community'))
    if request.method == 'GET':
        return render_template('write-article.html', title='write', us=g.user)


@app.route("/signup", methods=['GET', 'POST'])
@app.route("/signup.html", methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功!请登录!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='signup', form=form, us=g.user)

@app.route("/news", methods=['GET', 'POST'])
@app.route("/news.html", methods=['GET', 'POST'])
def news():
    page = request.args.get('page', 1, type=int)
    pagination = News.query.order_by(News.id.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('news.html', title='news', us=g.user, posts=posts, pagination=pagination,endpoint=page)

@app.route("/news-content/<int:contentnum>", methods=['GET', 'POST'])
def news_content(contentnum):
    if request.method == 'GET':
        post = News.query.get(contentnum)
        return render_template('news-content.html', title='news', us=g.user, post = post)




@app.route('/logout')
def logout():
    print(current_user, '退出登录')
    logout_user()
    return redirect(url_for('index'))
#title='首页'



@app.route('/market.html', methods=['GET', 'POST'])
@app.route('/market', methods=['GET', 'POST'])
@login_required
def draw():
    if request.method=='GET':
        hs = charts.bar.create_hs()  # return page
        return render_template('market.html',
                               myechart=hs.render_embed(),
                               script_list=hs.js_dependencies.items,
                               us=g.user)

    if request.method=='POST':

        code=[]
        if request.form['code']!='':
            code.append(request.form['code']+'-'+"Kline")
        if request.form['code2']!='':
            code.append(request.form['code2']+'-'+"Kline")

        print(code)
        mode_combo = 'KLine'
        startdate = request.form['startdate']
        print(startdate)
        optInterval = request.form['interval']
        print(optInterval)
        width1 = 0
        length1 = 0
        #以上内容要做正则性判断
        ok=1
        if ok==1:
            chart=charts.bar.stock_draw(code,mode_combo,startdate,optInterval)
            return render_template('market.html',
                                   myechart=chart.render_embed(),
                                  script_list=chart.js_dependencies.items,
                                   us=g.user)
        else:
            pass
        #return render_template() 返回错误页面提示信息




'''
@app.route('/bar')
def bar():
    _bar = charts.bar.create_charts()#return page
    print("我画了一张股票图;)")
    print(_bar.js_dependencies.items)
    return render_template('base.html',
                           title='柱状图',
                           source_file='bar',
                           myechart=_bar.render_embed(),
                           script_list=_bar.js_dependencies.items)

'''



'''
@app.route('/boxplot')
def boxplot():
    _boxplot = charts.boxplot.create_charts()
    return render_template('base.html',
                           title='箱线图',
                           source_file='boxplot',
                           myechart=_boxplot.render_embed(),
                           script_list=_boxplot.get_js_dependencies())


@app.route('/effectscatter')
def effectscatter():
    _es = charts.effectscatter.create_charts()
    return render_template('base.html',
                           title='动态散点图',
                           source_file='effectscatter',
                           myechart=_es.render_embed(),
                           script_list=_es.get_js_dependencies())


@app.route('/funnel')
def funnel():
    _funnel = charts.funnel.create_charts()
    return render_template('base.html',
                           title='漏斗图',
                           source_file='funnel',
                           myechart=_funnel.render_embed(),
                           script_list=_funnel.get_js_dependencies())


@app.route('/gauge')
def gauge():
    _gauge = charts.gauge.create_charts()
    return render_template('base.html',
                           title='仪表盘',
                           source_file='gauge',
                           myechart=_gauge.render_embed(),
                           script_list=_gauge.get_js_dependencies())


@app.route('/geo')
def geo():
    _geo = charts.geo.create_charts()
    return render_template('base.html',
                           title='地理坐标系',
                           source_file='geo',
                           myechart=_geo.render_embed(),
                           script_list=_geo.get_js_dependencies())


@app.route('/geolines')
def geolines():
    _geolines = charts.geolines.create_charts()
    return render_template('base.html',
                           title='地理坐标系线图',
                           source_file='geolines',
                           myechart=_geolines.render_embed(),
                           script_list=_geolines.get_js_dependencies())


@app.route('/graph')
def graph():
    _graph = charts.graph.create_charts()
    return render_template('base.html',
                           title='关系图',
                           source_file='graph',
                           myechart=_graph.render_embed(),
                           script_list=_graph.get_js_dependencies())


@app.route('/heatmap')
def heatmap():
    _heatmap = charts.heatmap.create_charts()
    return render_template('base.html',
                           title='热力图',
                           source_file='heatmap',
                           myechart=_heatmap.render_embed(),
                           script_list=_heatmap.get_js_dependencies())


@app.route('/kline')
def kline():
    _kline = charts.kline.create_charts()
    return render_template('base.html',
                           title='K线图',
                           source_file='kline',
                           myechart=_kline.render_embed(),
                           script_list=_kline.get_js_dependencies())


@app.route('/line')
def line():
    _line = charts.line.create_charts()
    return render_template('base.html',
                           title='折线图',
                           source_file='line',
                           myechart=_line.render_embed(),
                           script_list=_line.get_js_dependencies())


@app.route('/line3d')
def line3d():
    _line3d = charts.line3d.create_charts()
    return render_template('base.html',
                           title='3D折线图',
                           source_file='line3d',
                           myechart=_line3d.render_embed(),
                           script_list=_line3d.get_js_dependencies())


@app.route('/liquid')
def liquid():
    _liquid = charts.liquid.create_charts()
    return render_template('base.html',
                           title='水球图',
                           source_file='liquid',
                           myechart=_liquid.render_embed(),
                           script_list=_liquid.get_js_dependencies())


@app.route('/map')
def map():
    _map = charts.map.create_charts()
    return render_template('base.html',
                           title='地图',
                           source_file='map',
                           myechart=_map.render_embed(),
                           script_list=_map.get_js_dependencies())



@app.route('/pie')
def pie():
    _pie = charts.pie.create_charts()
    return render_template('base.html',
                           title='饼图',
                           source_file='pie',
                           myechart=_pie.render_embed(),
                           script_list=_pie.get_js_dependencies())





@app.route('/radar')
def radar():
    _radar = charts.radar.create_charts()
    return render_template('base.html',
                           title='雷达图',
                           source_file='radar',
                           myechart=_radar.render_embed(),
                           script_list=_radar.get_js_dependencies())




@app.route('/scatter')
def scatter():
    _scatter = charts.scatter.create_charts()
    return render_template('base.html',
                           title='散点图',
                           source_file='scatter',
                           myechart=_scatter.render_embed(),
                           script_list=_scatter.get_js_dependencies())




@app.route('/themeriver')
def themeriver():
    _themeriver = charts.themeriver.create_charts()
    return render_template('base.html',
                           title='主题河流图',
                           source_file='themeriver',
                           myechart=_themeriver.render_embed(),
                           script_list=_themeriver.get_js_dependencies())


@app.route('/treemap')
def treemap():
    _treemap = charts.treemap.create_charts()
    return render_template('base.html',
                           title='树图',
                           myechart=_treemap.render_embed(),
                           script_list=_treemap.get_js_dependencies())


@app.route('/wordcloud')
def wordcloud():
    _wordcloud = charts.wordcloud.create_charts()
    return render_template('base.html',
                           title='词云图',
                           source_file='wordcloud',
                           myechart=_wordcloud.render_embed(),
                           script_list=_wordcloud.get_js_dependencies())


'''
