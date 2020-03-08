"""
@FileName   : common.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 一些常用的功能和模块获取时间和生成验证码等
@Time       : 2020/1/29 15:13
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
import time
from random import choice
from pathlib import Path
import psutil
from threading import Thread


def getlocaltime():
    """格式化当前时间

    :return: 字符串格式的当前调用时间
    """
    datetime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())).encode("utf-8")
    return datetime


def getCapture():
    """生成邮箱验证码,默认8位

    :return: 邮箱验证码
    """
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    CaptureCode = ""
    for i in range(8):
        CaptureCode += choice(numbers)
    return CaptureCode


def createDirFile(dirname: str):
    """ 在当前项目路径下创建指定文件夹 eg : .../BackServer/folders

    :param dirname: 需要创建的文件夹名称
    :return: bool,文件夹的绝对路径
    """
    # path :["/","bs/","bs/Common","bs/Common/dir/","bs/folders"]
    testmypath = Path.cwd()     # 获取程序运行的当前路径
    # print("当前的程序运行路径为:", testmypath)
    tuplepath = testmypath.parts
    tuplelen = len(tuplepath)

    # 只要程序的运行路径（当前文件单独运行或被调用运行）包含BackServer即可
    # 在"BackServer/"目录下创建文件夹/dirname = > xxx/BackServer/dirname/
    if "BackServer" in tuplepath:
        index = tuplepath.index("BackServer")
        print("BackServer exists, index is %s" % index)
        if index == tuplelen-1:
            # print('当前处于指定路径下')
            backup_path = Path.cwd() / dirname
            backup_path.mkdir(mode=0o777, parents=False, exist_ok=True)
            # print("指定路径下创建成功...", backup_path)
            flag = True
        else:
            p = Path('../'*(tuplelen - index-1))
            p = p / dirname
            backup_path = p.resolve()
            backup_path.mkdir(mode=0o777, parents=False, exist_ok=True)
            # print('返回指定路径,创建成功...', p.resolve())
            flag = True
    # 程序路径不包含BackServer，不能在BackServer下创建文件夹
    else:
        flag = False
        print("当前程序运行路径不在指定路径中...")
        backup_path = ""
    return flag, str(backup_path)


def getMachineInfo():
    """
    利用psutil跨平台获取系统的内存、CPU、网络速率信息
    :return:
    """
    M = 1024 * 1024
    G = M * 1024

    mem = psutil.virtual_memory()
    # print("---------Memory Info--------")
    # # print('系统内存：', mem)
    # print('所有内存：%dM %fG' % (mem.total // M, mem.total / G))
    # print('空闲内存：%dM %fG' % (mem.available // M, mem.available / G))
    # print('使用内存：%dM %fG' % (mem.used // M, mem.used / G))
    # print('内存使用率：%.2f%%' % mem.percent)
    # print("---------CPU Info--------")
    # print("CPU使用率: %.3f%%" % psutil.cpu_percent(interval=1))
    # print("CPU线程数 %d" % psutil.cpu_count())
    # print("CPU核数 %d" % psutil.cpu_count(logical=False))
    n = psutil.net_io_counters()
    s1 = n.bytes_sent  # 发送字节数
    s2 = n.bytes_recv  # 接受字节数
    time.sleep(1)
    n2 = psutil.net_io_counters()
    s1 = round((n2.bytes_sent - s1) / 1024, 2)
    s2 = round((n2.bytes_recv - s2) / 1024, 2)
    # print("up:%skb/s down:%skb/s" % (s1, s2))
    timestr = time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年',m='月',d='日',h='时',f='分',s='秒')
    machine_info_list = [
        {'key': "CPU核数", 'value': "%d" % psutil.cpu_count(
            logical=False), 'timestr': timestr},
        {'key': "CPU线程数", 'value': "%d" % psutil.cpu_count(), 'timestr': timestr},
        {'key': "所有内存", 'value': '%dM|%.2fG' % (
            mem.total // M, mem.total / G), 'timestr': timestr},
        {'key': '已用内存', 'value': '%dM|%.2fG' % (
            mem.used // M, mem.used / G), 'timestr': timestr},
        {'key': '空闲内存', 'value': '%dM|%.2fG' % (
            mem.available // M, mem.available / G), 'timestr': timestr},
        {'key': '内存使用率', 'value': '%.2f%%' % mem.percent, 'timestr': timestr},
        {'key': 'CPU使用率', 'value': '%.3f%%' % psutil.cpu_percent(
            interval=1), 'timestr': timestr},
        {'key': "瞬时速率上", 'value': "%skb/s" % s1, 'timestr': timestr},
        {'key': "瞬时速率下", 'value': "%skb/s" % s2, 'timestr': timestr}
    ]

    # print(time.strftime("%Y年%m月%d日 %a %H:%M:%S", time.localtime(time.time())))
    return machine_info_list


def threadWorker(funcname, **args):
    """ 开一个线程去完成耗时函数.args参数对要和funcname对应

    :param funcname: 需要执行的函数名
    :param kwargs: 函数参数对
    """
    thread = Thread(target=funcname, kwargs=args)
    # .start()会安排对象在另外一个单独线程中运行run()方法,是异步执行。run()是普通的同步执行
    thread.start()
    # thread.run() # run方法会等funcname执行完再往下走
