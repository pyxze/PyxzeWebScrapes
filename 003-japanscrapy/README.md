This is a demo of the japanscrape using scrapy. http://scrapy.org/

Once you have scrapy installed, you can run:

scrapy crawl sitelinks --nolog -o sitelinks.csv -t csv

in the first level project folder to create a csv of the site links.

I copied those links into site_spider.py, which lets you use:

scrapy crawl site --nolog -o site.csv -t csv

to create a csv of some of the site data.
