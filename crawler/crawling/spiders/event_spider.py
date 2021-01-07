from __future__ import absolute_import
import scrapy
import json
import requests
from scrapy.http import Request
from crawling.spiders.lxmlhtml import CustomLxmlLinkExtractor as LinkExtractor
from scrapy.conf import settings

from crawling.items import RawResponseItem
from crawling.spiders.redis_spider import RedisSpider


class EventSpider(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "event"

    def __init__(self, *args, **kwargs):
        super(EventSpider, self).__init__(*args, **kwargs)

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


        def parse_event_id(url):
            return url.split("-")[-1].split("?")[0]

        def parse_events(s):
            s = s.split('"results":')
            r = s[1].split(',"aggs"')
            events = json.loads(r[0])
            return events

        def fetch_events_details(even_ids):
            event_ids_str = ",".join(even_ids)
            url = "https://www.eventbrite.com/api/v3/destination/events/?event_ids={}&expand=event_sales_status,primary_venue,image,saves,my_collections,ticket_availability&page_size=20".format(event_ids_str)

            payload={}
            headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
              'Referer': 'https://www.eventbrite.com/d/united-states/all-events/?page=1',
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': 'a9709ad2504f11ebbd0de767d03e109c',
              'Cookie': ''
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            return response.json()
        

        #1. If we want to scrap HTML
        # event_ids = []
        # for event_url in set(response.css('div[class=eds-event-card-content__primary-content] a::attr(href)').extract()):    
        #     event_ids.append(parse_event_id(event_url))
        #     #req = Request(response.urljoin(event_url), callback=self.parse_event)
            #req.meta['item'] = item
            #yield req 

        #2. If we want to fetch details from underlying API
        #all_events_details = fetch_events_details(event_ids)

        #3. Parse event details from response.text, 
        # spwaning callback to event details page to let scrapy cluster handle the any duplicate calls to urls because of multiple filters
        for event in parse_events(response.text):
            req = Request(event['url'], callback=self.parse_event)
            req.meta['event'] = event
            yield req


        pagination_link = response.xpath('//a[text()="Next"]/@href').get()
        if pagination_link:
            req = Request(response.urljoin(pagination_link), callback=self.parse)
            yield req

    #Get organizer and other event details
    def get_other_details(self,s):
        r = s.split('<script type="application/ld+json">')
        j = r[1].split('</script>')
        details = json.loads(j[0])
        return details

    def parse_event(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()



        # capture raw response
        item = RawResponseItem()
        # populated from response.meta
        item['appid'] = response.meta['appid']
        item['crawlid'] = response.meta['crawlid']
        item['attrs'] = response.meta['attrs']



        event = response.meta['event']
        try:
            item['event_name'] = event['name']
            item['event_url'] =  event['url'] #event_url
            item['event_image'] = event['image']['original']['url']
            event_categories = []
            event_formats = []
            for tag in event['tags']:
                if tag['prefix'] == 'EventbriteCategory':
                    event_categories.append(tag['display_name'])
                if tag['prefix'] == 'EventbriteFormat':
                    event_formats.append(tag['display_name'])
            item["event_category"] = ",".join(event_categories)
            item["event_format"] = ",".join(event_formats)
            item["event_location_type"] = "OnPrem"
            if event['is_online_event']:
                item["event_location_type"] = "Online"
            item['event_start_date'] = event['start_date']
            item['event_start_time'] = event['start_time']
            
            if 'end_date' in event:
                item['event_end_date'] = event['end_date']
            if 'end_time' in event:
                item['event_end_time'] = event['end_time']

            if 'primary_venue' in event:
                if 'name' in event['primary_venue']:
                    item['venue_name'] = event['primary_venue']['name']
                if 'address' in event['primary_venue']:
                    if 'country' in  event['primary_venue']['address']:
                        item['country'] = event['primary_venue']['address']['country']
                    if 'region' in  event['primary_venue']['address']:
                        item['state'] = event['primary_venue']['address']['region']
                    if 'city' in  event['primary_venue']['address']:
                        item['city'] = event['primary_venue']['address']['city']
        except Exception as e:
            print("KEY ERROR",e)

        #Optionally we can scrap some elements from event details page itself
        item['event_name'] = response.css('h1[class=listing-hero-title]::text').extract()[0]
        item['item_type'] = "event"
        
        organizer_details = self.get_other_details(response.text)['organizer']
        #organizer_item = OrganizerItem()
        item['organizer_name'] = organizer_details['name']
        item['organizer_profile_url'] = organizer_details['url']

        #item['event_organizer'] = organizer_item
        req = Request(organizer_details['url'], callback=self.parse_organizer)
        yield req
        yield item

    def parse_organizer(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()


        # capture raw response
        item = RawResponseItem()
        item['appid'] = response.meta['appid']
        item['crawlid'] = response.meta['crawlid']
        item['attrs'] = response.meta['attrs']


        item['item_type'] = "organizer" 

        other_details = self.get_other_details(response.text)
        if 'description' in other_details:
            item['organizer_description'] = other_details['description']
        item['organizer_profile_url'] = other_details['url']

        live_events_text = response.xpath("//*[contains(text(), 'Live Events')]/text()").extract_first()
        past_events_text = response.xpath("//*[contains(text(), 'Past Events')]/text()").extract_first()
        organiser_total_events = 0
        if live_events_text:
            organiser_total_events += int(live_events_text.strip("Live Events"))
        if past_events_text:
            organiser_total_events += int(past_events_text.strip("Past Events"))
        item['organiser_total_events'] = organiser_total_events

        yield item

