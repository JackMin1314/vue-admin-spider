"""
@FileName   : timed_db_backup.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 用于mysql数据库的定时备份到磁盘上的功能
@Time       : 2020/2/3 17:09
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib

# 导入定时任务模块的库
from apscheduler.schedulers.background import BackgroundScheduler

# 导入配置文件
from Config.config import year, month, week, day_of_week, hour, minute, second
from Config.config import mysql_base, mysql_table, mysql_passwd, db_backup_dir

# 导入创建文件夹模块
from Common.common import createDirFile, getlocaltime
# 导入pymysql
import pymysql
# 导入excel处理
import xlwt


def fetchDB():
    """查询mysql所有数据并返回

    :return: 返回数据库表的结果
    """
    db = pymysql.Connect("localhost", "root", mysql_passwd,
                         mysql_base, charset='utf8')
    # cursor 默认返回的结果是元组，可以指定返回list，里面是字典格式
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM {}".format(mysql_table)
    try:
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
    except:
        print("{} 备份数据库错误...", getlocaltime().decode('utf-8'))
        db.rollback()
    db.close()
    print(type(result), result)
    return result


# 自己封装了下样式，可依据需要添加修改
def initStyle(bound: bool, colour_index: int, height: int, borders: int, pattern: int, pattern_fore_colour: int):
    """根据参数设置单元格格式样式

    :param bound: 是否加粗
    :param colour_index: 字体颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow...
    :param height: 字体大小20为衡量单位20 * xx
    :param borders: 细实线-1，小粗实线-2，细虚线-3，中细虚线-4，大粗实线-5，双线-6，细点虚线-7, 大粗虚线-8，细点划线-9，粗点划线-10，细双点划线-11，粗双点划线-12，斜点划线-13...
    :param pattern: 是否设置背景色等NO_PATTERN, SOLID_PATTERN...
    :param pattern_fore_colour: 背景色颜色
    :return: 具有以上style属性的实例
    """
    # 设置excel单元格样式
    style = xlwt.XFStyle()
    style.font.bold = bound
    style.font.colour_index = colour_index  # red
    style.font.height = height  # 字体大小，12为字号，20为衡量单位
    # style.alignment.horz = style.alignment.HORZ_CENTER
    style.alignment.horz = style.alignment.HORZ_CENTER
    style.alignment.vert = style.alignment.VERT_CENTER
    style.alignment.wrap = 1  # 设置自动换行
    # 粗细实虚线
    style.borders.left = borders
    style.borders.top = borders
    style.borders.right = borders
    style.borders.bottom = borders
    # 设置颜色
    style.pattern.pattern = pattern
    style.pattern.pattern_fore_colour = pattern_fore_colour    # 22-gray
    return style


def writeExcel(result: list, backup_path: str):
    """写入数据到excel表格里面

    :param result: 从数据库取的数据
    :param backup_path: 需要备份的数据路径
    :return:
    """

    # 创建一个 workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个 worksheet, 添加名字
    worksheet = workbook.add_sheet('Mysql_Backup')
    # 创建style实例
    style = initStyle(True, 2, 20 * 12, 2, xlwt.Pattern.SOLID_PATTERN, 5)
    # 添加表格的字段名
    column_number = (len(result[0]) if result else 0)
    # 合并单元格并写入数据第一行日期名称
    worksheet.write_merge(0, 1, 0, column_number-1, getlocaltime().decode(
        'utf-8') + " -- 数据备份", style)  # 第多少行合并几行，第多少列合并几列，写入数据数据，用什么样式
    # 设置行高
    tall_style = xlwt.easyxf('font:height 320')
    # 数据库字段长度适配
    worksheet.col(0).width = 256 * 30  # 适配USER_TYPE
    worksheet.col(1).width = 256 * 30  # 适配USER_LOCK
    worksheet.col(2).width = 256*30     # 适配USER_NAME
    worksheet.col(3).width = 256*40     # 适配USER_PASSWD
    worksheet.col(4).width = 256*80     # 适配USER_SALT
    worksheet.col(5).width = 256*30     # 适配USER_MAIL
    worksheet.col(6).width = 256*30     # 适配SUBBMISSION_DATE
    # 写入数据库表的字段名
    if column_number > 0:
        i = 0
        style2 = initStyle(True, 0, 20 * 12, 1, xlwt.Pattern.NO_PATTERN, 5)
        worksheet.row(2).set_style(tall_style)
        for name in (result[0]).keys():
            worksheet.write(2,  i, name, style2)
            i += 1
    else:
        print("数据库表格为空")

    style3 = initStyle(False, 0, 20 * 12, 1, xlwt.Pattern.NO_PATTERN, 5)
    i = 3
    for user in result:
        j = 0
        for k, v in user.items():
            print('{0} --> {1}'.format(k, v))
            if j < 7:
                worksheet.write(i, j, v, style3)
                print("this", i, j, v)
                j += 1
        i += 1

    # r表示忽略转义字符,使用decode是因为返回的是byte要转为str
    workbook.save(
        backup_path + r'\db_Excel_{}.xls'.format((getlocaltime().decode('utf-8'))[:-9]))


def importExcel():
    """查询数据保存到excel

    :return:
    """
    is_exist, backup_path = createDirFile(db_backup_dir)
    # 如果创建成功
    if is_exist:
        # 查询数据库的数据
        result = fetchDB()
        if len(result) == 0:
            print("没有数据,不保存")
            flag = True
        # 有数据导入到excel里面(应为加密采用的是单向门限函数,即便是存储了本地的数据库密码和盐，也很难反解用户的密码;所以即便是统计目的也是可以全部获取信息的)
        else:
            try:
                writeExcel(result, backup_path)
                flag = True
            except:
                print("导入数据到Excel失败")
                flag = False

    # 如果创建失败
    else:
        print("创建文件路径错误...")
        flag = False
    return flag


def myjob():
    print('time: %s start to backup DataBase' % getlocaltime().decode('utf-8'))
    importExcel()


def timed_task():
    scheduler = BackgroundScheduler()
    # cron表达式定时执行
    scheduler.add_job(myjob, 'cron', year=year, month=month, week=week,
                      day_of_week=day_of_week, hour=hour, minute=minute, second=second)
    # 该部分调度是一个独立的线程

    try:
        scheduler.start()
    except(KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    # timed_task()
    myjob()
    # scheduler = BackgroundScheduler()
    # # 每隔5秒执行一次
    # scheduler.add_job(myjob, 'interval', seconds=5)
    # # 该部分调度是一个独立的线程
    # scheduler.start()
    # scheduler.shutdown()
