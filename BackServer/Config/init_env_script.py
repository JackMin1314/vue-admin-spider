"""
@FileName   : init_env_script.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 主要是用来初始化运行BackServer的环境以及对python进行换源
@Time       : 2020/2/8 12:48
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
import os


# 第一步先给python全局换源
def sourceChanging():
    # 需要换源的配置文件pip.ini
    text = '''[global]\nindex-url = http://pypi.douban.com/simple/\ntimeout = 6000\ntrusted-host = pypi.douban.com'''
    # 先获取系统的用户路径
    username = os.environ['USERNAME']
    print(username)
    createdir = os.environ["USERPROFILE"] + r"\pip"
    if not os.path.exists(createdir):
        print('folder name "pip" is not existed,so make it... ')
        os.makedirs(createdir, mode=0o777, exist_ok=True)
        print('create pip.ini file...')
        with open(createdir + r'\pip.ini', mode='w', encoding='utf-8') as f:
            f.write(text)
        print("python换源结束...")
    else:
        print(' folder name "pip" is existed')
        if os.path.exists(createdir + r'\pip.ini'):
            print("%s目录下'pip.ini'文件已经存在,python换源结束" % createdir)
        else:
            print("pip.ini文件不存在，开始创建")
            with open(createdir + r'\pip.ini', mode='w', encoding='utf-8') as f:
                f.write(text)
            print("python换源结束...")

    # 下面代码是用来获取并保存环境变量的,存之以学
    # with open('path_backup.txt', mode='w', encoding='utf-8') as f:
    #     for k, v in os.environ.items():
    #         print(k + '>>>' + v)
    #         f.write(k + ">>>>" + v + "\n")


# 第二步下载相关环境需要的第三方库
def download_pkg():
    """第二步下载相关环境需要的第三方库

    :return: bool
    """
    print("正在下载安装必要的第三方库文件...")
    try:
        # 如果需要使用IT之家爬虫还需要下载selenium、BeautifulSoup4、requests。可添加到后面
        os.system('pip install flask flask_cors flask_wtf flask_mail pymysql redis apscheduler xlwt psutil ')
        print("安装成功...")
        flag = True
    except Exception as e:
        print("下载安装失败...原因是:%s" % e)
        flag = False
    return flag


# init_env_script初始化函数
def init_env_script():
    sourceChanging()
    if download_pkg():
        print("所有环境配置完毕，程序退出...")
    else:
        print("配置环境过程出错，请检查，程序退出...")


if __name__ == '__main__':
    init_env_script()

