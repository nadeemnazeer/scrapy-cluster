# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    event_name = scrapy.Field()
    birthdate = scrapy.Field()
    link =  scrapy.Field()

class EventItem(scrapy.Item):
    # define the fields for your item here like:
    event_name = scrapy.Field()
    event_url =  scrapy.Field()
    event_id = scrapy.Field()
    event_category = scrapy.Field()
    event_format = scrapy.Field()
    event_image = scrapy.Field()
    event_location_type = scrapy.Field()

