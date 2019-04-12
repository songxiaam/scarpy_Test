# -*- coding: utf-8 -*-
import scrapy
import re
from jobs.items import JobsItem

from idna import unicode


class A51jobSpider(scrapy.Spider):
    name = '51job'
    # allowed_domains = ['www.51job.com', 'search.51job.com', 'jobs.51job.com']
    allowed_domains = ['51job.com']
    # start_urls = ['https://www.51job.com/']
    # list_kws = ['iOS', 'Android', 'Python', 'Java']
    list_kws = ['iOS']
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

        # 实例化
        job_item = JobsItem()


        selector = scrapy.Selector(response)

        item_cn = selector.xpath('/html/body/div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]/div[@class="tHeader tHjob"]/div/div[@class="cn"]')
        # 1.职位名称
        # job_name = selector.xpath('/html/body/div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]/div[@class="tHeader tHjob"]/div/div[@class="cn"]/h1/@title').extract()
        job_name = item_cn.xpath('h1/@title').extract()[0]
        job_item.job_name = job_name
        # 2.公司名称
        company_name = item_cn.xpath('p[@class="cname"]/a[1]/@title').extract()[0]
        job_item.company_name = company_name
        # 3.福利
        welfares = item_cn.xpath('div/div/span/text()').extract()
        # 4.月薪
        monthly_pay = item_cn.xpath('strong/text()').extract()[0]
        #  x-y 元/天 千/月 万/月 万以上/月 万/年 万以上/年
        tmp_dict = {'元/天': 30, '千/月': 1000, '千以上/月': 1000, '千以下/月':  1000, '万/月': 10000, '万以上/月': 10000, '万/年': 1/12, '万以上/年': 1/12}
        money_min = 0
        money_max = 0
        for key, value in tmp_dict.items():
            if monthly_pay.strip() == '':
                money_min = money_max = 0
                break

            elif key in monthly_pay:
                temp_money = monthly_pay.strip(key)
                temp_money_list = temp_money.split('-')
                if len(temp_money_list) == 2:
                    money_min = float(temp_money_list[0])*value
                    money_max = float(temp_money_list[1])*value
                    break
                else:
                    money_min = money_max = float(temp_money)*value
                    break
        job_item.monthly_pay_min = money_min
        job_item.monthly_pay_max = money_max
        # print('------------- %d ~ %d' % (money_min, money_max))
        # 5.职位要求
        requirement = item_cn.xpath('p[2]/@title').extract()[0].replace(u'\xa0', u' ').replace(' ', '').split('|') # &nbsp解码

        # 工作地
        addrStr = requirement[0]
        addrList = addrStr.split('-')
        city = addrList[0]
        area = ''
        if len(addrList) == 2:
            area = addrList[1]
        job_item.area = area
        # 经验
        experience = '无工作经验'
        # 学历
        educationArr = ['初中及以下', '高中/中技/中专', '大专', '本科', '硕士', '博士']
        education = '所有'
        # 人数
        count = 0
        for item in requirement:
            if '年经验' in item:
                experience = item[:-3]
            elif item in education:
                education = item
            elif re.match(r'招.*?人', item):
                count_str = item[1:-1]
                if count_str == '若干':
                    count = 0
                else:
                    count = int(count_str)

        # print('工作城市%s, 区:%s, 经验:%s, 学历:%s, 招聘%s人' % (city, area, experience, education, ('若干' if count == 0 else str(count))))

        job_item.education = education
        job_item.experience = experience

        item_detail = selector.xpath('/html/body/div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]/div[3]')
        # 6.职位详情
        # job_details = item_detail.xpath('div[1]/div[1]/p/text()').extract()
        job_details = item_detail.xpath('string(div[1]/div[1])').extract()[0] #terminal打印不完整
        # print('------------')
        # print(job_details)
        job_item.job_detail = job_details
        com = re.compile(u'(岗位职责|工作职责)[:：]?(.*?)(任职资格|任职要求)[:：]?(.*?)(职能类别)[:：]?(.*?)(关键字)[:：]?')
        re_list = re.findall(com, unicode(job_details))
        if re_list:
            print(re_list[0][0].strip())

        # print('++++++++++++')
        # job_detail = job_details.replace(' ', '').replace('\n', '')

        # job_details = item_detail.xpath('div[1]/div/')
        # for item in item_detail:
        #     title_h2 = item.xpath('h2/span/text()').extract()[0]
        #     detail_p = item.xpath('string(div)').extract()[0]
        #
        #     print ('------------')
        #     print(detail_p)
        #     print ('++++++++++++')


        # print(selector.xpath('/html/body/div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]/div[3]/div[1]/h2/span/text()').extract()[0])

        # 7.上班地址
        job_address = item_detail.xpath('div[2]/div/p/text()').extract()
        job_item.address = job_address
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
        job_item.company_link = company_link
        # 11.公司性质
        company_nature = item_company.xpath('div[2]/p[1]/text()').extract()[0]
        # 12.员工人数
        company_people = item_company.xpath('div[2]/p[2]/text()').extract()[0]
        # 13.所处行业
        company_industry = item_company.xpath('div[2]/p[3]/a/text()').extract()
        # 14.公司信息
        company_info = item_detail.xpath('string(div[3]/div)').extract()[0]
        job_item.company_info = company_info
        # print(company_info)
        # print(job_name+"--"+company_name+','.join(welfares)+'--'+monthly_pay+'--'+','.join(requirement)+'\n'+job_address[1]+job_map+'\n'+' '.join(company_industry)+company_link)
        # yield job_item

        return job_item # 将item提交给管道

    def sub_string(self, template):
        rule = r"'(.*?)'"
        return re.findall(rule, template)
