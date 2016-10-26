from sqlalchemy import create_engine, Column, Integer, String, Float, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3 as lite
import os
from datetime import datetime

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


# For a future page with data about all the items you've entered. Keeps track of totals and averages.
# Also gives a list of all outstanding products so they can be displayed on the stats page too.
def GetMetadata():
    session = Session()
    metadata = {}
    total_count = 0
    count_outstanding = 0
    value_outstanding = 0
    outstanding_items_list = []
    total_value = 0.0
    total_age = 0

    # Loop through all products in the database and update counts and totals.
    for p in session.query(Product).all():
        total_count += 1
        if p.location != "Home":
            count_outstanding += 1
            value_outstanding += p.price
            outstanding_items_list.append(p)
        total_value += p.price
        total_age += datetime.now().year - p.year_acquired

    session.close()

    # Calculate averages.
    average_age = total_age / total_count
    average_value = total_value / total_count

    # Create a bunch of dict entries with the data we have.
    dict_values = [{'Number of Items': total_count}, {'Items Outstanding': count_outstanding},
                   {'Value Outstanding': value_outstanding}, {'Total Value': total_value},
                   {'Average Value': average_value}, {'Average Age': average_age},
                   {'Outstanding Items List': outstanding_items_list}]

    # Put the dict entries in the dictionary then return it.
    for value in dict_values:
        metadata.update(value)

    return metadata


# A method for updating the product. Currently goes through and updates all columns even if they were unchanged.
def UpdateProduct(itemID, response):
    session = Session()

    for k, v in response.items():
        session.query(Product).filter_by(id=itemID).update({k: v})

    session.commit()
    product = GetProduct(itemID)
    session.close()

    return product


# A method to make sure the year and price values are in the right format.
def isValidEdit(p):
    try:
        p = dict(p)
        int(p['year_acquired'][0])
        float(p['price'][0])
        return True
    except ValueError:
        return False
