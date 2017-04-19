from scrapy import Spider
from scrapy.http import Request
from scrapy.http import FormRequest
import json
import math
import re
from position.items import PositionItem


class MySpider(Spider):
    name = 'position'
    allowed_domains = ['lagou.com']

    def __init__(self):
        super().__init__()
        self.url = 'http://www.lagou.com/jobs/positionAjax.json'
        self.cookies = {
            'user_trace_token': '20170408172550-237840596dd94ae88b379b3791a8c469',
            'index_location_city': '%E5%85%A8%E5%9B%BD',
            'SEARCH_ID': 'e354eea8e1b84ef891abe7071aa316e2',
            'JSESSIONID': 'B93ACD36FC4545F3D9F5DA36E4B5BE0E',
            'TG-TRACK-CODE': 'index_navigation',
            'LGSID': '20170408203621-f83ee032-1c57-11e7-bece-525400f775ce',
            'LGRID': '20170408175306-2a18769d-1c41-11e7-be1b-525400f775ce',
            'LGUID': '20170408173849-2b42c224-1c3f-11e7-9d69-5254005c3644',
            '_ga': 'GA1.2.502905871.1491644464',
            '_gat': '1'
        }
        self.pn = 1

    def start_requests(self):
        yield FormRequest(self.url, formdata={'first': 'true', 'pn': str(self.pn), 'kd': 'python'},
                          callback=self.first_parse, cookies=self.cookies)

    def first_parse(self, response):
        jdict = json.loads(response.text)
        jcontent = jdict["content"]
        jposresult = jcontent["positionResult"]
        self.pn = math.ceil(jposresult['totalCount'] / jposresult['resultSize'])
        for n in range(2, self.pn + 1):
            yield FormRequest(self.url, formdata={'first': 'false', 'pn': str(n), 'kd': 'python'},
                              callback=self.parse)
        return self.parse(response)

    def parse(self, response):
        jdict = json.loads(response.text)
        jcontent = jdict["content"]
        jposresult = jcontent["positionResult"]
        jresult = jposresult["result"]
        for position in jresult:
            yield Request('https://www.lagou.com/jobs/' + str(position['positionId']) + '.html',
                          callback=self.description, meta={'position': position})

    @classmethod
    def description(cls, response):
        text = ''.join(response.css('.job_bt > div:nth-child(2) *::text').extract())
        text = re.sub('\s+', '', text)
        item = PositionItem()
        position = response.meta['position']
        item['positionId'] = position['positionId']
        item['education'] = position['education']
        item['city'] = position['city']
        item['salary'] = position['salary']
        item['industryField'] = position['industryField']
        item['workYear'] = position['workYear']
        item['companySize'] = position['companySize']
        item['financeStage'] = position['financeStage']
        item['description'] = text
        yield item
