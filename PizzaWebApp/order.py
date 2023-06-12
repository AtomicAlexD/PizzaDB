from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Markup
from db_calls import db_read, db_write 

order_bp = Blueprint('order',__name__, template_folder='templates/order')
pizza_count = int(0)

@order_bp.route('/', methods=["GET"])
def pizza_maker():
    #check user is logged in, if not send them to log in
    user_id = session.get('user_id')
    num_items_in_basket = session.get('num_items_in_basket')
    if not user_id:
        flash('please log in first', category='danger')
        return redirect(url_for('auth.log_in'))
    if request.method == "GET":
        toppings = db_read.get_pizza_toppings()
        sizes = db_read.get_pizza_sizes()
        return render_template('order_pizza.html',
                               toppings=toppings,
                               sizes=sizes,
                               user_id = user_id,
                               num_items_in_basket=num_items_in_basket)
    
@order_bp.route('/add_to_basket', methods=["POST"])
def add_to_basket():
    '''
    when user logs in, we should check for open orders and place cookie.
    when pizza placed in basket
    if cookie order_id = 0:
        generate order number & update cookie
    place order_id & size_id into order.pizza and generate new order_pizza_id
    get order_pizza_id and place in order.pizza_toppings along with topping id (1 per topping)
    '''
    user_id = session.get('user_id')
    order_id = session.get('order_id')
    num_items_in_basket = session.get('num_items_in_basket')
    if order_id == 0:
        db_write.start_new_order(user_id)
        order_id = db_read.check_open_orders(user_id)
        session['order_id'] = order_id
    order_details = request.form
    db_write.new_custom_pizza(order_id, order_details)
    num_items_in_basket = db_read.basket_count(order_id)
    session['num_items_in_basket'] = num_items_in_basket
    flash(Markup('Added to basket, <a href="'+ url_for('order.view_basket') +'">View basket</a> or continue adding pizza.'), category='success')
    return redirect(url_for('order.pizza_maker'))


@order_bp.route('/basket', methods=["GET","POST"])
def view_basket():
    user_id = session.get('user_id')
    order_id = session.get('order_id')
    num_items_in_basket = session.get('num_items_in_basket')
    basket = db_read.get_basket(user_id,order_id)
    basket_items = db_read.get_basket_items(user_id,order_id)
    if request.method == "GET":        
        return render_template('view_basket.html',
                                basket=basket,
                                basket_items = basket_items,
                                user_id=user_id,
                                num_items_in_basket=num_items_in_basket
                                )
    if request.method == "POST":
        db_write.order_the_pizza(order_id)
        session.pop('num_items_in_basket', default=0)
        session.pop('order_id', default=0)
        flash(Markup( 'Order Placed! Expected Delivery Time:<a href="https://www.dominos.co.uk/">Never.... Order some real pizza here</a>'), category='success' )
        return redirect(url_for('home.home_page'))