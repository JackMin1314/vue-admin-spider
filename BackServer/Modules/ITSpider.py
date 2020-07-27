"""
@FileName   : ITSpider.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: IT之家的评论爬虫核心功能。(因为该内容编写时间是19年的直接搬运了，当时编码水平有限，整体代码编写风格很差，望见谅)
@Time       : 2020/1/3 0:00
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""


import requests
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re


it_save_name = ""
def it_urlneat(url):
    url= url
    if(url[8]=='m'):        # 解决手机it之家链接问题
        id=url[url.find('/html')+6:-4]
        url1=id[0:3]
        url2=id[3:]
        url='https://www.ithome.com/0/{}/{}.htm'.format(url1, url2)
    else:
        url=url
    commentlist.append(url)
    return url

def it_details(url):
    user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]
    ua = random.choice(user_agent_list)    # 随机从代理池选择
    headers = {'User-agent': ua}        # 构造headers,代理
    result = requests.post(url=url, headers=headers)
    # 添加为了构造文件名字
    str_result = (result.content).decode(encoding='raw_unicode_escape')
    my_re = re.compile(r"<title>.*</title>")
    re_result = (my_re.findall(str_result)[0])[7:-8]
    title_str = (re_result.encode('raw_unicode_escape')).decode(encoding='utf-8')
    print('标题名字为:', title_str)
    global it_save_name
    it_save_name = title_str[:20] + '.txt'
    it_save_name = re.sub(r"""[\\/:*?"<>#|]""", '', it_save_name)
    print('保存文件名为:', it_save_name)
    result_str = str(result.content)  # 直接强制类型转换为str，方便提取
    # comment_num = result_str[result_str.find('iframe align="middle" data=') + 28:result_str.find('datalapin ="0" scrolling="no"') - 2]
    index_start = result_str.find('align="middle" data=')
    index_end = result_str.find('datalapin') - 2
    comment_num = result_str[index_start+21:index_end]
    # print("ooops!! comment_num:", comment_num)
    cookies = str(result.cookies)  # 当使用post方法的时候cookies才能获得，改个headers就行
    asp_net_sessionid = cookies[cookies.find('ASP.NET_SessionId='):cookies.find(' for')]
    # BEC = cookies[cookies.find('BEC='):cookies.find('/>]') - 19] # 2020改版后不使用了
    cookies += asp_net_sessionid + '; '  # 这里的cookies必须要严格构造,2020改版后 cookies变化了
    timestamp = time.time()
    cookies += 'UM_distinctid=16cc5185ba783b-013f12b49e6d6b-7373e61-144000-16cc5185ba8489; '
    cookies += 'Hm_lvt_cfebe79b2c367c4b89b285f412bf9867={0}; '.format(int(timestamp))
    cookies += 'fullsrcmodal=true; '
    cookies += 'Hm_lvt_f2d5cbe611513efcf95b7f62b934c619={0}; '.format(int(timestamp+12))
    cookies += 'Hm_lpvt_f2d5cbe611513efcf95b7f62b934c619={0}; '.format(int(timestamp+429))
    cookies += 'Hm_lpvt_cfebe79b2c367c4b89b285f412bf9867={0}; '.format(int(timestamp+429))

    return headers, comment_num, cookies

def crazy_spider(news_id,ajax_url,headers,myhash,page):
    ajax_data = {
        'newsID': news_id,
        'hash': myhash,  #
        'type': 'commentpage',
        'page': page,  #
        'order': 'false'
    }
    ajax_result = requests.post(url=ajax_url, headers=headers, data=ajax_data)
    print("当前链接状态：{}".format(ajax_result.status_code))
    soup = BeautifulSoup(ajax_result.content, 'html.parser')  # xpath拿不到数据？因为返回的格式是json！(ajax不能使用xpath直接拿标签)
    li_list = soup.find_all('li', class_='entry')
    # print(len(li_list))   查看目前it_home评论一页50个
    # response.text用json.loads()格式化，并取出html，最后再用BeautifulSoup()格式化一下，评论的各个数据就很容易取出来
    if len(ajax_result.content)==0:
        print('评论已经爬完！')
        return 2
    for li in li_list:
       # 分析html源码，取出热评对应数据
       # item['用户名'] = li.find('span', class_='nick').text
       # item['时间'] = li.find('span', class_='posandtime').text.split('\xa0')[1]
        item['评论'] = li.find('p').text
        mystr = li.find('p').text
        flag = 1
        for i in hideword:
            if mystr.find(i) != -1 or len(mystr)>80:     #   长度？
                flag = 0
                print("【过滤关键字为：%s】" % i)
                break
            else:
                flag = 1
                continue
        if flag == 1:
            print(mystr)
            commentlist.append(mystr)


def it_save(commentlist, save_file_path):
    with open(file=save_file_path + r'\{}'.format(it_save_name), mode="w", encoding='utf-8') as f:
        for line in commentlist:
            f.write(line + '\n')


def ctl_spider(page_start,url,cookies,comment_url,ajax_url, headers):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]
    ua = random.choice(user_agent_list)  # 随机从代理池选择
    news_id = url[24:-4].replace('/', '')  # 从url构造获取NewsId
    timestamp = time.time()
    comment_data = {
        ':authority':'dyn.ithome.com',
        ':method': 'GET',
        ':path': '/comment/{}'.format(comment_url[31:]),
        ':scheme': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': ua,
        'Cookie': 'UM_distinctid=16cc5185ba783b-013f12b49e6d6b-7373e61-144000-16cc5185ba8489; '+ 'Hm_lvt_cfebe79b2c367c4b89b285f412bf9867={0}; '.format(int(timestamp)) + 'Hm_lvt_f2d5cbe611513efcf95b7f62b934c619={0}; '.format(int(timestamp+3)),
        # 'ASP.NET_SessionId=shkniyq40o5h45rvvwd1vnqt; BEC=228f7aa5e3abfee5d059195ad34b4137|1556702302|1556702302',#直接添加也可以
        'Host': 'dyn.ithome.com',
        #'Referer': url,
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': 1,
        'Connection': 'keep-alive',
        #'origin': 'https://dyn.ithome.com',
        'sec-fetch-site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }  # 构造comment_data

    # 获取评论页面的hash参数
    TIME_TIMEOUT = 10
    # 创建chrome启动选项
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.set_headless()
    chrome_options.add_argument('--user-agent=%s' % ua)
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    # 关闭提示（浏览器正在被自动化程序控制）但是会有提示框
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 指定chrome启动类型为headless 并且禁用gpu（无启动页面）
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 调用环境变量指定的chrome浏览器创建浏览器对象
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(comment_url)
    # 微博通过navigator判断是否selenium，这里设置很重要！！！
    driver.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
    # pagetype = driver.find_element_by_xpath(" /html/body/div[@class='post_comment']/div[@class='comm_list']/div[@id='divLatest']/script") # /html/body/div[@class='post_comment']/div[@class='comm_list']/div[@id='divLatest']
    # print(pagetype.text)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # pagetype = soup.text
    # pagetype = pagetype[pagetype.find('var pagetype = \'') + 16:pagetype.find('lhcl(1)') - 2]
    pagetype_all = soup.find('div', id="divLatest")
    pagetype = pagetype_all.contents[-1]
    # print("hi, pagetype:", pagetype)
    pagetype = str(pagetype)
    pagetype = pagetype[24:-11]
    # print("need myhash:", pagetype)
    myhash = pagetype
    time.sleep(1)
    driver.close()
    driver.quit()

    t = 0
    for page in range(page_start, page_start + 4):
        # 这里可以控制爬多少。js前端用字符串？
        try:
            t1 = crazy_spider(news_id, ajax_url, headers, myhash, page)  # myhash 这里进行了网页改版 2020/1/1;hash在评论页面的script标签里面
            if (t1 == 2):
                t = 2
        except:
            print("Post请求失败！")
            t = t + 1
        if (t == 2):  # 超时结束或者评论爬取完毕
            break
        time.sleep(random.randint(3, 5))  # 控制爬取间隔时间，反爬


# 下面注释不要删除！这里跟__name__=='__main__'内容一致，本程序单独运行时不用考虑main，作为模块被别人使用时，main内部内容不被执行
hideword = ['it', '王跃', '爱否', '今晚', '封面', 'htm', '赌', '篇', '图片', '第五', '第四', '嫖娼', '单位', '强奸', '起诉',
                '律师', '@', '没人', '信用卡', '股市', '川普', '赌博', '花呗', '套现', '贷款', '税', '青岛', '小便', '贪腐', '上访',
                '贪污', '腐败', '不公平', 'IT', '玄隐', '“', '第一', '第二', '第三', '”', '政府', '特朗普', '上车', '股票', '沙发',
                '马云', '资源', '楼', '铺路', '刺客', '实习', '评论', '热评', '尾巴', '微博', '之家', '小编', '水', '文章', '新闻', '编辑',
                '标题', '价值', '家友', '权利', '权力', '剥削', 'www', '圈子', "打工嫌累"]  # 添加过滤关键字例如：hideword = ["傻逼", "sb", "儿子"]
item = {}
commentlist = []
page_start = 1
url = "https://m.ithome.com/html/476121.htm"  #   能找到 iframe align="middle" data=； 324f9add8e997e46，但是#document（包括评论页面参数，hash）以及评论链接不在返回数据里
# url=it_urlneat(url)       # 被别的模块runSpider导入的时候再调用
news_id = url[24:-4].replace('/', '')  # 从url构造获取NewsId
# headers, comment_num, cookies = it_details(url)
# comment_url = 'https://dyn.ithome.com/comment/{}'.format(comment_num) # 构造评论页面comment_url 得到cookies，headers访问数据页面,获取hash，
ajax_url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'  # 根据对应url获取newsID，再将newsID和type数据post给接口（该url）获取返回的热评数据
# ctl_spider(page_start, url, cookies, comment_url, ajax_url, headers)
# it_save(commentlist)
