# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import jieba.analyse as jal
import time
import pymysql

class JobsPipeline(object):
    # item容器
    # 生成对应item的spider爬虫
    def process_item(self, item, spider):
        return item

    # spider开启时调用
    def open_spider(self, spider):
        pass

    # spider关闭时调用
    def close_spider(self, spider):
        pass

    # 返回爬虫实例化对象(新建管道的爬虫实例)
    @classmethod
    def from_crawler(cls, crawler):
        pass

#数据去重
class DropItemPipeline(object):
    #初始化建立 set, 储存职位名称+公司名称组合
    def __init__(self):
        self.set_names = set()

    # 默认执行方法,判断item中职位名称+公司名称是否在set_names中,
    # 如果存在,则抛出异常,丢弃item,
    # 否则储存到set_names中,并返回item给后面的管道
    # 仅对本次爬虫执行有效
    def process_item(self, item, spider):
        tmp = item['job_name']+item['company_name']
        # 已经存在
        if tmp in self.set_names:
            # 手动抛出异常
            raise DropItem('already existed')
        else:
            self.set_names.add(tmp)
            return item


#数据清洗
class DataClearPipeline(object):
    def process_item(self, item, spider):
        # 对于字符串,去除两端空格
        for key in item:
            item[key] = item[key].strip()
        # 对数据进一步分割处理
        # spider中的操作写到这里
        # 文本分词,提取关键词
        # jieba中文分词模块,引用jieba,需要安装(pip install jieba)
        # 对于岗位职责和任职要求做关键字提取
        job_details_fenci = jal.extract_tags(item['job_detail'], topK=10)
        item['job_detail_keyword'] = '/'.join(job_details_fenci)
        print(job_details_fenci)
        # 判断异常值或空值数据,进行数据填充
        # 1.判断薪资是否为空
        if item['monthly_pay_min'] == '':
            item['monthly_pay_min'] = 0
        if item['monthly_pay_max'] == '':
            item['monthly_pay_max'] = 0
        # ... 其他为空判断

class DataTimePipeline(object):
    def process_item(self, item, spider):
        time.time()


# 数据存储
class MySqlPipeline(object):
    # 建立初始化方法
    def __init__(self, mysql_host, mysql_user, mysql_passwd, mysql_db):
        self.MYSQL_HOST=mysql_host
        self.MYSQL_USER=mysql_user
        self.MYSQL_PASSWD=mysql_passwd
        self.MYSQL_DB=mysql_db

    # 从seting提取mysql配置信息
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # crawler.settings.get()表示从settings文件查找配置信息
            # mysql_host = crawler.settings.get('MYSQL_HOST', 'localhost')
            # mysql_user = crawler.settings.get('MYSQL_USER', 'py')
            # mysql_passwd = crawler.settings.get('MYSQL_PASSWD', '2654615Ww')
            # mysql_db = crawler.settings.get('MYSQL_DB', 'job')
            )

    # 启动爬虫时连接数据库
    def open_spider(self, spider):
        # self.conn = pymysql.connect(host=)
