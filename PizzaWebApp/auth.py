from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from pizza_web_app import bcrypt
from db_calls import db_read, db_write

auth_bp = Blueprint('auth',__name__, template_folder='templates/auth')

authentication_error = 'incorrect user name or password, please try again'

@auth_bp.route('/login', methods=["GET","POST"])
def log_in():
    if request.method == "POST":
        #form filled and sent, go do the work
        data = request.form
        user_name = data.get('email')
        password = data.get('password')
        user_id = db_read.get_user_id(user_name)
        if not user_id:
            #user does not exist
            flash(authentication_error,category='warning')
            return(render_template("log_in.html"))
        user_info = db_read.get_user_info(user_id)
        stored_password = user_info.password_hash
        password_check = bcrypt.check_password_hash(stored_password,password)
        if password_check == True:
            #email and password has matched, log user in
            session['user_id'] = user_id
            #check here for open basket? 
            order_id = db_read.check_open_orders(user_id)
            if not order_id: 
                session['order_id'] = 0
            else:
                session['order_id'] = order_id
                num_items_in_basket = db_read.basket_count(order_id)
                session['num_items_in_basket'] = num_items_in_basket
            return redirect(url_for('order.pizza_maker'))
        else:
            flash(authentication_error,category='warning')
            return redirect(url_for('auth.log_in'))
    elif request.method == 'GET':
        #page hit, display log in form
        return(render_template("log_in.html"))

@auth_bp.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        #form filled and sent, go do the work
        data = request.form
        email = data.get('email')
        password1 = data.get('password')
        password2 = data.get('password2')
        #first check user doesnt already exist
        account = db_read.get_user_id(email)
        if account:
            flash('you already have an account',category='danger')
            return redirect(url_for('auth.log_in'))
        #then make sure password entry is correct
        elif password1 != password2:
            flash('learn to type your passwords correctly please', category='danger')
        else:
            #lets secure this password
            pw_hash = bcrypt.generate_password_hash(password1).decode('utf-8')
            #add the details to the db
            db_write.add_new_customer(data,pw_hash)
            #send them to the log in page
            return redirect(url_for('auth.log_in'))
    elif request.method == 'GET':
        #page hit, display log in form
        return(render_template("register.html"))

@auth_bp.route('/logout', methods=["GET"])
def log_out():
    session.pop('user_id', default=None)
    session.pop('order_id', default=None)
    flash('logged out', category="success")
    return redirect(url_for('home.home_page'))