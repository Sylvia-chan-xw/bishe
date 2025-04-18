from flask import Flask,session,request,redirect,render_template
import re
app = Flask(__name__)
app.secret_key='this is secret key'

from views.page import page
from views.user import user
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

@app.route('/')
def hello_world():  # put application's code here
    return session.clear()

@app.before_request
def before_request():
    pat=re.compile(r'/static')
    if re.search(pat,request.path):return #判断是否访问静态目录
    elif request.path=='/user/login' or request.path=='/user/register':return #判断如果进入登陆注册界面
    elif session.get('username'):return #判断如果有session的情况下是否能自由切换导航路由
    return redirect('/user/login') #如果三个都不满足，直接到login页面

@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')

if __name__ == '__main__':
    app.run()
