# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Item, Field
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


class OrganizerItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    response_url = Field()
    status_code = Field()
    status_msg = Field()
    response_headers = Field()
    request_headers = Field()
    body = Field()
    links = Field()
    attrs = Field()
    success = Field()
    exception = Field()
    encoding = Field()
    organizer_name = Field()
    organizer_profile_url =  Field()
    organizer_description = Field()

class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    response_url = Field()
    status_code = Field()
    status_msg = Field()
    response_headers = Field()
    request_headers = Field()
    body = Field()
    links = Field()
    attrs = Field()
    success = Field()
    exception = Field()
    encoding = Field()
    name = Field()
    birthdate = Field()
    text =  Field()
    
    event_name = Field()
    event_url =  Field()
    event_id = Field()
    event_category = Field()
    event_format = Field()
    event_image = Field()
    event_location_type = Field()
    event_start_date = Field()
    event_end_date = Field()
    event_start_time = Field()
    event_end_time = Field()
    event_organizer = Field()
    organizer_name = Field()
    organizer_profile_url =  Field()
    organizer_description = Field()
    venue_name = Field()
    street_address_1 = Field() 
    street_address_2 = Field()
    city = Field()
    state = Field()
    country = Field()
