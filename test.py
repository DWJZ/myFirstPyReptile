#coding=utf-8
import requests
from scrapy import Selector
import pymongo
import os
import re
import  time
MongoClient = pymongo.MongoClient
Client = MongoClient()

client = MongoClient('172.27.7.94', 27017)
db = client['test']
data = db['data']

arr = []
page = 1

def getUrlContent(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3107.4 Safari/537.36'
    }
    page = requests.get(url=url, headers=header,timeout=10)
    return page.content

def getImgListUrl(content):
    se = Selector(text=content)
    li = se.xpath("//div[@class='random_title']/text()").extract()
    aItems = se.xpath("//a[@class='list-group-item random_list']").extract()
    arr = []
    for aItem in aItems:
        arr.append({
            'href': Selector(text=aItem).xpath("//a[@class='list-group-item random_list']/@href").extract()[0],
            'title': Selector(text=aItem).xpath("//div[@class='random_title']/text()").extract()[0]
        })

    for arrItem in arr:

        filePath = 'D:\\doutula\\' + arrItem['title']
        filePath = ''.join(filePath.split(' '))

        if not os.path.isdir(filePath):
            os.makedirs(filePath)
        getImgList(url=arrItem['href'], filePath=filePath)


def getImgList(url, filePath):
    content = getUrlContent(url)
    se = Selector(text=content)
    artile_desList = se.xpath('//div[@class="artile_des"]').extract()

    for artile_des in artile_desList:
        artile_des = Selector(text=artile_des)
        imgUrl = artile_des.xpath("//img/@src").extract()[0].strip('https://')
        imgUrl = 'https://' + imgUrl
        imgName = artile_des.xpath("//img/@alt").extract()[0]

        imgName = re.sub("[\s+\.\?\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),imgName) # 去除标点符号
        if (len(imgName) > 20) :
            imgName = imgName[:20]  # 截取字符串

        suffix = os.path.splitext(imgUrl)[1]
        imgContent =  getUrlContent(imgUrl)


        fileName = filePath + '\\' + imgName + suffix.lower()
        print fileName

        with open(unicode(fileName), 'wb') as f:
            f.write(imgContent)


def start():
    content = getUrlContent('https://www.doutula.com/article/list/')
    se = Selector(text=content)
    lastPage = se.xpath("//ul[@class='pagination']/li[last()-1]/a/text()").extract()[0]
    for page in range(46,int(lastPage)+1):
        try:
            getImgListUrl(getUrlContent('https://www.doutula.com/article/list/?page=' + str(page)))
            print u'---------------------爬取' + str(page) +u'页完成-----------------'
        except Exception as e:
            print e
            continue

    print u'爬取完成'
start()

