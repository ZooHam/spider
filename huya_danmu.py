#!/usr/bin/env python3
# coding=utf-8
# author:sakuyo
# ----------------------------------

import csv, time, sys, signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Huya(object):
    def SaveToCSV(self, fileName, headers, contents):
        titles = headers
        data = contents
        # csv用utf-8-sig来保存
        with open(fileName + '.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=titles)
            writer.writeheader()
            writer.writerows(data)
            print('写入完成！')


class HuyaLive(Huya):

    def __init__(self, target):  # 初始化 输入值target为直播间ID
        self.target = target
        self.barrageList = {}

    def Connect(self):  # 连接直播间
        chrome_options = Options()
        # 使用headless无界面浏览器模式
        chrome_options.add_argument('--headless')  # 增加无界面选项
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        url = 'https://www.huya.com/' + self.target
        driver.get(url)
        time.sleep(5)

        while True:  # 无限循环，伪监听
            time.sleep(1)  # 等待1秒加载
            chatRoomList = driver.find_element("chat-room__list")
            chatMsgs = chatRoomList.find_elements_by_class_name("J_msg")
            # 定位弹幕div，逐条解析
            for chatMsg in chatMsgs:
                try:
                    dataId = chatMsg.get_attribute('data-id')  # 每条弹幕都有独立data-id
                    content = {}  # 初始化弹幕内容字典
                    # 尝试是否为礼物弹幕
                    try:
                        hSend = chatMsg.find_element_by_class_name("tit-h-send")
                        content['username'] = hSend.find_elements_by_class_name("cont-item")[0].text
                        content['gift'] = hSend.find_element_by_class_name("send-gift").find_element_by_tag_name(
                            "img").get_attribute("alt")
                        content['num'] = hSend.find_elements_by_class_name("cont-item")[3].text
                    except:
                        pass
                    # 尝试是否为消息弹幕
                    try:
                        mSend = chatMsg.find_element_by_class_name("msg-normal")
                        content["username"] = mSend.find_element_by_class_name("J_userMenu").text
                        content["msg"] = mSend.find_element_by_class_name("msg").text
                    except:
                        pass
                    # 存入弹幕列表
                    self.SaveToBarrageList(dataId, content)

                except:
                    continue

    def SaveToBarrageList(self, dataId, content):  # 弹幕列表存储
        if dataId in self.barrageList or not content:  # 去重、去空
            pass
        else:
            content['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.barrageList[dataId] = content
            print(dataId, content)


def QuitAndSave(signum, frame):  # 监听退出信号
    print('catched singal: %d' % signum)
    hyObj.SaveToCSV('test', ['username', 'time', 'msg', 'gift', 'num'], hyObj.barrageList.values())
    sys.exit(0)


if __name__ == '__main__':  # 执行层
    # 信号监听
    signal.signal(signal.SIGTERM, QuitAndSave)
    signal.signal(signal.SIGINT, QuitAndSave)

    hyObj = HuyaLive('52724')
    hyObj.Connect()

