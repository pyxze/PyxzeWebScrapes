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
        begin = u.find("local")
        end = u.find(",")
        code = u[begin+6:end]
        imagePage = "http://www.hagah.com.br/jsp/default.jspx?action=newGalleryModal&id=%s" % (code)
        d = makeTree(imagePage)
        imageLinks = d.xpath('//*[@class="listaFotos"]//a/@href')
        try:
            for link in imageLinks:
                if (link == "#"):
                    pass
                else:
                    file = requests.get(link)
                    slug = "".join(x for x in link if x.isalnum() or x == ".")
                    f = open(slug, "w")
                    f.write(file.content)
                    f.close()
                    print u, " | ", slug
        except:
            pass
    except:
        pass
