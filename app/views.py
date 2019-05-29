#coding: utf8
from flask import render_template, flash, redirect, session, url_for, request, g
import app.charts as charts
from flask_login import login_user, logout_user, current_user, login_required
from .forms import *
from .models import User
from . import app, db, lm

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
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
@app.route("/login.html", methods=['GET', 'POST'])
def login():
    if g.user is None:
        return render_template('login.html')
    if g.user is not None and g.user.is_authenticated:
        print('已经登陆')
        return redirect(url_for('index'))
    form = LoginForm()
    #print('收到表格')
    #print(form.username.data, form.password.data)
    #print(form.validate_on_submit())
    if form.validate_on_submit():
        #print('判断了有输入')
        #print(form.username.data, form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        #print('获取user信息')
        if user is None or not user.check_password(form.password.data):
            #print('用户名或密码无效')
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user)
        #print('登陆成功')
        return redirect(request.args.get('next') or url_for('index'))
    #print('输入无效')
    return render_template('login.html', form=LoginForm())

@app.route('/market')
@app.route('/market.html')
@login_required
def market():
    return render_template('market.html')

@app.route("/strategy", methods=['GET', 'POST'])
@app.route("/strategy.html", methods=['GET', 'POST'])
@login_required
def strategy():
    if request.method == 'GET':
        return render_template('strategy.html')

@app.route("/signup", methods=['GET', 'POST'])
@app.route("/signup.html", methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        print('已经登陆')
        return redirect(url_for('index'))
    form = SignupForm()
    for i in form.email.errors:
        print(i)
    for i in form.username.errors:
        print(i)
    for i in form.password.errors:
        print(i)
    for i in form.password2.errors:
        print(i)
    print(form.username.errors)
    print(form.password.errors)
    print(form.password2.errors)
    print('收到表格')
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print('已写入数据库')
        flash('注册成功!请登录!')
        return redirect(url_for('login'))
    print('输入无效')
    return render_template('signup.html', form=form)

@app.route("/news", methods=['GET', 'POST'])
@app.route("/news.html", methods=['GET', 'POST'])
def news():
    if request.method == 'GET':
        return render_template('news.html')

@app.route("/MyStrategy", methods=['GET', 'POST'])
@app.route("/MyStrategy.html", methods=['GET', 'POST'])
@login_required
def MyStrategy():
    if request.method == 'GET':
        return render_template('MyStrategy.html')

@app.route('/logout')
def logout():
    logout_user()
    print('退出登录')
    return redirect(url_for('index'))
#title='首页'

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


@app.route('/grid')
def grid():
    _grid = charts.grid.create_charts()
    return render_template('base.html',
                           title='Grid类',
                           source_file='grid',
                           myechart=_grid.render_embed(),
                           script_list=_grid.get_js_dependencies())


@app.route('/overlap')
def overlap():
    _overlap = charts.overlap.create_charts()
    return render_template('base.html',
                           title='Overlap类',
                           source_file='overlap',
                           myechart=_overlap.render_embed(),
                           script_list=_overlap.get_js_dependencies())


@app.route('/timeline')
def timeline():
    _timeline = charts.timeline.create_charts()
    return render_template('base.html',
                           title='Timeline类',
                           source_file='timeline',
                           myechart=_timeline.render_embed(),
                           script_list=_timeline.get_js_dependencies())


'''
'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
'''