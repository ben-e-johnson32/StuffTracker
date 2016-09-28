import sqlite3 as lite
import os


# This script created the database. I'm sure it'll change as I move forward.
def CreateProductsTable():
    os.chdir(os.path.dirname(__file__))
    cwd = os.getcwd()
    db = lite.connect(cwd + '/static/products.db')
    cursor = db.cursor()

    cursor.execute('DROP TABLE Products')
    cursor.execute('CREATE TABLE Products(ID INTEGER PRIMARY KEY,'
                   'Item TEXT, Description TEXT, Price REAL, Age INTEGER,'
                   'YearAcquired INTEGER, Location TEXT, UPC CHARACTER(20) NULL,'
                   'Image INTEGER)')
    db.commit()
    db.close()


# A method to add a product to the database.
def EnterProduct(p):
    data = (p.name, p.desc, p.price, p.age, p.year_acquired, p.location, p.upc, p.image)
    os.chdir(os.path.dirname(__file__))
    cwd = os.getcwd()
    db = lite.connect(cwd + '/static/products.db')
    cursor = db.cursor()

    cursor.execute('INSERT INTO Products(Item, Description, Price, Age, YearAcquired,'
                   'Location, UPC, Image) VALUES (?,?,?,?,?,?,?,?)', data)
    db.commit()
    db.close()


# A method to retrieve one product from the database. Returns a tuple of each value in the row matching the itemID.
def GetProduct(itemID):
    os.chdir(os.path.dirname(__file__))
    cwd = os.getcwd()
    db = lite.connect(cwd + '/static/products.db')
    cursor = db.cursor()

    cursor.execute('SELECT * FROM PRODUCTS WHERE ID = (?)', (itemID,))
    item = cursor.fetchone()
    db.close()
    print(item)
    return item


# p = products.Product(name="Macbook Pro", desc="This laptop looks just like a TV.", price=1200.50, age=7,
#                      year_acquired=2009, location="Home", upc=None, image="/static/cobytv.jpg")
# EnterProduct(p)
# CreateProductsTable()
# GetProduct(2)