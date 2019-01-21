
from flask import Flask, jsonify, abort, make_response, request # for general flask
from flask_restful import reqparse # for parsing optional argument on inventory check
from flask_httpauth import HTTPBasicAuth # for setting up authentification
auth = HTTPBasicAuth()

app = Flask(__name__)

# products and specifications inside the database. Currently set as a list of dictionaries
products = [
    {
        'id': 1,
        'title': 'Chocolate',
        'price': 5.0, 
        'inventory_count': 0
    },
    {
        'id': 2,
        'title': 'Strawberry',
        'price': 7.5,
        'inventory_count': 35
    }
]

# shopping cart items
shopping_cart = {}
shopping_cart["Current items:"] = {}
shopping_cart["Total price"] = 0 

@app.route('/product_lookup/', methods = ['GET'])
def get_products():

    #check if the optional argument of "inventory_check" is included in the request
    parser = reqparse.RequestParser()
    parser.add_argument('inventory_check', store_missing=False)
    args = parser.parse_args()

    #only include products with inventory left
    if 'inventory_check' in args:
        valid_products = []
        for existing_product in products:
            if existing_product['inventory_count'] > 0:
                valid_products.append(existing_product)

        return jsonify({'Current products': valid_products})

    else:
        return jsonify({'Current products': products})



@app.route('/product_lookup/<string:product_title>/', methods = ['GET'])
def get_product(product_title):

    #check if the optional argument of "inventory_check" is included in the request
    parser = reqparse.RequestParser()
    parser.add_argument('inventory_check', store_missing=False)
    args = parser.parse_args()

    #if optional argument is included, check for inventory and title of product
    if 'inventory_check' in args:
        valid_products = []
        for existing_product in products:
            if existing_product['inventory_count'] > 0 and existing_product['title'] == product_title:
                valid_products.append(existing_product)

        if len(valid_products) == 0:
            return jsonify("No matching product found that has inventory left")
            # abort(404)
        else:
            return jsonify({'Current products': valid_products[0]})

    #if optional argument is not included, only check for title of product
    else:
        valid_products = []
        for existing_product in products:
            if existing_product['title'] == product_title:
                valid_products.append(existing_product)

        if len(valid_products) == 0:
            return jsonify("No matching product found")

        # if optional arguments not included
        else: 
            return jsonify({'Current products': valid_products[0]})



#PUT request for purchasing products as it involves modifying the data
@app.route('/product_purchase/<string:product_title>/', methods = ['PUT'])
@auth.login_required #authenticatio required
def purchase_product(product_title):

    purchase_amount = int(request.json.get('purchase_amount'))
    #check for inventory and name matching with query
    valid_products = []
    for existing_product in products:
        if existing_product['inventory_count'] >= purchase_amount and existing_product['title'] == product_title:
            valid_products.append(existing_product)

    # no valid products
    if len(valid_products) == 0:
        return jsonify("The product is either not found, sold out, or does not have enough inventory left for the amount to be purchased")

    # modify the inventory value after the product has been purchased
    valid_products[0]['inventory_count'] = valid_products[0]['inventory_count'] - purchase_amount
    return jsonify({'updated inventory': products})



#PUT request for purchasing products as it involves modifying the data
@app.route('/add_to_cart/<string:product_title>/', methods = ['PUT'])
def add_product_to_cart(product_title):

    purchase_amount = int(request.json.get('purchase_amount'))
    #check for inventory and name matching with query
    valid_products = []
    for existing_product in products:
        if existing_product['title'] == product_title:
            # if already exists, check if cart amount + new amount <= inventory amount
            if product_title in shopping_cart["Current items:"]:
                if shopping_cart["Current items:"][product_title] + purchase_amount <= existing_product['inventory_count']:
                    valid_products.append(existing_product)
            # if not in cart, check if new purchase amount <= inventory amount
            else:
                if existing_product['inventory_count'] >= purchase_amount:
                    valid_products.append(existing_product)
            
    # no valid products
    if len(valid_products) == 0:
        return jsonify("The product is either not found, sold out, or does not have enough inventory left for the amount to be purchased")

    # if the product already exists in cart
    if valid_products[0]['title'] in shopping_cart["Current items:"]:
        shopping_cart["Current items:"][valid_products[0]['title']] += purchase_amount
        shopping_cart["Total price"] += purchase_amount*valid_products[0]['price']

    # if product not in cart, initialize
    else:
        shopping_cart["Current items:"][valid_products[0]['title']] = 0
        shopping_cart["Current items:"][valid_products[0]['title']] += purchase_amount
        shopping_cart["Total price"] += purchase_amount*valid_products[0]['price']

    # modify the cart value only, do not modify the inventory
    return jsonify({'updated cart': shopping_cart})



@app.route('/delete_from_cart/<string:product_title>/', methods = ['PUT'])
def delete_product_from_cart(product_title):

    delete_amount = int(request.json.get('delete_amount'))
    #check for inventory and name matching with query
    valid_products = []
    for existing_product in products:
        if existing_product['title'] == product_title:
            # check if amount in cart is greater than the amount to be deleted
            if product_title in shopping_cart["Current items:"]:
                if shopping_cart["Current items:"][product_title] >= delete_amount:
                    valid_products.append(existing_product)
        
    # check for valid products
    if len(valid_products) == 0:
        return jsonify("The product is either not found or not enough in the cart to be deleted")

    # delete from cart if pass all the conditions
    if valid_products[0]['title'] in shopping_cart["Current items:"]:

        shopping_cart["Current items:"][valid_products[0]['title']] -= delete_amount
        shopping_cart["Total price"] -= delete_amount*valid_products[0]['price']
    
    # return the cart for user to see
    return jsonify({'updated cart': shopping_cart})



# complete the cart, and update inventory with PUT request
@app.route('/complete_cart/', methods = ['PUT'])
@auth.login_required # authentification required
def complete_cart():

    # check if cart already empty
    if int(shopping_cart["Total price"]) == 0:
        return jsonify("Shopping cart is empty, nothing to complete")

    #update the cart info
    for cart_items_key, cart_items_value in shopping_cart["Current items:"].items():
        for individual_product in products:
            if individual_product['title'] == cart_items_key:
                individual_product['inventory_count'] -= int(cart_items_value)
                shopping_cart["Total price"] -= int(cart_items_value)*individual_product['price']
                shopping_cart["Current items:"][cart_items_key] = 0

    # return all cart and inventory info
    return jsonify({'updated products inventory': products, 'updated cart': shopping_cart})


# set up authentification
# User name has to be Henry
# Password has to be Xu
@auth.get_password
def get_password(username):
    if username == 'Henry':
        return 'Xu'
    return None

# if no correct login provided
@auth.error_handler
def unauthorized_access():
    return make_response(jsonify({'error': 'unauthorized_access'}))

# run app in debug mode for better output structure
if __name__ == '__main__':
    app.run(debug=True)