from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from project.items import SitelinkItem

class SitelinksSpider(BaseSpider):
    name = "sitelinks"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.jnto.go.jp/eng/location/destinations/spots.html"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//li')
        items = []
        for site in sites:
            item = SitelinkItem()
            try:
                item['link'] = site.select('a/@href').extract()
                if item['link'][0].find("location/spot") > 0:
                    #item['title'] = site.select('a/text()').extract()
                    items.append(item)
            except:
                pass
        return items
