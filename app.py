from flask import Flask, request
import json
from dbhelpers import run_statement

app = Flask(__name__)

# Restaurant POST
@app.post('/api/restaurant')
def post_restaurant():
    name = request.json.get('name')
    address = request.json.get('address')
    phone_num = request.json.get('phoneNum')
    image_url = request.json.get('image_url')
    if name == None:
        return "You must specify a Restaurant name."
    if address == None: 
        return "You must specify a Restaurant's address."
    if phone_num == None:
        return "You must specify a Restaurant's phone number."
    # I am leaving image_url out of the If statement because it is Nullable
    result = run_statement("CALL post_restaurant(?,?,?,?)", [name, address, phone_num, image_url])
    if result == None:
        return "Successfully added new Restaurant."
    elif "Duplicate entry" in result:
        return "This Restaurant has already been added, please choose a different name to register."
    else:
        return result

# Restaurant GET
@app.get('/api/restaurant')
def get_restaurants():
    result = run_statement("CALL get_restaurants()")
    if (type(result) == list):
        return json.dumps(result, default=str)
    else: 
        return "Sorry, something went wrong."

# Restaurant DELETE
@app.delete('/api/restaurant')
def delete_restaurant():
    rest_id = request.json.get('restId')
    if rest_id == None:
        return "You must specify a Restaurant's ID"
    result = run_statement("CALL delete_restaurant(?)", [rest_id])
    if result == None:
        return "Successfully deleted Restaurant."
    else:
        return "Unable to delete Restaurant {}.".format(rest_id)

# Menu POST
@app.post('/api/menu')
def post_menu_item():
    rest_id = request.json.get('restId')
    name = request.json.get('name')
    description = request.json.get('description')
    price = request.json.get('price')
    image_url = request.json.get('image_url')
    if rest_id == None:
        return "You must specify a Restaurant's ID."
    if name == None:
        return "You must specify a menu item name."
    if description == None: 
        return "You must specify a menu item description."
    if price == None:
        return "You must specify a menu item price."
    # I am leaving image_url out of the If statement because it is Nullable
    result = run_statement("CALL post_menu_item(?,?,?,?,?)", [rest_id, name, description, price, image_url])
    if result == None:
        return "Successfully added new item to menu."
    else:
        return result

app.run(debug = True)