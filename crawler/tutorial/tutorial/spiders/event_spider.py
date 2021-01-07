import scrapy

from scrapy.http import Request
from tutorial.items import TutorialItem
class EventSpider(scrapy.Spider):
    name = 'event'

    start_urls = ['https://www.eventbrite.com/d/united-states/all-events/?page=1']

    def parse(self, response):
        
        for event_link in set(response.css('div[class=eds-event-card-content__primary-content] a::attr(href)').extract()):
            print(event_link)
            item = TutorialItem()
            item['link'] = event_link

            req = Request(response.urljoin(event_link), callback=self.parse_event)
            req.meta['item'] = item
            yield req

        # pagination_link = response.css('li.next a::attr(href)').get()
        # req = Request(response.urljoin(pagination_link), callback=self.parse)
        # yield req

    def parse_event(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = response.meta['item']
        item['name'] = response.css('h1[class=listing-hero-title]::text').extract()[0]
        # item['birthdate'] = extract_with_css('.author-born-date::text')
        yield item



#root > div > div.eds-structure__body > div > div > div > div.eds-fixed-bottom-bar-layout__content > div > main > div > div > section.search-base-screen__search-panel > div.search-results-panel-content > div.search-main-content > ul > li:nth-child(1) > div > div > div.search-event-card-square-image > div > div > div > article > div > div.eds-event-card-content__content > div > div.eds-event-card-content__primary-content > a