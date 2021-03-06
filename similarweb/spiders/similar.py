# -*- coding: utf-8 -*-
import scrapy
import json
import re
from similarweb.items import SimilarwebItem


class SimilarSpider(scrapy.Spider):
    name = 'similar'
    allowed_domains = ['similarweb.com']

    def start_requests(self):
        headers = dict()
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        default_url = 'https://www.similarweb.com/website/'
        domains_data = open('domains.json')
        domains = json.load(domains_data)
        for domain in domains:
            yield scrapy.Request(default_url+domain, callback=self.parse, headers=headers)

    def parse(self, response):
        traffic_response = re.findall('WeeklyTrafficNumbers":{[^}]*}', response.text)[0]
        traffic_json = traffic_response[22:]

        domain = response.url.split('/')[-1]
        traffic = json.decoder.JSONDecoder().decode(traffic_json)

        item = SimilarwebItem(domain=domain, traffic=traffic)
        yield item
