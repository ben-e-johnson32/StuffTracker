from flask import Flask, render_template, request
import productsdb
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/Users/Ben/PycharmProjects/StuffTracker/static/"


# Placeholder home page - just has a link to the page that shows all products and the add new product page.
@app.route('/')
def home():
    return render_template("home.html")


# Read a bit about filters - decided to try one out since I could probably use it later. Took the python formatting bit
# from here: http://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
@app.template_filter()
def currencyfilter(value):
    return '${:,.2f}'.format(value)


# This page displays all the products in your database.
@app.route('/products')
def show_products():
    productList = productsdb.GetAllProducts()
    return render_template("products.html", products=productList)


@app.route('/products/<itemID>')
def show_product(itemID):
    product = productsdb.GetProduct(itemID)
    return render_template("product.html", product=product)


# The page where users enter new products.
@app.route('/add_product')
def add_product():
    return render_template("add_product.html")


# The method that updates the database and saves the user's image file. Got a lot of info from the documentation:
# http://flask.pocoo.org/docs/0.11/patterns/fileuploads/
# Currently saves each image as a jpg. It stores the images in the static folder and the database has the path to
# that item's image.
@app.route('/product_added', methods=['POST'])
def product_added():
    response = request.form
    newItem = productsdb.Product(name=response['product'], desc=response['description'], price=response['price'],
                                 year_acquired=response['yearAcquired'], location=response['location'],
                                 upc=response['UPC'], image="/static/" + response['imageName'] + ".jpg")
    productsdb.EnterProduct(newItem)
    file = request.files['file']
    filename = response['imageName'] + ".jpg"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("product_added.html", product=response['product'])


if __name__ == '__main__':
    app.run()
