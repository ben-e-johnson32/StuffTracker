from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3 as lite
import os

os.chdir(os.path.dirname(__file__))
cwd = os.getcwd()
engine = create_engine('sqlite:////' + cwd + '/static/products.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Product(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    price = Column(Float)
    year_acquired = Column(Integer)
    location = Column(String)
    upc = Column(String)
    image = Column(String)


# This script created the database. I'm sure it'll change as I move forward.
def CreateProductsTable():
    db = lite.connect(cwd + '/static/products.db')
    cursor = db.cursor()

    cursor.execute('DROP TABLE Products')
    cursor.execute('CREATE TABLE Products(id INTEGER PRIMARY KEY,'
                   'name TEXT, desc TEXT, price REAL,'
                   'year_acquired INTEGER, location TEXT, upc CHARACTER(20) NULL,'
                   'image TEXT)')
    db.commit()
    db.close()


def EnterProduct(p):
    session = Session()
    session.add(p)
    session.commit()
    session.close()


def GetProduct(itemID):
    session = Session()
    product = session.query(Product).filter(Product.id == itemID).first()
    session.close()
    return product


def GetAllProducts():
    session = Session()
    products = []

    for p in session.query(Product).all():
        products.append(p)

    session.close()
    return products
