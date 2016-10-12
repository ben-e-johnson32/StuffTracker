from sqlalchemy import create_engine, Column, Integer, String, Float, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3 as lite
import os

os.chdir(os.path.dirname(__file__))
cwd = os.getcwd()
engine = create_engine('sqlite:////' + cwd + '/static/products.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


# The Product class using SQLAlchemy. Maps the columns of the table to the variables of the object.
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


# Add a product object to the database.
def EnterProduct(p):
    session = Session()
    session.add(p)
    session.commit()
    session.close()


# Get one product from the database based on its ID.
def GetProduct(itemID):
    session = Session()
    product = session.query(Product).filter(Product.id == itemID).first()
    session.close()
    return product


# Get all products from the database in the order chosen.
def GetAllProducts(orderby):
    session = Session()
    products = []
    # A big if/else to determine the order of the product list that's returned.
    if orderby is None:
        for p in session.query(Product).all():
            products.append(p)
        session.close()
        return products
    elif orderby == 'value':
        for p in session.query(Product).order_by(desc(Product.price)):
            products.append(p)
        session.close()
        return products
    elif orderby == 'alphabetical':
        for p in session.query(Product).order_by(Product.name):
            products.append(p)
        session.close()
        return products
    elif orderby == 'location':
        for p in session.query(Product).order_by(Product.location):
            products.append(p)
        session.close()
        return products
    elif orderby == 'newest':
        for p in session.query(Product).order_by(desc(Product.year_acquired)):
            products.append(p)
        session.close()
        return products
    elif orderby == 'oldest':
        for p in session.query(Product).order_by(Product.year_acquired):
            products.append(p)
        session.close()
        return products