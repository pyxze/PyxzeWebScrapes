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

from sqlalchemy import create_engine
engine = create_engine('sqlite:///podcasts.sqlite', echo=False)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Text

class Podcast(Base):
    __tablename__ = 'podcasts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    subtitle = Column(String)
    description = Column(Text)
    podcast_link = Column(String)
    episode_title = Column(String)
    episode_description = Column(Text)
    episode_date = Column(String)
    episode_url = Column(String)
    def __init__(self, title, subtitle, description, podcast_link, episode_title, episode_description, episode_date, episode_url):
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.podcast_link = podcast_link
        self.episode_title = episode_title
        self.episode_description = episode_description
        self.episode_date = episode_date
        self.episode_url = episode_url

class Podcast_Link(Base):
    __tablename__ = 'podcast_links'
    id = Column(Integer, primary_key=True)
    podcast_link = Column(String)

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

while session.query(Podcast_Link).count() > 0:
    print session.query(Podcast_Link).count()
    row = session.query(Podcast_Link).first()
    d = pickleTree(row.podcast_link)
    title = "n/a"
    subtitle = "n/a"
    try:
        title = d.xpath('//*[@id="title"]/div[1]/h1/text()')[0]
    except:
        pass
    try:
        subtitle = d.xpath('//*[@id="title"]/div[1]/h2/text()')[0]
    except:
        pass
    try:
        description = d.xpath('//*[@id="content"]/div/div[2]/div[1]/p/text()')[0]
    except:
        description = "n/a"
    try:
        number_of_episodes = d.xpath('//*[@class="tracklist-content-box"]//tbody//tr').__len__()
        if number_of_episodes == 0:
            number_of_episodes = 1
    except:
        number_of_episodes = 1
    for i in range(1,number_of_episodes + 1):
        episode_title = "n/a"
        episode_description = "n/a"
        episode_date = "n/a"
        episode_url = "n/a"
        try:
            episode_title = d.xpath('//*[@class="tracklist-content-box"]//tbody//tr[%s]/td[2]/span/span/text()' % i)[0]
        except:
            pass
        try:
            episode_description = d.xpath('//*[@class="tracklist-content-box"]//tbody//tr[%s]/td[3]/span/span/text()' % i)[0]
        except:
            pass
        try:
            episode_date = d.xpath('//*[@class="tracklist-content-box"]//tbody//tr[%s]/td[4]/span/span/text()' % i)[0]
        except:
            pass
        try:
            episode_url = d.xpath('//*[@class="tracklist-content-box"]//tbody//tr[%s]' % i)[0].attrib["audio-preview-url"].replace('www.podtrac.com/pts/redirect.mp3/', '')
        except:
            pass
        podcast = Podcast(title, subtitle, description, row.podcast_link, episode_title, episode_description, episode_date, episode_url)
        session.add(podcast)
    session.commit()
    session.delete(row)
    session.commit()