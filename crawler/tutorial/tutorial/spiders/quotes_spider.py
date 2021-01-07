import scrapy

from scrapy.http import Request
from tutorial.items import TutorialItem
class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        
        for quote in response.css('div.quote'):
            item = TutorialItem()
            item['text'] = quote.css('span.text::text').get()
            
            author_page_link = quote.css('.author + a::attr(href)').get()
            print(author_page_link)
            req = Request(response.urljoin(author_page_link), callback=self.parse_author)
            req.meta['item'] = item
            yield req

        pagination_link = response.css('li.next a::attr(href)').get()
        req = Request(response.urljoin(pagination_link), callback=self.parse)
        yield req

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = response.meta['item']
        item['name'] = extract_with_css('h3.author-title::text')
        item['birthdate'] = extract_with_css('.author-born-date::text')
        yield item