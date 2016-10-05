from flask import Flask, render_template, request
import products
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
# (not currently being used, but only because the database currently contains some garbage data that will make it crash)
@app.template_filter()
def currencyfilter(value):
    return '${:,.2f}'.format(value)


# This page displays all the products in your database.
@app.route('/products')
def show_products():
    # Get a list of rows from the database.
    rows = productsdb.GetAllProducts()
    # Initialize a dictionary for the primary key and product objects.
    productList = {}
    # Loop through the rows from the database and rebuild them into objects, storing them in the dictionary.
    for x in range(len(rows)):
        product = products.Product(rows[x][1], rows[x][2], rows[x][3], rows[x][4], rows[x][5],
                                   rows[x][6], rows[x][7], rows[x][8])
        entry = { x + 1: product }
        productList.update(entry)
    # Render the template with the dictionary of products.
    return render_template("products.html", products=productList)


# Get a row from the database by its primary key. Build a Product object with the tuple that's returned,
# then render the products.html template with that Product object.
@app.route('/products/<itemID>')
def show_product(itemID):
    row = productsdb.GetProduct(itemID)
    product = products.Product(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

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
    newItem = products.Product(response['product'], response['description'], response['price'],
                               response['age'], response['yearAcquired'], response['location'],
                               response['UPC'], "/static/" + response['imageName'] + ".jpg")
    productsdb.EnterProduct(newItem)
    file = request.files['file']
    filename = response['imageName'] + ".jpg"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("product_added.html", product=response['product'])


if __name__ == '__main__':
    app.run()
