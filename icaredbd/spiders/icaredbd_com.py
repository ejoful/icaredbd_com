# -*- coding: utf-8 -*-
import scrapy
from icaredbd.items import IcaredbdItem
from scrapy_redis.spiders import RedisSpider


class IcaredbdComSpider(scrapy.Spider):
    name = 'icaredbd_com'
    allowed_domains = ['icaredbd.com']
    start_urls = ['http://icaredbd.com:6868/src/ebooks.php?&page_no=1']

    def parse(self, response):
        li_list = response.css('.table.table-striped tbody .link_bar')
        for link in li_list:
            item = IcaredbdItem()
            item['url'] = link.css('::attr(href)').extract_first()
            name_ext = link.css('::text').extract_first()
            name_ext_arr = name_ext.split('.')
            item['name'] = name_ext_arr[0]
            item['type'] = name_ext_arr[1]
            item['download_link'] = item['url'].\
                replace('download.php', 'downloadme.php')
            item['file_urls'] = [item['download_link']]
            yield item

        li_list = response.css('ul.pagination .page-link')
        for li in li_list:
            li_text = li.css('::text').extract_first()
            if li_text == '>>':
                next_url = li.css('::attr(href)').extract_first()
                yield scrapy.Request(next_url, callback=self.parse)
