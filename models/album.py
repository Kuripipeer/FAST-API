from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    genre = Column(String)