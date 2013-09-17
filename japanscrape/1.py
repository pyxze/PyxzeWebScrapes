# -*- coding: utf-8 -*-

import requests
from lxml import etree
import pickle
import os.path
import sys
sys.tracebacklimit = 0

def slugify(s):
    return "".join(x for x in s if x.isalnum() or x == ".")

def getText(url):
    r = requests.get(url)
    return r.content

def pickleTree(url):
    slug = slugify(url)
    if os.path.isfile("pickles/" + slug + ".pickle"):
        input = open("pickles/" + slug + ".pickle", "rb")
        t = pickle.load(input)
        input.close()
    else:
        t = getText(url)
        output = open("pickles/" + slug + ".pickle", "wb")
        pickle.dump(t, output)
        output.close()
    return etree.HTML(t)

url = "http://www.jnto.go.jp/eng/location/destinations/spots.html"
d = pickleTree(url)
spotlinks = d.xpath('//*[@class="index_box"]//a/@href')
# for link in spotlinks:
#     if link.find("location/spot") > 0:
#         try:
#             url = "http://www.jnto.go.jp" + link
#             d = pickleTree(url)
#             information = d.xpath('//*[@class="article_box"]//p/text()')
#             information = "".join(information).lstrip()
#             print information
#         except (KeyboardInterrupt, SystemExit):
#             raise

import Queue
import threading
from threading import Thread

def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

def do_work(url):
    try:
        url = "http://www.jnto.go.jp" + url
#        print url
        d = pickleTree(url)
#        try:
#            print d.xpath('//*[@id="page-title"]/h1/text()')
#        try:
        try:
            name = d.xpath('//*[@id="page-title"]/h1/text()')[0]
        except:
            name = "err"
        try:
            oneliner = d.xpath('//*[@class="article"]/h2/text()')[0]
        except:
            oneliner = "n/a"
        try:
            description = "".join(d.xpath('//*[@class="article"]/p/text()')).lstrip()
        except:
            description = "err"
        try:
            information = d.xpath('//*[@id="contents"]/div[1]/div//*/text()')
            informationtext = ""
            for part in information:
                informationtext += part.lstrip()
        except:
            informationtext = "err"
        try:
            parent = d.xpath('//*[@id="leftNavi"]/h3/a/text()')[0].title()
        except:
            parent = "err"
        print url, \
              "\n\nName:", name,\
              "\n\nOneliner:", oneliner,\
              "\n\nDescription:", description,\
              "\n\nInformation:", informationtext,\
              "\n\nParent:", parent

#        except:
#            print "Error with " + url
        # print page_title
#        except:
#            raise
        # information = d.xpath('//*[@class="article_box"]//p/text()')
        # information = "".join(information).lstrip()
        # print information
        print "-------------------"
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print "Problem with: " + url
        print "-------------------"
#        raise

q = Queue.Queue(maxsize=0)
for i in range(10):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in spotlinks:
    if item.find("location/spot") > 0:
        q.put(item)

q.join()