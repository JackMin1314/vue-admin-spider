"""
@FileName   : flask_app.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 服务后端业务逻辑处理，结合数据库处理向前端提供数据，进行权限验证
@Time       : 2020/1/27 12:49
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
from Modules.runSpider import runSpider
from Log.errlogs import logger, cleanLogging
from Common.myemail import send_email_capture
from Encryption.encryp import checkPW, computePW, create_Salt
from Common import UserAction as User_Action
from Common.timed_db_backup import timed_task
from Common.common import getlocaltime, getCapture, getMachineInfo, createDirFile, threadWorker
from Common import DataSynchronism as DB_Sync
from Config.config import *
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
from flask import Flask, request, session, jsonify, make_response, send_from_directory, abort
import os
import sys
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 导入相关配置
# 导入数据库处理
# 导入通用模块
# 导入加密验证模块
# 导入邮箱验证码发送模块
# 导入日志记录模块

# 导入Module业务功能

app = Flask(__name__)
app.debug = True

# 生产环境下修改下面的值会导致之前的token不能使用
app.secret_key = my_secretKey
# 设置session过期时间
app.config['PERMANENT_SESSION_LIFETIME'] = session_lifeTime
csrf = CSRFProtect(app)
# 先跨域，在路由
CORS(app)

# 配置mail ./Config/config.py
app.config['MAIL_SUPPRESS_SEND'] = MAIL_SUPPRESS_SEND
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

mail = Mail(app)

serverlogs_path = ""
spider_file_status = False
spider_file_name = ""
# @app.after_request
# def after_request(response):
#     # 调用函数生成 csrf_token
#     csrf_token = generate_csrf()
#     # 通过 cookie 将值传给前端
#     response.set_cookie("csrf_token", csrf_token)
#     return response


# 首次Get请求下发CSRF-TOKEN
@app.route('/', methods=["GET", "POST"])
def first_request():
    """首次Get请求下发CSRF-TOKEN以及相关cookies数据

    :return: json格式字符串
    """
    # response = response()
    # 调用函数生成 csrf_token; generate_csrf()里面在包里的session.py中
    # hashlib.sha1(os.urandom(64)).hexdigest()
    # s = URLSafeTimedSerializer(secret_key, salt='wtf-csrf-token')

    csrf_token = generate_csrf()
    # 通过 cookie 将值传给前端
    result = {"code": 0, 'msg': 'success'}
    resp = make_response(jsonify(result))
    # 指定cookie放在/位置
    resp.set_cookie("csrf_token", csrf_token, httponly=False, path='/')
    resp.set_cookie('datetime', getlocaltime())
    # 允许前端可以通过获取header的字段
    resp.headers['Access-Control-Expose-Headers'] = 'csrf_token,Set-Cookie'
    resp.headers['csrf_token'] = csrf_token
    resp.headers['supportsCredentials'] = True
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # resp.headers['Access-Control-Allow-Credentials'] = True
    return resp


'''

几点注解前端 axios(默认axios是不带cookies请求的，而且后端设置了跨域)
(一) 当前端配置withCredentials=true时, 后端配置Access-Control-Allow-Origin不能为*, 必须是相应地址
(二) 当配置withCredentials=true时, 后端需配置Access-Control-Allow-Credentials
(三) 当前端配置请求头时, 后端需要配置Access-Control-Allow-Headers为对应的请求头集合

'''


# 如果路由想取消CSRF就在app.route上面添加@csrf.exempt; csrf-token对get方法无效
@app.route('/login', methods=['POST', 'GET'])
def login():
    """ 前端登录请求post请求，从数据库中验证params完整性和正确性,并设置相应的cookies和session

    :return: json结果
    """
    logintime = ""
    if request.method == 'POST':
        # 这里进行了折衷的处理为了实现登录顶掉他人登录的需求.(人性化的做法应该是提示在他处登录，询问要不要踢掉或者在其他地方先推出，这边在登陆)
        quit()
        print(request.form.get("username", type=str, default=""))
        # 判断用户名密码是否正确
        username = request.form.get("username", type=str, default="")
        passwd = request.form.get("passwd", type=str, default="")
        if username == "" or passwd == "":
            code = "-1"
            msg = "用户名或密码为空或不合法"
        # 用户名不空查询后端数据
        else:
            result = DB_Sync.query_redis(username)
            # 用户不存在
            if result["code"] == "-1":
                code = "-1"
                msg = "用户名或密码错误"
            # 用户存在 result["code"]返回0,1
            else:
                salt = ""
                # 判断密码是否正确
                if result["data"] != "":
                    salt = result["data"]["USER_SALT"]
                    localPW = result["data"]["USER_PASSWD"]
                print("redis data", result["data"])
                print("computePasswd", computePW(passwd, salt))
                # 验算用户传递的密码是否和数据库中保存的一致
                isConsistent = checkPW(computePW(passwd, salt), localPW)
                # 密码输入正确
                if isConsistent:
                    code = "0"
                    msg = "登录验证成功"
                    session["logintime"] = getlocaltime()
                    if session.get("isLogin"):
                        logger.warning("%s用户登录失败,原因是已在其他地方登录" % username)
                        return jsonify(code="-1", msg="您已在其他地方登录")
                    session["isLogin"] = True
                    session["username"] = username
                    logintime = getlocaltime()
                    logger.info("%s用户登录成功" % username)
                # 密码输入错误
                else:
                    code = "-1"
                    msg = "用户名或密码错误"
                    logger.warning("%s用户登录输入密码错误,登录失败" % username)
        resp = jsonify(code=code, msg=msg)
        resp.set_cookie('datetime', getlocaltime())
        resp.set_cookie('logintime', logintime)
        resp.set_cookie('username', request.form.get("username", type=str, default="null"),
                        expires=max_ageTime)  # max_age单位是秒，过期时间
        return resp
    # 如果是其他请求方法
    else:
        resp = jsonify(
            code='-1', msg='{} Method is not allowed !'.format(request.method))
        resp.set_cookie('datetime', getlocaltime())
        resp.set_cookie('logintime', logintime)
        resp.set_cookie('username', request.form.get("username", type=str, default="null"),
                        expires=max_ageTime)  # max_age单位是秒，过期时间
        return resp


# 这里当前的退出逻辑采用GET，同时删除session等数据
@app.route('/quit')
def quit():
    """ get方式退出登录并清除session数据

    :return: json结果
    """
    username = session.get("username")
    print(username)
    print('session["isLogin"]=', session.get("isLogin"))
    if username is not None and session.get("isLogin"):
        session["isLogin"] = False
        csrf_token = session.get('csrf_token')
        session.clear()
        session['csrf_token'] = csrf_token
        resp = jsonify(code="0", msg="清除服务端数据成功!")
        logger.info("%s用户退出成功,已经清除服务端session数据" % username)
        return resp
    else:
        resp = jsonify(code="1", msg="您已经退出登录")
        logger.error("拒绝响应%s用户，原因是: 您已经退出登录" % username)
        return resp


# 更新用户的密码，更新完毕要求用新密码重新登录
@app.route('/update_passwd', methods=["POST"])
def updatePWD():
    """Post方式用户更新密码,需要核实用户登录状态,用原来的salt加密后新密码入库,并要求重新登录。

    :return: json结果
    """
    username = session.get("username")
    if session.get("isLogin") and username is not None:
        # 处于登录的状态的时候，重新生成密码存储到mysql而且同步刷新Redis
        old_pwd = request.form.get("old_passwd", type=str, default="")
        new_pwd = request.form.get("new_passwd", type=str, default="")
        # 下面获取该用户原始数据进行验证
        result = DB_Sync.query_redis(username)
        print("查询用户本地结果为:", result)
        localPW = result["data"]["USER_PASSWD"]
        salt = result["data"]["USER_SALT"]
        # 用户原始密码输入正确，允许修改mysql然后同步redis
        print('计算结果:', computePW(old_pwd, salt))
        if checkPW(computePW(old_pwd, salt), localPW):
            # 用原来的盐加密生成新的用户密码
            compute_new_pwd = computePW(new_pwd, salt)
            isOK = DB_Sync.sync_redis_insert(username, compute_new_pwd, salt)
            if isOK:
                resp = jsonify(code="0", msg="密码修改成功，请用新的密码登录")
                resp.set_cookie("datetime", getlocaltime())
                logger.warning("%s用户修改密码成功,并退出登录" % username)
                # 修改了密码后,需要重新登录,应该清除session数据。然后刷新redis，不然会导致login时候的redis用之前的
                DB_Sync.refresh_redis(username)
                session["isLogin"] = False
                session.clear()
            else:
                resp = jsonify(code="-1", msg="密码修改失败，请重试")
                print("{0}用户修改密码失败,原密码:{1}|新密码:{2}".format(
                    username, localPW, compute_new_pwd))
                logger.warning("%s用户修改密码失败" % username)
        else:
            # 传递过来的用户原始密码为假
            resp = jsonify(code="-1", msg="您原始密码输入有误，请重新输入")
            logger.error("%s用户修改密码失败,原始密码不正确" % username)
    else:
        # 该用户已经退出登录了，不处于登录状态
        resp = jsonify(code="1", msg="您当前不处于登录状态，请先登录")
        logger.warning("%s用户当前处于非登录状态,修改密码失败" % username)
    return resp


# 根据邮箱发送验证码，建议使用get方法
@app.route('/get_capture', methods=["GET", "POST"])
def sendCapture():
    """ 发送邮箱验证码

    :return: json结果
    """
    if request.method == "POST":
        email = request.form.get("email")
    if request.method == "GET":
        email = request.args.get("email")
    print(email)
    if email is None:
        code = "-1"
        msg = "未输入邮箱地址"
    else:
        captureCode = getCapture()
        send_email_capture(app, mail, email, captureCode)
        code = "0"
        msg = "发送成功，请尽快前往注册"
        isOk = DB_Sync.create_redis_Capture(email, captureCode)
        if not isOk:
            print("保存十分钟验证码失败")
            code = "-1"
            msg = "保存十分钟验证码失败"
    return jsonify(code=code, msg=msg)


# 新用户注册入库
@app.route('/register', methods=["GET", "POST"])
def register():
    """判断为新用户，新用户注册，需要结合传递过来的邮箱（邮箱要唯一）以及邮箱验证码，用户名（唯一）和密码

    :return: json结果
    """
    if request.method == "POST":
        email = request.form.get("email", type=str, default="")
        username = request.form.get("username", type=str, default="")
        passwd = request.form.get("passwd", type=str, default="")
        capture = request.form.get("capture", type=str, default="")
        # 用户名，密码，验证码, 邮箱为空
        if not (username and passwd and email and capture):
            code = "-1"
            msg = "用户输入了空参数"
        # 查询本地是否有同名用户名和邮箱
        else:
            # 本地数据库不存在已注册相关用户名和邮箱信息,核实验证码注册
            if not DB_Sync.exist_UserName_email(username, email):
                captureCode = DB_Sync.query_redis_Capture(
                    email)       # 如果email没找到,capturecode为None而不是""
                if captureCode == capture:
                    code = "0"
                    msg = "注册成功"

                    # 新用户写入数据库
                    # 先对用户密码加密,需要盐
                    salt = create_Salt()
                    passwd = computePW(passwd, salt)
                    # 新用户入库
                    isOk = DB_Sync.sync_redis_insert(
                        username, passwd, salt, email)
                    if not isOk:
                        code = "-1"
                        msg = "新用户注册入库失败"
                    else:
                        # 刷新同步到redis
                        DB_Sync.refresh_redis(username)
                        session['isLogin'] = True
                        session['username'] = username
                        # 最后创建该用户的文件夹
                        iscreate, user_home_str = User_Action.create_user_homedir(
                            username)
                        if iscreate:
                            logger.info("为新注册用户%s创建文件夹成功" % username)
                        else:
                            logger.error("为新注册用户%s创建文件夹失败" % username)
                else:
                    code = "-1"
                    msg = "验证码失效或错误"
            # 本地已存在相关信息用户信息
            else:
                code = "-1"
                msg = "用户名或邮箱已存在，请重新输入"
    else:
        code = '-1'
        msg = '{} Method is not allowed !'.format(request.method)
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 忘记密码
@app.route('/forget_passwd', methods=['POST'])
def forgetPWD():
    """用户名和邮箱以及邮箱的验证码和新密码,查询本地用户名和邮箱是否对应，是发送验证码，然后检验验证码

    :return: json结果
    """
    email = request.form.get("email", type=str, default="")
    username = request.form.get("username", type=str, default="")
    captureCode = request.form.get("capture", type=str, default="")
    new_passwd = request.form.get("new_passwd", type=str, default="")
    # 本地数据库无对应数据，修改不了
    if not DB_Sync.exist_UserName_email(username, email):
        code = "-1"
        msg = "用户名或者邮箱错误"
    # 本地有数据可以修改,核对验证码
    else:
        # 判断根据邮箱查到的用户名是否一致,避免修改他人的数据
        # 验证码一致,而且email和用户名也对应.(默认不考虑用户忘记用户名的情况)
        isConsist = DB_Sync.is_consistent(email, username)
        if captureCode == DB_Sync.query_redis_Capture(email) and isConsist:
            result = DB_Sync.query_redis(username)
            # 根据用户名查询到了结果(salt)
            print(result)
            salt = result["data"]['USER_SALT']
            compute_new_pwd = computePW(new_passwd, salt)
            isOK = DB_Sync.sync_redis_insert(
                username, compute_new_pwd, salt, email)
            print("is ok", isOK)
            if isOK:
                code = "0"
                msg = "密码重置成功，请用新的密码登录"
                logger.info("%s用户密码修改成功" % username)
                # 修改密码后需要清除session数据
                session["isLogin"] = False
                session.clear()
                if DB_Sync.refresh_redis(username):
                    print("redis刷新成功...")
                else:
                    print("redis刷新失败...")
            else:
                code = "-1"
                msg = "密码重置失败，请重试"
                print("{0}用户重置密码失败".format(username))
                logger.error("%s用户重置密码失败" % username)
        else:
            code = "-1"
            msg = ("验证码失效" if isConsist else "用户名密码不一致")
            logger.error("%s用户重置密码失败,原因:%s" % (username, msg))
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 用户自己删除账户所有数据,需要验证码
@app.route('/erase_user', methods=["POST"])
def eraseUSER():
    """ 清空redis数据并删除本地数据库用户信息，同步redis

    :return: json结果
    """
    username = request.form.get("username", type=str, default="")
    email = request.form.get("email", type=str, default="")
    captureCode = request.form.get("capture", type=str, default="")
    # 判断是否处于登录状态
    if session["isLogin"] and session.get("username") == username:
        # 判断验证码是否正确
        isConsist = DB_Sync.is_consistent(email, username)
        if captureCode == DB_Sync.query_redis_Capture(email) and isConsist:
            # 删除redis数据，然后删除本地mysql数据
            isDelete = DB_Sync.sync_redis_delete(username, email)
            if isDelete:
                code = "0"
                msg = "用户账号注销成功"
                session["isLogin"] = False
                # 清除服务器数据
                session.clear()
                logger.info("%s用户账号注销成功" % username)
                # 用户删除成功时候，删除用户目录
                if User_Action.remove_user_homedir(username):
                    logger.warning("注销删除%s用户文件目录数据成功" % username)
                else:
                    logger.error("注销删除%s用户文件目录数据失败" % username)
            else:
                code = "-1"
                msg = "用户账号注销失败"
                logger.warning("%s用户账户注销失败" % username)
        else:
            code = "-1"
            msg = "验证码不一致"
            logger.info("%s用户输入验证码不一致" % username)
    # 当前不是处于登录状态
    else:
        code = "-1"
        msg = "您当前不处于登录状态，请先登录"
        logger.warning("%s用户删除数据失败,原因:当前处于非登录状态" % username)
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 获取mysql用户列表
@app.route('/user_list', methods=["POST"])
def userList():
    """ 获取数据库中用户列表除了password和salt

    :return: json结果
    """
    username = request.form.get("username", type=str, default="")
    if session["isLogin"] and session.get("username") == username:
        result = DB_Sync.query_redis(username)
        userlock = result['data']['USER_LOCK']
        if userlock == 0:
            code = "0"
            msg = "获取用户列表成功"
            data = DB_Sync.user_list()
        else:
            return abort(401)
    else:
        code = "-1"
        msg = "您当前不处于登录状态，请先登录"
        data = ""
    resp = jsonify(code=code, msg=msg, data=data)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 添加获取系统当前硬件状态的信息
@app.route('/machine_info', methods=["GET"])
def machineInfo():
    """ 获取当前服务器部分运行状态和硬件资源信息

    :return: json结果
    """
    result = getMachineInfo()
    resp = jsonify(code="0", msg="获取系统资源信息成功", data=result)
    return resp


# 根据用户名返回其下所有文件和文件的属性大小、创建日期等
@app.route('/user_files_info', methods=["GET"])
def userFilesInfo():
    username = request.args.get("username")
    if session.get('username') == username and session.get('isLogin'):
        result = DB_Sync.query_redis(username)
        userlock = result['data']['USER_LOCK']
        if userlock == 0:
            userfiles_info = []
            # 返回该用户下的文件列表
            user_file_list = User_Action.user_file_list(username)
            if user_file_list:
                # 根据文件列表去获取文件的属性
                for li in user_file_list:
                    userfiles_info.append(
                        User_Action.user_file_info(username, li))
                return jsonify(code="0", msg="用户文件获取成功", data=userfiles_info)
            else:
                logger.error("%s用户文件夹为空" % username)
                return jsonify(code="1", msg="用户文件获取失败")
        else:
            return abort(401)
    else:
        return jsonify(code="-1", msg="您当前不处于登录状态，请先登录")


# 指定路径下文件下载
@app.route('/download_file')
def downLoadFile():
    """ 下载用户名下的文件
    http://127.0.0.1:9999/download_file?username=Allen&filename=b.pdf
    :return:
    """
    if request.method == "POST":
        username = request.form.get("username")
        filename = request.form.get("filename")
    if request.method == "GET":
        # 对于get其实flask会自动解析urldecode，因此如果前端请求用户名(本项目用户名前端有要求不含特殊字符)或者文件名不做处理的话，后端解析可能会导致出错
        # 例如前端请求filename=”我的C++笔记.md“ 后端解析filename的值就会变成 “我的C 笔记.md"
        # 因为+号被转义成%2B表示空格（可以通过query_string看到），我们可以对转义后的字符%2B进行替换成+
        # 但是个人不推荐这么做，因为: 1. 复杂，类似转义字符有"+、空格、/、%、#、&、="等,每个都需要整个字符考虑；2. 转义替换顺序有要求。顺序不当，可能会产生新的转义问题
        # 因而推荐前端进行url参数转义类似javascript的encodeURIComponent等，可以保证按照正常的解析不会出错
        username = request.args.get("username")
        filename = request.args.get("filename")
    # 有该文件
    # User_Action.create_user_rootdir()
    if username and filename:
        result = DB_Sync.query_redis(username)
        userlock = result['data']['USER_LOCK']
        # 如果前端请求带字符串格式就需要用eval去掉引号""
        # username = eval(username)
        # filename = eval(filename)
        is_exists, file_directory = User_Action.query_user_file(
            username, filename)
        # print("isexists, dictory", is_exists, file_directory)
        if userlock == 0:
            if is_exists:
                return send_from_directory(directory=file_directory, filename=filename.encode('utf-8').decode('utf-8'), as_attachment=True)
            else:
                return abort(404)
        else:
            return abort(401)
    else:
        return abort(404)


# 第一个是用户角色的调整，高级调整低级，同级无法互相调整，super(唯一)调整所有包括admin
# 第二个是设置账号锁定：super > admin > user
@app.route('/change_role', methods=['POST'])
def changeRole():
    """ 改变用户的类型和锁定用户

    :return: json结果
    """
    tup = ("user", "admin", "super")  # 用下标 0, 1, 2 来比较权限的大小！！
    # 当前修改者属性
    username = request.form.get("username", type=str, default="")
    # 被修改者的新属性
    othername = request.form.get("othername", type=str, default="")
    new_othertype = request.form.get("new_othertype", type=str, default="user")
    new_otherlock = request.form.get("new_otherlock", type=int, default=0)

    # 如果当前用户处于登录状态
    print(session["isLogin"], session.get("username"))
    if session["isLogin"] and session.get("username") == username:
        result = DB_Sync.query_redis(username)
        usertype = result["data"]["USER_TYPE"]
        userlock = result["data"]["USER_LOCK"]
        result = DB_Sync.query_redis(othername)
        othertype = result["data"]["USER_TYPE"]
        # # userlock = int(userlock, encoding='utf-8')
        # usertype = str(usertype, encoding='utf-8')
        # othertype = str(othertype, encoding='utf-8')
        # 当前用户不处于锁定状态，且当前用户的权限比被修改用户的权限高（能改）(这里就解决了自己修改自己的问题，自己只能降级自己)
        # 且改动权限不能超过自己的当前权限（改的幅度）
        if userlock == 0 and tup.index(othertype) < tup.index(usertype) and \
                tup.index(new_othertype) <= tup.index(usertype):
            ischanged = DB_Sync.change_user_permission(
                othername, new_othertype, new_otherlock)
            if ischanged:
                code = "0"
                msg = "用户权限修改成功"

            else:
                code = "-1"
                msg = "用户权限修改失败"
        else:
            code = "1"
            msg = "您没有权限执行操作"
    else:
        code = "-1"
        msg = "您当前不处于登录状态"
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 管理员或者super删除用户
@app.route('/delete_user', methods=["POST"])
def deleteUSER():
    """ 管理员或者super用户在用户管理界面删除其他用户(低权限用户)

    :return:
    """
    tup = ("user", "admin", "super")  # 用下标 0, 1, 2 来比较权限的大小！！
    # 当前修改者属性
    username = request.form.get("username", type=str, default="")
    # 被修改者的属性
    othername = request.form.get('othername', type=str, default="")
    otheremail = request.form.get("otheremail", type=str, default="")

    result = DB_Sync.query_redis(othername)
    # print(result)
    othertype = result["data"]["USER_TYPE"]
    # 判断当前用户是否在线
    if session.get("username") == username and session.get('isLogin'):
        # 获取当前用户的权限和锁定情况
        result = DB_Sync.query_redis(username)
        usertype = result["data"]["USER_TYPE"]
        userlock = result["data"]["USER_LOCK"]
        # 判断当前用户是否有权限删除,自己删除不了自己
        if userlock == 0 and tup.index(usertype) > tup.index(othertype):
            is_delete = DB_Sync.sync_redis_delete(othername, otheremail)
            if is_delete:
                code = "0"
                msg = "用户账号注销成功"
                logger.info("%s管理员注销%s用户成功" % (username, othername))
                # 用户删除成功时候，删除用户目录
                if User_Action.remove_user_homedir(username):
                    logger.warning("注销删除%s用户文件目录数据成功" % username)
                else:
                    logger.error("注销删除%s用户文件目录数据失败" % username)
            else:
                code = "-1"
                msg = "用户账号注销失败"
                logger.error("%s管理员注销%s用户失败" % (username, othername))
        else:
            code = "1"
            msg = "您没有权限执行操作"

    else:
        code = "-1"
        msg = "您当前不处于登录状态，请先登录"
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 用户自己删除自己文件夹下的文件
@app.route('/delete_user_file', methods=['POST'])
def deleteUserFile():
    username = request.form.get("username", type=str, default="")
    filename = request.form.get("filename", type=str, default="")
    if username == "" or filename == "":
        return jsonify(code="-1", msg="用户名或者文件名为空")
    # 当前用户处于登陆状态
    if session.get("username") == username and session.get("isLogin"):
        if User_Action.remove_user_file(username, filename):
            code = "0"
            msg = "文件删除成功"
        else:
            code = "-1"
            msg = "文件删除失败"
    else:
        code = "1"
        msg = "当前处于非登陆状态，请先登录"
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 删除清空服务器的日志文件内容BackServer/folders/errlogs.txt，只有super权限可以
@app.route('/clean_serve_log', methods=["POST"])
def super_cleanLog():
    """ 超级管理员清除服务器的所有用户行为日志errlogs.txt

    :return: json结果
    """
    username = request.form.get("username", type=str, default="")
    if session.get("isLogin") and session.get("username") == username:
        result = DB_Sync.query_redis(username)
        usertype = result["data"]["USER_TYPE"]
        userlock = result["data"]["USER_LOCK"]
        # 超级用户且没有被人为锁定
        if usertype == "super" and userlock == 0:
            if cleanLogging():
                code = "0"
                msg = "文件清除成功"
                logger.info("%s用户删除日志成功，具有权限为%s，锁定为%d" %
                            (username, usertype, userlock))
            else:
                code = "1"
                msg = "文件异常，无法清除"
                logger.error("%s用户删除日志失败,原因:文件异常，无法清除" % username)
        else:
            code = "-1"
            msg = "您没有权限执行该操作"
    else:
        code = "-1"
        msg = "您当前不处于登录状态，请先登录"
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 返回备份文件夹下的db_backup_dir的errlogs.txt和数据库备份文件
@app.route('/errlogs_db_info', methods=['GET'])
def super_logsBackup():
    """ 返回errlogs.txt和数据库备份文件的属性

    :return: json结果
    """
    is_exists, backup_dir = createDirFile(db_backup_dir)
    global serverlogs_path
    serverlogs_path = backup_dir
    filelistinfo = []
    if is_exists:
        filelist = User_Action.fileList(backup_dir)
        for file in filelist:
            filelistinfo.append(User_Action.fileListInfo(backup_dir, file))
        return jsonify(code="0", msg="用户文件获取成功", data=filelistinfo)
    else:
        return jsonify(code="-1", msg="服务端文件路径错误")


# 清空备份文件夹下的db_backup_dir的errlogs.txt和删除数据库备份文件,只有super权限可以
@app.route('/handle_logdb', methods=['POST'])
def super_Handle_LogDB():
    """ super清空errlogs.txt和删除db备份文件(正常来说应该保留最近一次备份的不允许删除,本项目不考虑此情况)

    :return: json结果
    """
    filename = request.form.get("filename", type=str, default="")
    username = request.form.get("username", type=str, default="")
    if session.get("isLogin") and session.get("username") == username:
        result = DB_Sync.query_redis(username)
        usertype = result["data"]["USER_TYPE"]
        userlock = result["data"]["USER_LOCK"]
        # 超级用户且没有被人为锁定
        if usertype == "super" and userlock == 0:
            # 如果是日志则清空
            if filename == serverlogs_name:
                if cleanLogging():
                    code = "0"
                    msg = "文件清空成功"
                    logger.info("%s用户删除日志成功，具有权限为%s，锁定为%d" %
                                (username, usertype, userlock))
                else:
                    code = "1"
                    msg = "文件异常，无法清除"
                    logger.error("%s用户删除日志失败,原因:文件异常，无法清除" % username)
            # 如果是备份文件则删除
            else:
                global serverlogs_path
                User_Action.fileDelete(
                    serverlogs_path + r'\{}'.format(filename))
                code = "0"
                msg = "文件删除成功"
                logger.info("%s用户删除文件%s成功，具有权限为%s，锁定为%d" %
                            (username, filename, usertype, userlock))
        else:
            code = "-1"
            msg = "您没有权限执行该操作"
    else:
        code = "-1"
        msg = "您当前不处于登录状态，请先登录"
    resp = jsonify(code=code, msg=msg)
    resp.set_cookie("datetime", getlocaltime())
    return resp


# 下载服务端备份数据库文件和errlogs日志
@app.route('/download_logdb', methods=['POST'])
def super_Download_LogDB():
    """ super管理员下载数据库备份文件和errlogs日志

    :return: json结果
    """
    username = request.form.get('username')
    filename = request.form.get('filename', type=str, default='')
    # 是否处于登录状态
    if session.get('username') == username and session.get('isLogin'):
        #　判断是否是super权限以及被人为锁定状态
        result = DB_Sync.query_redis(username)
        usertype = result['data']['USER_TYPE']
        userlock = result['data']['USER_LOCK']
        if usertype == 'super' and userlock == 0:
            logger.info('super用户%s下载了文件%s' % (username, filename))
            print('server path:', serverlogs_path)
            return send_from_directory(directory=serverlogs_path, filename=filename.encode('utf-8').decode('utf-8'), as_attachment=True)
        else:
            return abort(401)
    else:
        code = "-1"
        msg = "您当前不处于登录状态，请先登录"
    return jsonify(code=code, msg=msg)


""""
请求响应时间很长会导致超时
1.首次采用请求后端，后端根据url hash为一个值作为任务id，存在session中，id值返回给前端。
2.前端异步轮询另一个接口判断任务后端id是否完成，如果后端任务id完成，session['hash的id']==True；
3.然后前端在执行下载文件
"""


@app.route('/it_spider', methods=['POST'])
def itSpiderID():
    """ 根据url hash为一个值作为任务id，存在session中，id值返回给前端。同时开个线程去爬取。

    :return: json结果
    """
    username = request.form.get('username')
    it_url = request.form.get('spiderurl', type=str, default='')
    # 是否处于登录状态
    if session.get('username') == username and session.get('isLogin'):
        # 　判断是否是super权限以及被人为锁定状态
        result = DB_Sync.query_redis(username)
        userlock = result['data']['USER_LOCK']
        if userlock == 0:
            # 给出用户的文件夹路径，用来保存爬取后的txt
            user_spider_path = User_Action.user_rootFile_dir + \
                r'\{0}'.format(username)
            # 生成任务id
            task_id = computePW(it_url, '')
            task_id = task_id[:17]
            session['task_id'] = task_id    # 任务id存到session里面
            # 创建线程去爬取而不阻塞当前执行
            try:
                threadWorker(handleITSpider, username=username,
                             url=it_url, path=user_spider_path)
            except Exception as e:
                logger.error('%s用户启动threadWorker失败,原因是%s' % (username, e))
            code = "0"
            msg = "已收到爬取请求"
            data = task_id
            return jsonify(code=code, msg=msg, data=data)
        else:
            return abort(401)
    else:
        code = "-1"
        msg = "您当前不处于登录状态，请先登录"
        return jsonify(code=code, msg=msg)


# 这里添加Module中的核心业务ITSpider.py
def handleITSpider(username: str, url: str, path: str):
    """ 核心业务ITSpider.py爬取，通过全局函数来保存爬取的状态,解决函数无法操作sessio的问题

    :param username: 执行操作的用户名
    :param url: 需要爬取的网址
    :param path: 用户文件夹下的绝对路径，保存爬取过的文件txt
    :return: 没有return(在ThreadWorker里面，return没有意义)
    """
    myfilename = ""
    try:
        myfilename = runSpider(url, path)
    except Exception as e:
        logger.error('%s用户爬取%s过程出错，原因是%s' % (username, url, e))
    if myfilename:
        # 全局变量解决任务完成后，函数无法操作session的问题
        global spider_file_status
        spider_file_status = True
        global spider_file_name
        spider_file_name = myfilename
        logger.info('%s用户请求爬取%s成功' % (username, url))
    else:
        logger.info('%s用户请求爬取%s失败' % (username, url))


@app.route('/spider_status', methods=['GET'])
def spiderStatus():
    """ 根据任务id检查爬取任务是否完成,完成返回文件名

    :return: json结果
    """
    task_id = request.args.get('task_id')
    global spider_file_status
    global spider_file_name
    # 数据爬取完毕，准备好了
    if session.get('task_id') == task_id and spider_file_status and spider_file_name != "":
        # 这次请求成功，状态改为False。为了下次使用
        spider_file_status = False
        # 任务完成清除task_id
        session.pop("task_id")
        return jsonify(code="0", msg="爬取完毕，下载或查看文件列表", data=spider_file_name)
    # 数据未准备好
    else:
        return jsonify(code="-1", msg="数据未准备好，请稍等")


# 初始运行时候调用
# User_Action.create_user_rootdir()
# timed_task()
if __name__ == "__main__":
    User_Action.create_user_rootdir()
    timed_task()
    app.run(host='127.0.0.1', port=9999, debug=False, threaded=True)
