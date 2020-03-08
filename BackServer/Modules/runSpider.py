"""
@FileName   : runSpider.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 调用ITSpider.py
@Time       : 5/03/2020 2:46 pm
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
from Modules import ITSpider as it_home


def runSpider(it_url: str, save_file_path: str):
    """ 根据it之家的url爬取评论，在指定的路径下生成的文件，返回文件名

    :param it_url: 爬取的url
    :param save_file_path: 保存文件的具体路径
    :return: str
    """

    # 评论中需要过滤的关键字
    it_home.hideword = ['下体', '云盘', '网盘', 'it', '王跃', '爱否', '今晚', '封面', 'htm', '赌', '篇', '图片', '第五', '第四', '嫖娼',
                        '单位', '强奸', '起诉', '律师', '@', '没人', '信用卡', '股市', '川普', '赌博', '花呗', '套现', '贷款', '税', '青岛', '小便',
                        '贪腐', '上访',
                        '贪污', '腐败', '不公平', 'IT', '玄隐', '“', '第一', '第二', '第三', '”', '政府', '特朗普', '上车', '股票', '沙发',
                        '马云', '资源', '楼', '铺路', '刺客', '实习', '评论', '热评', '尾巴', '微博', '之家', '小编', '水', '文章', '新闻',
                        '编辑', '标题', '价值', '家友', '权利', '权力', '剥削', 'www', '圈子', "打工嫌累"]  # 添加过滤评论关键字

    it_home.item = {}
    it_home.commentlist = []
    it_home.page_start = 1
    # 【手机分享要爬取的某个热点话题链接】https://m.ithome.com/html/419302.htm
    it_home.url = it_url
    # 格式化url
    it_home.url = it_home.it_urlneat(it_home.url)
    # 从url构造获取NewsId
    it_home.news_id = it_home.url[24:-4].replace('/', '')
    # 获取相关参数
    it_home.headers, it_home.comment_num, it_home.cookies = it_home.it_details(
        it_home.url)
    # 构造评论页面comment_url 得到cookies，headers访问数据页面,获取hash
    it_home.comment_url = 'https://dyn.ithome.com/comment/{}'.format(
        it_home.comment_num)
    # 根据对应url获取newsID，再将newsID和type数据post给接口（该url）获取返回的热评数据
    it_home.ajax_url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'
    # 爬取的控制函数
    it_home.ctl_spider(it_home.page_start, it_home.url, it_home.cookies,
                       it_home.comment_url, it_home.ajax_url, it_home.headers)
    # 爬取结束文件保存函数
    it_home.it_save(it_home.commentlist, save_file_path)
    return it_home.it_save_name
