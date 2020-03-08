"""
@FileName   : Config.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 相关配置文件数据库和后端session、密钥、email设置等
@Time       : 2020/1/28 18:37
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
from datetime import timedelta
"""
global mysql and redis Config
mysql,redis密码部分请按照实际修改
如果修改了MySQL默认库表部分，请同时修改目录config/Mysql_Init_Script.sql
先修改内容
然后 mysql -u root -p 输入密码
最后 source  /绝对路径下的/Mysql_Init_Script.sql
"""
# MySQL数据库名称
mysql_base = 'spider'
# MySQL数据库中表名称
mysql_table = 'userinfo'
# MySQL数据库root对应的密码
mysql_passwd = '5201020116'
# Redis数据库对应的密码
redis_passwd = '5201020116'

# session 生存时间
session_lifeTime = timedelta(days=3)
# cookie 生存时间(秒)
max_ageTime = 60*60*6    # 6hour
# 生成token的密钥,修改下面的值会导致之前的token不能使用
my_secretKey = "9fw65ge2rg121*#!!"

# email验证码相关配置
# 邮箱服务器地址
MAIL_SERVER = "smtp.qq.com"
# QQ mail支持SSL（port：465）和TLS（port：587）方式对应端口不一样，邮箱不支持非加密方式发送邮件
MAIL_PORT = 587
MAIL_USE_TLS = True
# 发送邮件，True为不发送
MAIL_SUPPRESS_SEND = False
# 发送方
MAIL_USERNAME = "1416825008@qq.com"
# 个人的授权码，可通过开启QQmail的POP3/SMTP服务 获得
MAIL_PASSWORD = "****开通后才可以使用邮件发送****"
# 默认的发送者
MAIL_DEFAULT_SENDER = "1416825008@qq.com"
# 设置redis保存最大email code保存时间10分钟
max_EmailCodeTime = 60*10

# cron定时任务配置
year = "*"
month = "*"
week = "*"
day_of_week = "*"   # "wed,sun"
hour = "14"
minute = "13"
second = "5"

# 配置保存mysql数据库的文件、日志文件、用户文件的根目录
db_backup_dir = 'folders'

# 保存用户产生的文件的主文件夹名
user_backup_dir = 'userfiles'

# errlog日志记录配置
# 配置输出日志格式
LOG_FORMAT = "%(asctime)s %(levelname)s %(funcName)s() ==> %(message)s "
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '      # 配置输出时间的格式，
serverlogs_name = 'errlogs.txt'
