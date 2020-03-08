"""
@FileName   : encryp.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 加密解密算法
@Time       : 2020/1/29 12:13
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
# !coding=utf-8
from hashlib import md5 as MD5
from os import urandom

def computePW(text: str, salt: str):
    """根据用户密码和数据库中的salt来计算返回md5的16进制值字符串

    :param text: 前端传来用户的密码(字符串)
    :param salt: 本地数据库存加密的盐(字符串)
    :return: 长md5后的32位16进制值字符串
    """
    # text = text.encode('utf-8')
    # s = text + salt
    # m = MD5(s)
    # return m.hexdigest().encode('utf-8')

    s = text + salt     # 不要调换位置，否则会导致hash结果不一致
    m = MD5(s.encode('utf-8'))  # 等效MD5(text.encode('utf-8') + salt.encode('utf-8'))
    return m.hexdigest()


def checkPW(md5str: str, USER_PASSWD: str):
    """检查本地数据库中密码和计算后的密码是否一致

    :param md5str: 计算后的密码(字符串)
    :param USER_PASSWD: 本地的存的密码(字符串)
    :return: bool
    """
    return md5str == USER_PASSWD


def create_Salt():
    """用于注册时候用户加密密码的盐

    :return: str
    """
    # return urandom(32).hex().encode('utf-8')
    return urandom(32).hex()


# print(urandom(32))
# print(urandom(32).hex())
# print(type(urandom(32)),"22222",type(urandom(32).hex()))
# print(os.urandom(32).hex())
#print(computePW("78788", b"5c7ea7a049790abf5acb05f51079bb3b0f97f28ffb4f3f886213392a66ce3010"))
# print(checkPW(computePW("12345",b"727dddd88ba58cb158941f5ab619da1596914eaf4504daa944196a3f19df6f51"),b"da68b52441df4e4d9ac33d9227f908c1"))
# print(computePW('https://www.ithome.com/0/476/120.htm',''))