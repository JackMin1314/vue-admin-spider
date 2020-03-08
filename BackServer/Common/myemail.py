"""
@FileName   : myemail.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 实现用户注册时发送的邮箱验证码
@Time       : 2020/1/30 11:01
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
from threading import Thread
from flask_mail import Message
from Log.errlogs import logger


def send_async_email(app, mail, msg):
    with app.app_context():
        mail.send(msg)


def send_email_capture(app, mail, email, capture):
    """用于注册时候异步发送邮件验证码
    注意频繁发送邮件可能会导致550 MailBox not found and access denied错误
    :param app: Flask实例对象
    :param mail: Flask的MAIL实例
    :param email: 合法用户注册的email
    :param capture: 随机数字验证码
    :return: bool
    """
    flag = False
    msg = Message(subject='Spider用户登录邮箱验证码：', recipients=[email])
    msg.html = '<!DOCTYPE HTML><html><head></head><body><p><font size="5",color=black>尊敬的用户: 您好!</font></p>&nbsp &nbsp &nbsp 您 <font color="#ff9955">Spider</font> 邮箱登录的验证码为: <span style="border-bottom: 1px dashed rgb(204, 204, 204);"><font size="5" color =green><b>{0}</b></font></span>有效期限为<b><font color ="rgb(204, 195, 175)">10分钟</font></b>，请尽快前往注册。(<i>如果不是您提交的申请，请忽略</i>)<p>&nbsp &nbsp &nbsp 感谢您的使用。</p></body></html>'.format(
        capture)
    thread = Thread(target=send_async_email, args=[app, mail, msg])
    # .start()会安排对象在另外一个单独线程中运行run()方法,是异步执行。run()是普通的同步执行
    try:
        thread.start()
        flag = True
        print("{0} 邮件发送成功".format(email))
        logger.info("%s邮箱验证码%s发送成功" % (email, capture))
    except Exception as e:
        flag = False
        print("{0} 邮件发送失败".format(email))
        logger.error("%s邮箱验证码%s发送失败,原因：%s" % (email, capture, e))
    return flag
