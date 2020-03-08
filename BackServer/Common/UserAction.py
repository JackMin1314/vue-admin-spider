"""
@FileName   : UserAction.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 提供用户相关的文件操作功能。包括产生用户根目录、生成、删除用户文件夹等
@Time       : 2020/2/22 20:08
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
from pathlib import Path
import shutil
from Config.config import user_backup_dir, db_backup_dir
from Common.common import createDirFile
import time

user_rootFile_exists = False
user_rootFile_dir = ""


def create_user_rootdir():
    """ 创建用户文件夹根目录，里面保存各自用户的文件夹.(约定必须在db_backup_dir下)

    :return: bool, 文件夹的绝对路径
    """
    is_exists, backup_dir = createDirFile(db_backup_dir)
    # 如果本地已经存在了db_backup_dir文件夹
    if is_exists:
        # 可以指定路径去创建文件夹
        user_dir = backup_dir + r'\{0}'.format(user_backup_dir)
        Path(user_dir).mkdir(mode=0o777, parents=False, exist_ok=True)
        global user_rootFile_exists
        user_rootFile_exists = True
        global user_rootFile_dir
        user_rootFile_dir = user_dir
        return True, user_rootFile_dir
    else:
        user_rootFile_exists = False
        user_rootFile_dir = ""
        return False, ""


def create_user_homedir(username: str):
    """ 根据用户名创建用户文件夹,需要提前运行

    :param username: 用户名
    :return: bool, 文件夹的绝对路径
    """
    # 用户家文件夹已经创建
    global user_rootFile_exists
    if user_rootFile_exists:
        user_homedir = user_rootFile_dir + r'\{0}'.format(username)
        Path(user_homedir).mkdir(mode=0o777, parents=False, exist_ok=True)
        print("创建用户%s文件成功" % username)
        return True, user_homedir
    else:
        print("创建用户%s文件失败" % username)
        return False, ""


def query_user_file(username, filename):
    """ 根据用户名和文件名，查询本地是否有该文件,前提运行了create_user_homedir

    :param username: 需要查询的用户名
    :param filename: 该用户名下的需要查询的文件
    :return: bool, 用户文件夹的绝对路径(若需文件的绝对路径可以拼接即可)
    """

    print(username, filename)
    user_homedir = user_rootFile_dir + r'\{0}'.format(username)
    user_filedir = user_homedir + '\{0}'.format(filename)
    print(user_homedir, user_filedir)
    return Path(user_filedir).is_file(), user_homedir


def user_file_list(username: str):
    """ 根据用户名返回该用户下的所有文件名列表

    :param username:
    :return: list
    """
    user_homedir = user_rootFile_dir + r'\{0}'.format(username)
    # 根目录存在
    file_list = []
    if user_rootFile_exists:
        # 用户名目录存在
        file_list = fileList(user_homedir)
    return file_list


def user_file_info(username: str, filename: str):
    """ 根据用户名和其下的文件名返回文件的属性大小、创建日期

    :param username: 用户名
    :param filename: 用户名下的文件名
    :return: json格式
    """
    isexists, filepath = query_user_file(username, filename)
    K = 1024
    if isexists:
        fileinfo = Path(filepath+'/{0}'.format(filename)).stat()
        fileinfo_json = {
            'username': username,
            'filename': filename,
            'filesize': '%.2fKB' % (fileinfo.st_size / K),
            'maketime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileinfo.st_mtime))
        }
        return fileinfo_json
    else:
        print('%s user file %s not found' % (username, filename))
        return {}


def remove_user_homedir(username: str):
    """ 根据用户名，删除文件及其下所有文件夹、文件

    :param username: 需要删除文件夹或文件的用户名
    :return: bool
    """
    # 先判断文件夹是否存在
    try:
        user_homedir = user_rootFile_dir + r'\{0}'.format(username)
        if Path(user_homedir).is_dir():
            shutil.rmtree(user_homedir, ignore_errors=True)
            print("文件删除成功")
        else:
            print("文件不存在")
        return True
    except Exception as e:
        print("删除文件异常%s" % e)
        return False


def remove_user_file(username: str, filename: str):
    """ 根据用户和文件名删除用户目录下该文件

    :param username:
    :param filename:
    :return: bool
    """
    # 先判断文件是否存在
    try:
        is_exists, user_home_str = query_user_file(username, filename)
        if is_exists:
            file_path = user_home_str + r'\{0}'.format(filename)
            # unlink接受参数必须是Path类型的,不能是字符串
            Path.unlink(Path(file_path))
            return True
        else:
            return True
    except Exception as e:
        print("delete %s用户文件%s出错,因为:%s" % (username, filename, e))
        return False


# 为super写了函数(真的吐槽自己当时写代码时候没考虑太多，很多删除操作都是可以通用的。现在还得一个个写)
def fileList(pathstr):
    """ 根据文件夹路径，返回该目录下一级的所有文件

    :param pathstr: 文件夹路径
    :return: list
    """
    file_list = []
    if Path(pathstr).is_dir():
        file_list = [x.parts[-1]
                     for x in Path(pathstr).iterdir() if x.is_file()]
    return file_list


def fileListInfo(filepath: str, filename: str):
    """ 根据文件的路径和文件名，返回该文件的属性

    :param filepath: 文件路径
    :param filename: 文件名
    :return: json
    """
    K = 1024
    fileinfo = Path(filepath + '/{0}'.format(filename)).stat()
    fileinfo_json = {
        'filename': filename,
        'filesize': '%.2fKB' % (fileinfo.st_size / K),
        'maketime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileinfo.st_mtime))
    }
    return fileinfo_json


def fileDelete(filepath: str):
    """ 根据路径删除对应的文件,文件不存在，也默认是删除成功

    :return: bool
    """
    try:
        # 判断文件是否存在
        if Path(filepath).is_file():
            # unlink接受参数必须是Path类型的,不能是字符串
            Path.unlink(Path(filepath))
            return True
        else:
            return True
    except Exception as e:
        print("删除备份文件出错,因为:%s" % e)
        return False
