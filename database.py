from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship
from config import DSN


engine = create_async_engine(DSN)
Base = declarative_base(bind=engine)


# class UserAds(Base):
#     __tablename__ = "user_ads"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String, unique=True, nullable=False, index=True)
#     password = Column(String, nullable=False)
#     token = Column(String, unique=True, nullable=True)

class Ads(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    desc = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # id_user = Column(Integer, ForeignKey("user_ads.id"), nullable=False)
    #
    # user_ads = relationship(UserAds, backref="ads")

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
