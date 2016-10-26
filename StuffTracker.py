from flask import Flask, render_template, request
import productsdb
import os

app = Flask(__name__)
# TODO: Make file paths cross-platform (only work in OSX)
app.config['UPLOAD_FOLDER'] = os.getcwd() + "/static/"


# Placeholder home page - just has a link to the page that shows all products and the add new product page.
@app.route('/')
def home():
    return render_template("home.html")


# Read a bit about filters - decided to try one out since I could probably use it later. Took the python formatting bit
# from here: http://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
@app.template_filter()
def currencyfilter(value):
    return '${:,.2f}'.format(value)


# Filter that rounds to one decimal place.
@app.template_filter()
def onedecimalfilter(value):
    return round(value, 1)


# This page displays all the products in your database.
@app.route('/products', methods=['GET', 'POST'])
def show_products():
    orderby = None
    if request.method == 'POST':
        orderby = request.form['orderby']
    productList = productsdb.GetAllProducts(orderby)
    return render_template("products.html", products=productList, orderby=orderby)


# The page for a particular product.
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


# A page that shows statistics about the entire inventory.
@app.route('/inventory_stats')
def show_stats():
    metadata = productsdb.GetMetadata()
    return render_template('inventory_stats.html', metadata=metadata)


# A page for editing a product.
@app.route('/products/<itemID>/edit')
def edit_product(itemID):
    p = productsdb.GetProduct(itemID)
    return render_template('edit_product.html', product=p)


# The page the user lands on after editing a product.
@app.route('/products/<itemID>/edit_successful', methods=["POST"])
def edit_successful(itemID):
    response = request.form
    # Check if the year is an integer and the price is a float. Everything else is just a string.
    if productsdb.isValidEdit(response):
        editedP = productsdb.UpdateProduct(itemID, response)
        return render_template('edit_successful.html', product=editedP)
    # If there's bad data, re-render the edit product page and display a somewhat helpful error message.
    else:
        p = productsdb.GetProduct(itemID)
        return render_template('edit_product.html', product=p, error=True)


if __name__ == '__main__':
    app.run()
