# -*- coding: utf-8 -*-
import scrapy

#从items文件导入Item类
from test1.items import Test1Item

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['lab.scrapyd.cn']
    
    #词条有7页，使用列表推导式改写一下start_urls
    start_urls = ['http://lab.scrapyd.cn/page/{}/'.format(page) for page in range(1, 7)]

    def parse(self, response):
        #获取所有词条
        divs = response.xpath('.//div[@class="quote post"]')

        #遍历div获取该页的内容
        for div in divs:
            #创建存放数据的item
            item = Test1Item()
            
            #获取作者，要使用extract()提取，extract()返回的是列表
            item['author'] = div.xpath('.//small[@class="author"]/text()').extract()[0]
            
            #获取标签
            item['tag'] = ','.join(div.xpath('.//a[@class="tag"]/text()').extract())
            
            #获取文本
            item['text'] = div.xpath('.//span[@class="text"]/text()').extract()

            #每个item都是一个词条，获取后程序还要继续运行，所以用yield
            yield item
