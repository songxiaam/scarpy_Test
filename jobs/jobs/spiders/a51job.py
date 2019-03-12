# -*- coding: utf-8 -*-
import scrapy


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['www.51job.com', 'search.51job.com', 'jobs.51job.com']
    # start_urls = ['https://www.51job.com/']
    list_kws = ['iOS', 'Android', 'Python', 'Java']
    urls = []
    for kw in list_kws:
        url = 'https://search.51job.com/list/020000,000000,0000,00,9,99,%s,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=' % kw
        urls.append(url)
        # print(url)
    # start_urls = ['https://search.51job.com/list/020000,000000,0000,00,9,99,数据分析师,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']
    start_urls = urls


    def parse(self, response):
        # list_kw = ['数据分析师']F%
        # for kw in list_kw:
        #     url = 'https://search.51job.com/list/020000,000000,0000,00,9,99,%s,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='%
        # (kw)
        #     print("===========")
        #     print(url)
        #     yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)


        # url = "https://search.51job.com/list/020000,000000,0000,00,9,99,数据分析师,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        # yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)

        selector = scrapy.Selector(response)
        result_list = selector.xpath('//*[@id="resultList"]/div[@class="el"]')
        for div_item in result_list:
            info_href = div_item.xpath('p/span/a/@href').extract()
            url = info_href[0]
            # print(url)
            if "jobs.51job.com" in url:
                yield scrapy.Request(url=url, callback=self.parse_info, dont_filter=True)
        # info_href = div_item.xpath('p/span/a/@href').extract()
        # scrapy.Request(url=info_href[0], callback=self.parse_info, dont_filter=True)


    # def parse_list(self, response):
    #     selector = scrapy.Selector(response)
    #     result_list = selector.xpath('//*[@id="resultList"]/div[@class="el"]')
    #     print('---------')
    #     print(result_list)
    #     return
    #     for div_item in result_list:
    #         info_href = div_item.xpath('p/span/a/@href').extract()
    #         print(info_href[0])
    def parse_info(self, response):
        selector = scrapy.Selector(response)

        item_cn = selector.xpath('/html/body/div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]/div[@class="tHeader tHjob"]/div/div[@class="cn"]')
        # 1.职位名称
        # job_name = selector.xpath('/html/body/div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]/div[@class="tHeader tHjob"]/div/div[@class="cn"]/h1/@title').extract()
        job_name = item_cn.xpath('h1/@title').extract()
        # 2.公司名称
        company_name = item_cn.xpath('p[@class="cname"]/a[1]/@title').extract()
        # 3.福利
        welfares = item_cn.xpath('div/div/span/text()').extract()
        # 4.月薪
        monthly_pay = item_cn.xpath('strong/text()').extract()
        print(job_name[0]+"--"+company_name[0]+','.join(welfares)+'--'+monthly_pay[0])

