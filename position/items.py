# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PositionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    positionId = scrapy.Field()
    education = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    industryField = scrapy.Field()
    workYear = scrapy.Field()
    companySize = scrapy.Field()
    financeStage = scrapy.Field()
    description = scrapy.Field()
