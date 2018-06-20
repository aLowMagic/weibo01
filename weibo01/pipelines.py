# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import os
import requests


class Weibo01Pipeline(object):

    def process_item(self, item, spider):
        try:
            self.textProcess(item)
            self.picProcess(item)
        except:
            print("数据"+item['url_id']+"保存失败")

        return item

    def textProcess(self, item):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='admin',
                               use_unicode=True, db='weibo01', charset='utf8')
        cur = conn.cursor()
        try:
            sql = 'insert into texts(userid, content, url_id, source_id) values(\'%s\', \'%s\', \'%s\', \'%s\');'\
                  %(item['userid'], item['content'], item['url_id'], item['source_id'])
            cur.execute(sql)
            conn.commit()
        except:
            print("数据"+item['url_id']+"储存入数据库失败")
            conn.rollback()
        cur.close()
        conn.close()

    def picProcess(self, item):
        try:
            picUrls = item['picsUrl']
            if len(picUrls) != 0:
                rootPath = 'E:\\file\\GitHub\\weibo01\\picsData\\'+item['url_id']
                if not os.path.exists(rootPath):
                    os.makedirs(rootPath)
                for num in range(len(picUrls)):
                    try:
                        cookie = {'cookie': 'Cookie: _T_WM=1b0927332dd0c401011213b2d42c0c03; SUB=_2A252LCTpDeRhGeBK6VYT9C_FyjSIHXVV70yhrDV6PUJbkdBeLU3VkW1NR8ZLnGXU-udMphEWvwhTpVEbopoI71D3; SUHB=079j551FA90ely; SCF=AlaRhRGmsd5xln1_0ducFzhTsq6v6ncRgAmwwBap--gASE07Qwk8j9Z9YQd-kY5S0SiftAY_GYW_eS7jXu6KVjw.; SSOLoginState=1529369785; MLOGIN=1; WEIBOCN_FROM=1110106030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26lfid%3D106003type%253D1%26luicode%3D20000174%26uicode%3D20000174'}
                        us = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
                        req = requests.get(url=picUrls[num], headers=us, cookies=cookie)
                        if req.status_code == 200:
                            pic = req.content
                            picName = rootPath+'\\'+str((item['picStr'])[num])+'.jpg'
                            with open(picName, 'wb') as f:
                                f.write(pic)
                    except:
                        print(picUrls[num] + "访问失败")
            else:
                return
        except:
            print(item['url_id']+"储存图片失败")