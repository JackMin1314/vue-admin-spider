"""
@FileName   : errlogs.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: log日志用于保存用户注册、修改密码、执行其他操作等异常错误和系统错误记录
@Time       : 2020/1/31 16:58
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
import logging
from Common.common import createDirFile
from Config.config import db_backup_dir, LOG_FORMAT, DATE_FORMAT, serverlogs_name

backup_path = ""


def initLogging():
    my_logger = logging.getLogger("jackmin")
    my_logger.setLevel(logging.DEBUG)  # 设置logger日志等级
    is_exists, filepath = createDirFile(db_backup_dir)
    global backup_path
    backup_path = filepath + r'\{}'.format(serverlogs_name)
    if not my_logger.handlers:
        # 创建handler(file,command)
        fh = logging.FileHandler(
            filepath + r'\{}'.format(serverlogs_name), encoding="utf-8")
        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT
        )
        # 为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 为logger添加的日志处理器
        my_logger.addHandler(fh)
        my_logger.addHandler(ch)
    return my_logger


def cleanLogging():
    """
    清除服务端的errlogs.txt（filename）日志内容
    :return: bool
    """
    try:
        with open(file=backup_path, mode="w+", encoding="utf-8") as f:
            f.truncate()    # 清空文件
        return True
    except Exception as e:
        with open(file=backup_path, mode="w+", encoding="utf-8") as f:
            f.write("尝试清空文件错误,原因是:%s" % e)
        return False


logger = initLogging()

if __name__ == '__main__':
    cleanLogging()
