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

'''Get category links.'''

if os.path.isfile("hagah-florianopolis-categorylinks.pickle"):
    input = open("hagah-florianopolis-categorylinks.pickle", "rb")
    categoryLinks = pickle.load(input)
    input.close()
else:
    categoryLinks = set()
    soup = makeSoup("http://www.hagah.com.br/sc/florianopolis/guia/")
    for i in soup(class_='node'):
        categoryLink = BeautifulSoup(str(i)).a['href']
        categoryLinks.update({categoryLink})
    output = open("hagah-florianopolis-categorylinks.pickle", "wb")
    pickle.dump(categoryLinks, output)
    output.close()

'''Process category links.'''

if os.path.isfile("hagah-florianopolis-vendorlinks.pickle"):
    input = open("hagah-florianopolis-vendorlinks.pickle", "rb")
    categoryLinks = pickle.load(input)
    input.close()
else:
    vendorLinks = set()
    for i in categoryLinks:
        '''Grab category codes and slugs from URLs.'''

        categoryCodeLocation = i.find("q=")
        categoryCode = i[categoryCodeLocation:]
        categorySlug = i[46:categoryCodeLocation-1]

        '''Get number of pages.'''
        categoryPagesLink = 'http://www.hagah.com.br/jsp/default.jspx?action=searchAjax&omit=true&state=sc&area=florianopolis&ag=guia&' + categoryCode
        soup = makeSoup(categoryPagesLink)
        pages = "1" # Minimum number of pages.
        try:
            soup = BeautifulSoup(str(soup(class_='aNormal')[0])) # Get pagination links.
            for p in soup('a'):
                page = BeautifulSoup(str(p))('a')[0].string
                try:
                    if int(page) > int(pages):
                        pages = page
                except:
                    pass
        except:
            pass

        '''Get page links.'''

        pageLinks = []

        for n in range(1,int(pages)+1): # + 1 for inclusive
            u = "http://www.hagah.com.br/sc/florianopolis/guia/%s?%s&p=%s" % (categorySlug,categoryCode,n)
            pageLinks.append(u)

        '''Get vendor links from page links.'''

        for p in pageLinks:
            print p
            soup = makeSoup(p)
            vendors = soup(class_='wrap-info-top-busca')
            for item in vendors:
                try:
                    vendorLink = BeautifulSoup(str(item)).a['href']
                    vendorLinks.update({vendorLink})
                except:
                    pass
    output = open("hagah-florianopolis-vendorlinks.pickle", "wb")
    pickle.dump(vendorLinks, output)

if os.path.isfile("hagah-florianopolis-vendorlinks.pickle"):
    input = open("hagah-florianopolis-vendorlinks.pickle", "rb")
    vendorLinks = pickle.load(input)
    vendorLinks = list(vendorLinks)
    input.close()

    '''Get vendor data.'''

    for vendorLink in vendorLinks[0:25]:
        try:
            r = requests.get(vendorLink)
            t = r.text
            d = etree.HTML(t)
            vendor = d.xpath('//*[@class="wrap-info-top-detail"]/h1/text()')[0]
            location = d.xpath('//*[@class="infoDetalhe"]//li/text()')[1]
            categories = d.xpath('//*[@class="categoriasDetalhe"]//h2/a/text()')
            address = ""
            address += d.xpath('//*[@class="infoDetalhe"]//li/a/text()')[0]
            address += d.xpath('//*[@class="infoDetalhe"]//li/text()')[0]
            address += d.xpath('//*[@class="infoDetalhe"]//li/a/text()')[1]
            phone = d.xpath('//*[@class="infoDetalhe"]//li/span/text()')[1]
            try:
                web = d.xpath('//*[@class="url"]/text()')[0]
            except:
                web = "n/a"
            print vendorLink.encode('utf-8'), " | ", location[:-2].encode('utf-8'),\
                " | ", vendor.encode('utf-8'), " | ", ", ".join(categories).encode('utf-8'), " | ",\
                address.encode('utf-8'), " | ", phone.strip(), " | ", web.encode('utf-8')
        except:
            pass