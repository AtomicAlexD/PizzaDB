#add home page here, link to log in and register 
from flask import Blueprint, render_template, request, flash, redirect, url_for, session

home_bp = Blueprint('home',__name__, template_folder='templates/home')

@home_bp.route('/')
def home_page():
    user_id = session.get('user_id')
    num_items_in_basket = session.get('num_items_in_basket')
    return render_template('home_page.html',user_id=user_id,num_items_in_basket=num_items_in_basket)

@home_bp.route('/clear_session')
def clear_session():
    session.clear()
    flash('All Clear!',category='success')
    return redirect(url_for('home.home_page'))
