from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraputils import get_news

Base = declarative_base()
engine = create_engine("sqlite:///news.db")  # экз. класса Engine, отвеч. за подключение к БД
# выбираем базу данных sqlite и она будет записана в файлик news.db
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(String)
    points = Column(String)
    label = Column(String)


Base.metadata.create_all(bind=engine)

# s = session()
# news_ar = get_news('https://news.ycombinator.com/newest', n_pages=35)
# for new in news_ar:
#     news = News(title=new['title'],
#                 author=new['author'],
#                 url=new['url'],
#                 comments=new['comments'],
#                 points=new['points'])
#     s.add(news)
#     s.commit()

