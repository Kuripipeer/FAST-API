from config.database import Base
from sqlalchemy import Column, Integer, String

class Computer(Base):
    __tablename__ = "computers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String)
    model = Column(String)
    color = Column(String)
    ram = Column(Integer)
    storage = Column(Integer)