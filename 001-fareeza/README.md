This web scrape was for gathering podcast information from iTunes. A notable feature is that I stopped using BeautifulSoup at this point and just started relying on lxml. This scrape uses pickling to cache webpage data.

The files are fairly self-evident. 1-collect-podcast-links.py collects the links for the category pages.

2-print-links-and-load-into-database.py goes through the category pages and collects all of the podcast links, using sqlalchemy to load this data into a sqlite database.

Finally, 3-collect-podcast-data.py goes through the links and grabs podcast information from the site, such as episode links and titles.

This scrape would occasionally fail while running 3-collect-podcast-data.py. Signs point to this being a disk write/read issue, and if I were to do this again I would likely dump the data to a bona fide database, such as postgresql.

The way I dealt with this issue was to have the script pull a url from the stack, try to scrape it, and not remove the url from the database until a successful write.

Another issue with this script was that it took a long long time to process. It wasn't the number of pages that was the problem (200,000) but the number of episodes in some of the pages -- some had up to 300 -- which resulted in over 6 million lines of (denormalized) data.

An obvious fix for this issue is multithreading, which I implemented in my next (demo) scrape. However, the Python web scraping framework Scrapy has caching AND multithreading built in (via Twisted), so I would likely just use Scrapy for future scrapes...
