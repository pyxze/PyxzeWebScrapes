# -*- coding: utf-8 -*-

import requests
from lxml import etree
import pickle
import os.path

def slugify(s):
    return "".join(x for x in s if x.isalnum() or x == ".")

def getText(url):
    r = requests.get(url)
    return r.text

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

# Go through initial crawl to get podcast links
if os.path.isfile("pickles/podcast_links.pickle"):
    input = open("pickles/podcast_links.pickle", "rb")
    podcast_links = pickle.load(input)
    input.close()
else:
    if not os.path.exists("pickles"):
        os.makedirs("pickles")
    podcast_links = set()
    url = "https://itunes.apple.com/us/genre/podcasts/id26?mt=2"
    d = pickleTree(url)
    categoryLinks = d.xpath('//*[@id="genre-nav"]//a/@href')
    for categoryLink in categoryLinks:
        print categoryLink
        d = pickleTree(categoryLink)
        alphaLinks = d.xpath('//*[@id="selectedgenre"]/ul//a/@href')
        for alphaLink in alphaLinks:
            print alphaLink
            d = pickleTree(alphaLink)
            number_of_pagination_links = d.xpath('//*[@id="selectedgenre"]/ul[2]//a/@href').__len__()
            if number_of_pagination_links == 0:
                number_of_pages = 1
            else:
                number_of_pages = number_of_pagination_links - 1
            for page in range(1,number_of_pages+1):
                print "page", page
                d = pickleTree(alphaLink + "&page=%s#page" % page)
                for podcast_link in d.xpath('//*[@id="selectedcontent"]//a/@href'):
                    get_finder = podcast_link.find("?")
                    if get_finder == -1:
                        print podcast_link
                        podcast_links.add(str(podcast_link))
                    else:
                        print podcast_link[:get_finder]
                        podcast_links.add(str(podcast_link[:get_finder]))
    output = open("pickles/podcast_links.pickle", "wb")
    pickle.dump(podcast_links, output)
    output.close()