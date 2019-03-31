# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# class TempItem(scrapy.Item):
#     test01 = scrapy.Field()
#     test02 = scrapy.Field()


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    job_name = scrapy.Field()
    company_name = scrapy.Field()
    monthly_pay_min = scrapy.Field()
    monthly_pay_max = scrapy.Field()
    area = scrapy.Field()
    company_link = scrapy.Field()
    company_info = scrapy.Field()
    experience = scrapy.Field() #工作经验
    education = scrapy.Field()
    address = scrapy.Field()

    # test = scrapy.Field(TempItem)

