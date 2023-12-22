from flask import Flask
from flask_bcrypt import Bcrypt

secret_key = 'this_is_not_a_secure_secret_key'

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = secret_key

from auth import auth_bp
from home import home_bp
from order import order_bp
from db_calls import db_read,db_write

app.register_blueprint(auth_bp,url_prefix='/authentication')
app.register_blueprint(home_bp)
app.register_blueprint(order_bp,url_prefix='/order')

is_toppings = db_read.get_pizza_toppings()
is_sizes = db_read.get_pizza_sizes() 
is_order_statuses = db_read.get_order_statuses()

if not is_toppings: 
    db_write.populate_toppings()
if not is_sizes:
    db_write.populate_sizes() 
if not is_order_statuses:
    db_write.populate_order_status()


print('Web Server Active on localhost:5555')