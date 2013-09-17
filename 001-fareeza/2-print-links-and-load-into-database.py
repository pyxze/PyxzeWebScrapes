import pickle

input = open("pickles/podcast_links.pickle", "rb")
podcast_links = list(pickle.load(input))
input.close()

from sqlalchemy import create_engine
engine = create_engine('sqlite:///podcasts.sqlite', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Text

class Podcast_Link(Base):
    __tablename__ = 'podcast_links'

    id = Column(Integer, primary_key=True)
    podcast_link = Column(String)

    def __init__(self, podcast_link):
        self.podcast_link = podcast_link

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

for podcast_link in podcast_links:
    print podcast_link
    podcast_link_entry = Podcast_Link(podcast_link)
    session.add(podcast_link_entry)
    session.commit()