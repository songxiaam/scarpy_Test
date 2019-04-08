# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import jieba

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
class DataClearnPipeline(self, item, spider):
    def process_item(self, item, spider):
    # 对于字符串,去除两端空格
    for key in item:
        item[key] = item[key].strip()
    # 对数据进一步分割处理
    # spider中的操作写到这里
    # 文本分词,提取关键词
    # jieba中文分词模块,引用jieba,需要安装(pip install jieba)
    # 判断异常值或空值数据,进行数据填充


    pass