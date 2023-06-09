from flask import Flask
from flask_bcrypt import Bcrypt

secret_key = 'this_is_not_a_secure_secret_key'

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = secret_key

from auth import auth_bp
from home import home_bp
from order import order_bp
from db_read import get_pizza_sizes,get_pizza_toppings, get_order_statuses
from db_write import populate_toppings,populate_sizes, populate_order_status

app.register_blueprint(auth_bp,url_prefix='/authentication')
app.register_blueprint(home_bp)
app.register_blueprint(order_bp,url_prefix='/order')

is_toppings = get_pizza_toppings()
is_sizes = get_pizza_sizes() 
is_order_statuses = get_order_statuses()

if not is_toppings: 
    populate_toppings()
if not is_sizes:
    populate_sizes() 
if not is_order_statuses:
    populate_order_status()


print('Web Server Active on localhost:5555')