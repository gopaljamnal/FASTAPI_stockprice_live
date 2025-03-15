from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "postgresql://stock_user:password@localhost/stock_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class StockData(Base):
    __tablename__ = "stocks"
    id = Column(Integer, autoincrement=True, primary_key=True)
    symbol = Column(String, index=True, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)
