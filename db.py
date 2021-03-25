from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:postgres@postgres_db_container/rss_feed_cache", echo=True)
Base = declarative_base()

make_session = sessionmaker(bind=engine)


class RssFeedCache(Base):
    __tablename__ = "rss_feed_cache"

    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    snapshot = Column(JSON)
