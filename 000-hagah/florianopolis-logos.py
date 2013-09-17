# -*- coding: latin-1 -*-

import requests
from bs4 import BeautifulSoup
from lxml import etree
import pickle
import os.path

def makeSoup(url):
    result = requests.get(url)
    text = result.text
    return BeautifulSoup(text)

def makeTree(u):
    r = requests.get(u)
    t = r.text
    return etree.HTML(t)

input = open("hagah-florianopolis-vendorlinks.pickle", "rb")
vendorLinks = pickle.load(input)
input.close()

for u in vendorLinks:
    try:
        d = makeTree(u)
        try:
            logo = d.xpath('//*[@class="wrap-logo-busca"]/img/@src')[0]
            file = requests.get(logo)
            slug = "".join(x for x in logo if x.isalnum() or x == ".")
            f = open(slug, "w")
            f.write(file.content)
            f.close()
            print u, " | ", slug
        except:
            pass
    except:
        pass
