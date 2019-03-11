# -*- coding: utf-8 -*-
import scrapy


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['www.zhaopin.com', 'sou.zhaopin.com']  # 域名
    start_urls = ['http://www.zhaopin.com/'] # 开始链接

    # 多个搜索关键词 页面
    def parse(self, response):
        # 完成自定义关键字搜索
        # https://sou.zhaopin.com/?jl=538&kw=数据分析师&kt=3
        list_kw = ['数据分析师']
        for kw in list_kw:
            url = 'https://sou.zhaopin.com/?jl=538&kw=%s&kt=3' % (kw)
            # 网页请求,提交给scrapy调度器,完成页面内容的下载
            # scrapy.Request(url=url, callback=self.parse_list)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_list)

    # 解析单个页面,获得职业列表,并完成下一页链接获取,提交给自身
    def parse_list(self, response):
        # 1.建立选择器
        selector = scrapy.Selector(response)
        # 2.完成列表详细页面链接的获取
        # //*[@id="listContent"]/div[1]
        # (1)先获取大于1的div数组
        # // *[ @ id = "listContent"] / div[79]
        # //*[@id="listContent"]
        # print(selector.text)
        # //*[@id="listContent"]
        # // *[ @ id = "listContent"] / div[1]
        list_content = selector.xpath('//div[@id="listItemPile"]/div[2]')
        # (2)遍历得到的的div数组,获取每个div下的详细数据
        print('================')
        print(list_content)
        return
        for div_item in list_content:
            info_href = div_item.xpath('div/a/@href').extract()
            # extract() 将Selector 节点对象转换为列表形式
            print('----------------')
            print(info_href[0])
            return
            yield scrapy.Request(url=info_href[0], callback=self.parse_info, dont_filter=True)
        # 3.完成下一页处理
        # 构建下一页url
        # 下一页按钮是否可用
        # next_disable = selector.xpath('//*[@id="pagination_content"]/div/button[2]/@disable')
        # if next_disable == 'disable':
        #     pages = selector.xpath('//*[@id="pagination_content"]/div/span[position>=1]')
        #     for span_item in pages:
        #         span_info = span_item.xpath('@class').extract()
        #         active = 'soupager__index--active'
        #         result = active in span_info[0]
        #         if result:
        #             texts = span_item.xpath('.//text()').extract()
        #             url = 'https://sou.zhaopin.com/?p=%d&jl=538&kw=%s&kt=3'%(int(texts[0])+1, key)
        #             # 递归
        #             yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)
        # 4.完成详细页面数据获取

    # 解析职业详情页
    def parse_info(self, response):
        print(response.url)
        selector = scrapy.Selector(response)
        # 1.职位名称
        job_name = selector.xpath('//h1[@class="l info-h3"]')
        print(job_name[0])
        # 2.公司名称
        # 3.福利信息
        # 4.月薪
        # 5.工作地点
        # 6.发布时间
        # 7.公司性质
        # 8.工作经验
        # 9.最低学历
        # 10.招聘人数
        # 11.职位类型
        # 12.公司规模
        # 13.所属行业
























