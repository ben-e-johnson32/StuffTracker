from StuffTracker import app
import unittest
import productsdb

# Much of this is taken from the Flask documentation:
# http://flask.pocoo.org/docs/0.11/testing/
# And this other tutorial I found:
# http://damyanon.net/flask-series-testing/

class StuffTrackerTestCase(unittest.TestCase):

    # Sets up the app for testing.
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    # Tests if the home page is reachable.
    def test_home_status(self):
        result = self.app.get('/')
        self.assertEquals(result.status_code, 200)


    # Tests if an object is a Product.
    def test_db_objects(self):
        obj = productsdb.GetProduct(1)
        self.assertIsInstance(obj, productsdb.Product)


if __name__ == '__main__':
    unittest.main()
