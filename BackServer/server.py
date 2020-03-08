"""
@FileName   : server.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 用Tornado作为Windows下服务器,托管flask的app，也可以使用apache。linux下可以用uwsgi和gunicorn
@Time       : 7/03/2020 3:39 pm
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
from flask_app import app
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
import platform

#  python3.8 asyncio 在 windows 上默认使用 ProactorEventLoop 造成的，而不是之前的 SelectorEventLoop。
#　针对windows平台单独处理
#if platform.system() == "Windows":
#    import asyncio
#    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
s = HTTPServer(WSGIContainer(app))
s.listen(9999)  # 监听 9999 端口
IOLoop.instance().start()
