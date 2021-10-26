# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import sqlite3  # 进行SQLite数据库操作

#影片详情链接的规则
findName = re.compile(r'<span>(.*)</span>')  #主播网名
findConcern = re.compile(r'<div class="_9035ad37393516563c608293fdc27a22-scss">(\d*)</div>') #关注数
findFans = re.compile(r'<div class="_9035ad37393516563c608293fdc27a22-scss">(.*)</div>') #粉丝数
findLikes = re.compile(r'<div class="_9035ad37393516563c608293fdc27a22-scss">(.*)</div>') #点赞数
findOpus = re.compile(r'<span class="_03811320ee25b81d1c705fae532572ec-scss">(\d*)</span>') #关注数

def main():
    baseurl = "https://www.douyin.com/user/MS4wLjABAAAAtv8dYBRv_whn9vGwiTCwGpXHQJauOrUPje0wXnIuELU?previous_page=app_code_link"  #要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)
    # 3.保存数据
    dbpath = "douyin.db" #当前目录新建数据库，存储进去
    saveData2DB(datalist,dbpath)
    askURL("https://www.douyin.com/user/MS4wLjABAAAAtv8dYBRv_whn9vGwiTCwGpXHQJauOrUPje0wXnIuELU?previous_page=app_code_link")


# 爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(0,1): #调用页面信息函数，1条，1次
        url=baseurl+str(i*1)
        html=askURL(url)  #保存获取的网页源码
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            data = []  # 保存主播所有信息
            item = str(item)
            #主播详情的链接
            data.append()#添加网名
            # concern=re.findall(findConcern,item)[0]
            # data.append(concern)#添加关注
            # fans=re.findall(findFans,item)[0]
            # data.append(fans)#添加粉丝数
            # likes=re.findall(findLikes,item)[0]
            # data.append(likes)#添加获赞数
            # opus=re.findall(findOpus,item)[0]
            # data.append(opus)#添加关注数
            # datalist.append(data)   #把处理好的电影信息放入datalist
    print(datalist)
    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


#保存数据到数据库
def saveData2DB(code,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in code:
            for index in range(len(data)):
                if index == 4 or index == 5:
                    continue
                data[index] = '"'+data[index]+'"'
            sql = '''
                    insert into douyin(
                    name,concern_list,fans_number,likes_number,opus_number)
                    values (%s)'''%",".join(data)
            cur.execute(sql)
            conn.commit()
    cur.close
    conn.close()


def init_db(dbpath):
    sql = '''
        create table douyin(
        id integer  primary  key autoincrement,
        name varchar ,
        concern_list numeric ,
        fans_number varchar,
        likes_number varchar ,
        opus_number varchar
        )


    '''  #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
    # init_db("douyin.db")
     print("爬取完毕！")


