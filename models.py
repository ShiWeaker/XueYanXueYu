from datetime import datetime
#import pytz

from sqlalchemy import Column, Integer, String, DateTime
from db import Base

#tz = pytz.timezone('PRC')


class Sayings(Base):
    __tablename__ = 'sayings'
    id = Column(Integer, primary_key=True)
    saying = Column(String(500), unique=False)
    likes = Column(Integer, unique=False)
    info = Column(String(5000), unique=False)
    datetime = Column(DateTime, unique=False)
    uid = Column(String(128), unique=False)

    def __init__(self, saying=None, likes=0, info=None, uid=None):
        self.saying = saying
        self.likes = likes
        self.info = info
        self.datetime = datetime.utcnow()
        self.uid = uid

    def __repr__(self):
        return '<Sayings %r>' % self.saying

