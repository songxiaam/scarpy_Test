# -*- coding: utf-8 -*-
import scrapy
import re

class A51jobSpider(scrapy.Spider):
    name = '51job'
    # allowed_domains = ['www.51job.com', 'search.51job.com', 'jobs.51job.com']
    allowed_domains = ['51job.com']
    # start_urls = ['https://www.51job.com/']
    list_kws = ['iOS', 'Android', 'Python', 'Java']
    urls = []
    for kw in list_kws:
        url = 'https://search.51job.com/list/020000,000000,0000,00,9,99,%s,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=' % kw
        urls.append(url)
        # print(url)
    # start_urls = ['https://search.51job.com/list/020000,000000,0000,00,9,99,数据分析师,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']
    start_urls = urls

    # 会默认调用
    def parse(self, response):
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
        job_name = item_cn.xpath('h1/@title').extract()[0]
        # 2.公司名称
        company_name = item_cn.xpath('p[@class="cname"]/a[1]/@title').extract()[0]
        # 3.福利
        welfares = item_cn.xpath('div/div/span/text()').extract()
        # 4.月薪
        monthly_pay = item_cn.xpath('strong/text()').extract()[0]
        # 5.职位要求
        requirement = item_cn.xpath('p[2]/@title').extract()[0].replace(u'\xa0', u' ').replace(' ', '').split('|') # &nbsp解码


        item_detail = selector.xpath('/html/body/div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]/div[3]')
        # 6.职位详情
        # job_details = item_detail.xpath('div[1]/div[1]/p/text()').extract()
        job_details = item_detail.xpath('string(div[1]/div[1])').extract()[0] #字符串数据顺序错乱
        job_detail = job_details.replace(' ', '').replace('\n', '')
        print ('------------')
        print(job_detail)
        print ('++++++++++++')
        # 7.上班地址
        job_address = item_detail.xpath('div[2]/div/p/text()').extract()
        # 8.地图位置
        job_positions = self.sub_string(item_detail.xpath('div[2]/div/a/@onclick').extract()[0])
        job_map = ''
        if job_positions:
            job_map = job_positions[0]

        item_company = selector.xpath('/html/body/div[3]/div[2]/div[4]/div[1]')
        # 9.公司名称
        company_name = item_company.xpath('div[1]/a/p/@title').extract()[0]
        # 10.公司链接
        company_link = ''
        company_links = item_company.xpath('div[1]/a/@href').extract()
        if company_links:
            company_link = company_links[0]
        # 11.公司性质
        company_nature = item_company.xpath('div[2]/p[1]/text()').extract()[0]
        # 12.员工人数
        company_people = item_company.xpath('div[2]/p[2]/text()').extract()[0]
        # 13.所处行业
        company_industry = item_company.xpath('div[2]/p[3]/a/text()').extract()
        # print(job_name+"--"+company_name+','.join(welfares)+'--'+monthly_pay+'--'+','.join(requirement)+'\n'+job_address[1]+job_map+'\n'+' '.join(company_industry)+company_link)



    def sub_string(self, template):
        rule = r"'(.*?)'"
        return re.findall(rule, template)
