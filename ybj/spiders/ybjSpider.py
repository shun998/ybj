import scrapy

from ybj.items import YbjItem


class YbjspiderSpider(scrapy.Spider):
    name = 'ybjSpider'
    allowed_domains = ['ybj.beijing.gov.cn']
    start_urls = ['http://ybj.beijing.gov.cn/']
    start_urls = ['http://ybj.beijing.gov.cn/zwgk/2020_zcwj/index.html',
                  'http://ybj.beijing.gov.cn/zwgk/2020_zcwj/index_1.html',
                  'http://ybj.beijing.gov.cn/zwgk/2020_zcwj/index_2.html',
                  'http://ybj.beijing.gov.cn/zwgk/2020_zcwj/index_3.html',
                  'http://ybj.beijing.gov.cn/zwgk/2020_zcwj/index_4.html'
                  ]  # 第一个要抓取的url

    # response 为 start_urls中影响对象

    def parse(self, response):
        text_list = response.xpath('//ul[@class="text_list"]/li/a/@href')
        # title_urls = []
        for dd in text_list:
            # print(response.request.url)
            title_url = str(response.request.url)[0:40] + str(dd.get())[1:]
            # print(str(response.request.url)[0:40] + str(dd.get())[1:])
            # title_urls.append(title_url)
            yield scrapy.Request(url=title_url, callback=self.parse_detail)

    def parse_detail(self, response):
        title = response.xpath('//div[@class="article_header"]//p/text()').get()
        # content_line = response.xpath('//div[@class="article"]//p*/text()').get()
        content_box = response.xpath('//div[@class="article"]')
        content = str(content_box.xpath('string(.)').get()).strip()
        # print(content)
        # content_lines = content_box.xpath('.//p/text()').get()
        # print(content_box)
        url = response.request.url
        item = YbjItem()
        item['title'] = title
        item['content'] = content
        item['url'] = url
        yield item
        # print(title, content)
