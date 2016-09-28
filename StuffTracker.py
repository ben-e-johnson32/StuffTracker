from flask import Flask, render_template
import products
import productsdb

app = Flask(__name__)


# Start page is currently just some stuff I did from a tutorial.
@app.route('/')
def template_test():
    return render_template("test2.html", my_string="What", my_list=[0, 1, 2, 3, 4, 5], num=11123.2)


# Read a bit about filters - decided to try one out since I could probably use it later. Took the python formatting bit
# from here: http://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
@app.template_filter()
def currencyfilter(value):
    return '${:,.2f}'.format(value)


# More stuff from tutorials.
@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello {}!'.format(name)


# Currently just a a test version of the below show_product method. /products will eventually display the products you
# have, then you'd pick one and it'd take you to the show_product page.
@app.route('/products')
def show_products():
    product = products.Product(name="Coby 32\" Television", desc="Coby's 32\" LCD TV offers a premium viewing "
                                                                 "experience, featuring brilliant picture, "
                                                                 "liquid-crystal display, and dual ATSC/NTSC tuners for"
                                                                 " great reception of digital signal (DTV-ready).",
                               price=357.02, age=6, year_acquired=2014, location="Home", upc=None, image="/static/cobytv.jpg")
    return render_template("products.html", product=product)


# Get a row from the database by its primary key. Build a Product object with the tuple that's returned,
# then render the products.html template with that Product object.
@app.route('/products/<itemID>')
def show_product(itemID):
    row = productsdb.GetProduct(itemID)
    product = products.Product(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    return render_template("products.html", product=product)


if __name__ == '__main__':
    app.run()
