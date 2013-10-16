# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProjectItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class ScrapydemoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class SitelinkItem(Item):
    link = Field()

class SiteItem(Item):
    link = Field()
    title = Field()
    blurb = Field()
    info = Field()
