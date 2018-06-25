# -*- coding: utf-8 -*-

import scrapy
import json
import re
from weibo01.items import Weibo01TextItem
from weibo01 import settings

class spider0(scrapy.Spider):
    name = 'wbSpider01'
    start_urls = ['https://m.weibo.cn/beta']

    cookie = settings.COOKIE
    visited = set()
    onOffNum = 1
    currentPage = 1

    def start_requests(self):
        yield scrapy.Request(url='https://m.weibo.cn/feed/friends?version=v4', cookies=self.cookie, callback=self.parseRaw)

    def parseRaw(self, response):   #登陆后页面
        data = json.loads(response.body)
        body = data[0]['card_group']
        for count in range(self.onOffNum, len(body)):
            item = body[count]
            id = item['mblog']['id']
            scrollId = data[0]['next_cursor']

            if id not in self.visited:
                self.visited.add(id)
                urlPage = 'https://m.weibo.cn/status/%s' % id
                yield scrapy.Request(url=urlPage, cookies=self.cookie, callback=self.parsePage)
        self.onOffNum = 0
        urlScroll = 'https://m.weibo.cn/feed/friends?version=v4&next_cursor=%s&page=%s' % (scrollId, self.currentPage)
        yield scrapy.Request(url=urlScroll, cookies=self.cookie, callback=self.parseRaw)    #滚轮

    def parsePage(self, response):  #进入微博正文页面
        items = Weibo01TextItem()
        text = response.body.decode()
        reg = re.compile(" var \$render_data = \[\{([\s\S]*)?\}\]")
        res = '{' + reg.findall(text)[0] + '}'
        res = json.loads(res)
        status = res['status']
        try:
            urlid = 'https://m.weibo.cn/status/%s' % (status['id'])
            text = self.textDispose(status['text'])
            if text == "转发微博":
                return
            userInform = status['user']
            userid = userInform['id']

            if 'retweeted_status' in status:
                retweeted_status = status['retweeted_status']
                source_id = retweeted_status['id']
                yield scrapy.Request(url='https://m.weibo.cn/status/%s'
                                         % source_id, cookies=self.cookie, callback=self.parsePage)
            else:
                source_id = ""

            pics = status['pic_ids']
            picList = []
            picStr = []
            if len(pics) != 0:
                for pic in pics:
                    picUrl = 'https://wx4.sinaimg.cn/large/%s.jpg' % str(pic)
                    picStr.append(pic)
                    picList.append(picUrl)

            items['url_id'] = status['id']
            items['content'] = text.replace('\n', '')
            items['userid'] = userid
            items['source_id'] = source_id
            items['picsUrl'] = picList
            items['picStr'] = picStr

            yield items

        except:
            self.log(urlid+" 链接未成功处理")


    def textDispose(self, text):    #text文件中有标签，把标签处理掉
        reg = re.compile(r'<[^>]+>')
        reText = reg.sub("", text)
        return reText
