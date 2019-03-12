# -*- coding: utf-8 -*-
import scrapy


class TextjobSpider(scrapy.Spider):
    name = 'textJob'
    allowed_domains = ['www.51job.com', 'jobs.51job.com']
    start_urls = ['https://jobs.51job.com/shanghai-ypq/107108862.html?s=01&t=0']

    def parse(self, response):
        print(response.text)
