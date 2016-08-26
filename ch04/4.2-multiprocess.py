#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : Jan Yang
@software: PyCharm Community Edition
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import pymongo


client = pymongo.MongoClient('localhost', 27017)  # 连接Mongodb数据库
sense = client['sense']  # 创建数据库
url_list = sense['url_list']  # 创建数据表
item_info = sense['item_info']  # 同上




def get_city_num():
    # url = 'http://www.senseluxury.com/'
    # response = requests.get(url)
    with open('six.html') as f:
        response = f.read()

    soup = BeautifulSoup(response, 'lxml')
    # print soup
    citys = soup.select('#destination_nav > div > div > div > dl.dl-list > dt > a')
    # print citys
    print(len(citys))
    for city in citys:
        city = city.get_text()
        print city






def get_page_list(page):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  #
    url = 'http://www.senseluxury.com/destinations_list/85?page=%s' % page
    response = requests.get(url)  # 发送请求
    wb_data = json.loads(response.text[1:-1])  # 将JSON字符串转换为字典
    # print wb_data['val']

    # 循环获取键值数据
    for i in wb_data['val']['data']:
        title = i['title']
        url = 'http://www.senseluxury.com' + i['url']  # 拼接链接
        server = i['server'].replace('&nbsp;', ' ').split()  # 数据清理，替换脏数据
        img = i['imageUrl']
        memo = i['memo']
        price = i['price']
        address = i['address'].split()
        subject = i['subject']

        data = {'title': title, 'url': url, 'server': server, 'img': img, 'memo': memo,
                'price': price, 'adderss': address, 'subject': subject, 'create_time': now}

        url_list.insert_one(data)  # 将数据插入数据库

        print(data)


if __name__ == '__main__':
    # get_page_list(1)
    get_city_num()
