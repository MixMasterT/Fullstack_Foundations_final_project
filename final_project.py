from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup_final_project import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurant_menu_final_project.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
sesh = DBSession()

app = Flask(__name__)

@app.route('/')
def allRestaurants():
    restaurants = sesh.query(Restaurant).all()
    return render_template("root.html",restaurants = restaurants)

@app.route('/new_restaurant/', methods=['GET','POST'])
def addRestaurant():
    if request.method == 'POST': #handle form
        if request.form['restaurant_name']:
            restaurant = Restaurant(name = request.form['restaurant_name'], address = request.form['restaurant_address'] or 'none', phone = request.form['restaurant_phone'] or 'none')
            sesh.add(restaurant)
            sesh.commit()
            flash('Restaurant "' + restaurant.name + '" has been added to database.')
            return redirect(url_for('allRestaurants'))
        else:
            return "The name field is required!!!"

    else: #must be a 'GET' request
        return render_template('addRestaurant.html')

@app.route('/<int:restaurant_id>/edit_restaurant/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    restaurant = sesh.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST': #handle form
        if request.form['restaurant_name']:
            restaurant.name = request.form['restaurant_name']
            restaurant.address = request.form['restaurant_address'] or 'none'
            restaurant.phone = request.form['restaurant_phone'] or 'none'
            sesh.add(restaurant)
            sesh.commit()
            flash('The details for "' + restaurant.name + '" have been updated.')
            return redirect(url_for('allRestaurants'))
        else:
            return "The name field is required!!!"

    else: #must be a 'GET' request
        return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/<int:restaurant_id>/delete_restaurant/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = sesh.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST': #handle form
        sesh.delete(restaurant)
        sesh.commit()
        flash(restaurant.name + " has been deleted from the database.")
        return redirect(url_for('allRestaurants'))
    else: #must be a 'GET' request
        return render_template('deleteRestaurant.html', restaurant = restaurant)
@app.route('/<int:restaurant_id>/view_menu/')
def viewMenu(restaurant_id):
    restaurant = sesh.query(Restaurant).filter_by(id = restaurant_id).one()
    items = sesh.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template("viewMenu.html", restaurant = restaurant, items = items)

@app.route('/<int:restaurant_id>/add_menu_item/', methods=['GET','POST'])
def addMenuItem(restaurant_id):
    restaurant = sesh.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['item_name']:
            item = MenuItem(name = request.form['item_name'], price = request.form['item_price'] or 'none', course = request.form['item_course'] or 'none', description = request.form['item_description'] or 'none', restaurant_id = restaurant.id)
            sesh.add(item)
            sesh.commit()
            flash(item.name + " has been added to the menu for " + restaurant.name + ".")
            return redirect(url_for('viewMenu', restaurant_id = restaurant.id))
        else:
            return "The name field is required!!!"

    else: #must be a 'GET' request
        return render_template('addMenuItem.html', restaurant = restaurant)

@app.route('/<int:menu_item_id>/edit_menu_item/', methods = ['GET','POST'])
def editMenuItem(menu_item_id):
    item = sesh.query(MenuItem).filter_by(id = menu_item_id).one()
    restaurant = sesh.query(Restaurant).filter_by(id = item.restaurant_id).one()
    if request.method == 'POST':
        if request.form['item_name']:
            item.name = request.form['item_name']
            item.price = request.form['item_price'] or 'none'
            item.course = request.form['item_course'] or 'none'
            item.description = request.form['item_description'] or 'none'
            item.restaurant_id = restaurant.id
            sesh.add(item)
            sesh.commit()
            flash(item.name + " has been updated in the database.")
            return redirect(url_for('viewMenu', restaurant_id = restaurant.id))
        else:
            return "The name field is required!!!"

    else: #must be a 'GET' request
        return render_template('editMenuItem.html', item = item, restaurant = restaurant)

@app.route('/<int:menu_item_id>/delete_menu_item/', methods = ['GET', 'POST'])
def deleteMenuItem(menu_item_id):
    item = sesh.query(MenuItem).filter_by(id = menu_item_id).one()
    restaurant = sesh.query(Restaurant).filter_by(id = item.restaurant_id).one()
    if request.method == 'POST': #delete the item
        sesh.delete(item)
        sesh.commit()
        flash(item.name + " has been deleted from the menu for " + restaurant.name)
        return redirect(url_for('viewMenu', restaurant_id = restaurant.id))

    else: #must be a 'GET' request
        return render_template('deleteMenuItem.html', item = item, restaurant = restaurant)

@app.route('/restaurants/JSON/')
def serializeAllRestaurants():
    all_restaurants = sesh.query(Restaurant).all()
    returnVal = {}
    for r in all_restaurants:
        returnVal[r.name] = r.serialize
    return jsonify(returnVal)

@app.route('/<int:restaurant_id>/menu/JSON/')
def serializeMenu(restaurant_id):
    restaurant = sesh.query(Restaurant).filter_by(id = restaurant_id).one()
    items = sesh.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    returnVal = {'restaurant':restaurant.name}
    for i in items:
        returnVal[i.name] = i.serialize
    return jsonify(returnVal)

@app.route('/<int:menu_item_id>/menu_item/JSON/')
def serializeItem(menu_item_id):
    item = sesh.query(MenuItem).filter_by(id = menu_item_id).one()
    restaurant = sesh.query(Restaurant).filter_by(id = item.restaurant_id).one()
    returnVal = {'restaurant':restaurant.name}
    returnVal[item.name] = item.serialize
    return jsonify(returnVal)

if __name__ == '__main__':
    app.secret_key = "fJVU12234JCJ205*(jg;sgjf)"
    app.debug = True
    app.run(host= '0.0.0.0', port=5000)
