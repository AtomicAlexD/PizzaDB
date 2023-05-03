from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Markup
from db_read import get_pizza_sizes, get_pizza_toppings
from db_write import new_custom_pizza

order_bp = Blueprint('order',__name__, template_folder='templates/order')
pizza_count = 0

@order_bp.route('/', methods=["GET","POST"])
def pizza_maker():
    global pizza_count
    #check user is logged in, if not send them to log in
    user_id = session.get('user_id')
    if not user_id:
        flash('please log in first', category='danger')
        return redirect(url_for('auth.log_in'))
    if request.method == "GET":
        toppings = get_pizza_toppings()
        sizes = get_pizza_sizes()
        return render_template('order_pizza.html',
                               toppings=toppings,
                               sizes=sizes,
                               user_id = user_id)
    elif request.method == "POST":
        order_details = request.form
        if 'basket' not in session:
            session['basket'] = {}
        basket = session['basket']
        if user_id not in basket: 
            basket[user_id] = {}
        user_basket = basket[user_id]
        user_basket[f'pizza_{str(pizza_count)}'] = order_details
        basket[user_id] = user_basket
        session['basket'] = basket
        print(session['basket'])
        pizza_count += 1
        flash(Markup('Added to basket, <a href="' + url_for('order.view_basket') + '">View basket</a> or continue adding pizza.'), category='success')
        return redirect(url_for('order.pizza_maker'))
    
@order_bp.route('/basket', methods=["GET","POST"])
def view_basket():
    if request.method == "GET":        
        user_id = session.get('user_id')
        print(user_id)
        basket = session.get('basket',{})
        print(basket)
        user_basket = session.get('user_basket',{})
        print(user_basket)
        return render_template('view_basket.html', pizzas = basket)
