from __future__ import absolute_import
import scrapy

from scrapy.http import Request
from crawling.spiders.lxmlhtml import CustomLxmlLinkExtractor as LinkExtractor
from scrapy.conf import settings

from crawling.items import RawResponseItem
from crawling.spiders.redis_spider import RedisSpider


class AuthorSpider(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "author"

    def __init__(self, *args, **kwargs):
        super(AuthorSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        self._logger.debug("crawled url {}".format(response.request.url))
        cur_depth = 0
        if 'curdepth' in response.meta:
            cur_depth = response.meta['curdepth']

        # capture raw response
        item = RawResponseItem()
        # populated from response.meta
        item['appid'] = response.meta['appid']
        item['crawlid'] = response.meta['crawlid']
        item['attrs'] = response.meta['attrs']

        # populated from raw HTTP response
        item["url"] = response.request.url
        item["response_url"] = response.url
        item["status_code"] = response.status
        item["status_msg"] = "OK"
        item["response_headers"] = self.reconstruct_headers(response)
        item["request_headers"] = response.request.headers
        item["body"] = ""
        item["encoding"] = response.encoding
        item["links"] = []

        # link_extractor = LinkExtractor(
        #                     allow_domains=response.meta['allowed_domains'],
        #                     allow=response.meta['allow_regex'],
        #                     deny=response.meta['deny_regex'],
        #                     deny_extensions=response.meta['deny_extensions'])

        # for link in link_extractor.extract_links(response):
        #         the_url = link.url
        #         the_url = the_url.replace('\n', '')
        #         item["links"].append({"url": the_url, "text": link.text, })
        #         if 'useragent' in response.meta and \
        #                 response.meta['useragent'] is not None:
        #             req.headers['User-Agent'] = response.meta['useragent']
                # link that was discovered
                # if '/author/' in the_url:
                #     req = Request(the_url, callback=self.parse_author)
                #     yield req
                # if '/page/' in the_url:
                #     req = Request(the_url, callback=self.parse)

                #     yield req
        for quote in response.css('div.quote'):
            item['text'] = quote.css('span.text::text').get()
            
            author_page_link = quote.css('.author + a::attr(href)').get()
            print(author_page_link)
            req = Request(response.urljoin(author_page_link), callback=self.parse_author)
            req.meta['text'] =quote.css('span.text::text').get()
            yield req

        pagination_link = response.css('li.next a::attr(href)').get()
        if pagination_link:
            req = Request(response.urljoin(pagination_link), callback=self.parse)
            yield req


    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
                    # capture raw response
        item = RawResponseItem()
        item['text'] = response.meta['text']
        # populated from response.meta
        item['appid'] = response.meta['appid']
        item['crawlid'] = response.meta['crawlid']
        item['attrs'] = response.meta['attrs']

        # populated from raw HTTP response
        item["url"] = response.request.url
        item["response_url"] = response.url
        item["status_code"] = response.status
        item["status_msg"] = "OK"
        item["response_headers"] = self.reconstruct_headers(response)
        item["request_headers"] = response.request.headers
        item["body"] = ""
        item["encoding"] = response.encoding
        item["links"] = []


        item['name'] = extract_with_css('h3.author-title::text')
        item['birthdate'] = extract_with_css('.author-born-date::text')
        print(".................parsing details")

        yield item
