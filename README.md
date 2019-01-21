# Shopify Backend Developer Intern Summer 2019 Challenge for Henry Xu

**Dependencies: Please have these setup before running the python script with the server side web api**

**Please also have python 3 set up**
```
virtualenv flask
pip3 install flask
pip3 install flask-httpauth
pip3 install flask-restful
```

**Download the python script in this repo, and run the following command on 1 terminal with the above dependencies set up: This will start the server on localhost:5000**
```
python shopify_backend.py
```
**After the server has been started, open up a new terminal and run these commands for each functionality:**

Note that the **?inventory_check** is the optional argument for whether to return items with 0 inventory

**Product general lookup that returns all products:**
```
curl localhost:5000/product_lookup/
curl localhost:5000/product_lookup/?inventory_check
```
**Product specific lookup for 1 element with title specified:**
**Replace the 'Strawberry' with the product title you want to search for**
```
curl localhost:5000/product_lookup/Strawberry/
curl localhost:5000/product_lookup/Strawberry/?inventory_check
```

**In terms of bunus features, I implemented "Shopping cart system" as well as making the API secure with user login authentification. Security feature with login username and password requirement only enabled for purchase items and complete cart. Use the command "with security feature implemented".**

**Note: replace the '5' with the amount you want to set, and replace the 'Strawberry' with the product you want for all following commands**

**Purchase without login info (will return no authentification from system): Need to specify amount to be purchased. The product type for chase is specified at the end of the URL**

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"purchase_amount":5}' http://localhost:5000/product_purchase/Strawberry/
```

**with security features implemented:**
```
curl -u Henry:Xu -i -H "Content-Type: application/json" -X PUT -d '{"purchase_amount":5}' http://localhost:5000/product_purchase/Strawberry/
```

**Add to cart:**
```
curl -i -H "Content-Type: application/json" -X PUT -d '{"purchase_amount":5}' http://localhost:5000/add_to_cart/Strawberry/
```
**Delete from cart:**
```
curl -i -H "Content-Type: application/json" -X PUT -d '{"delete_amount":5}' http://localhost:5000/delete_from_cart/Strawberry/
```
**Complete cart without login info (will return no authentification from system):**
```
curl -i -H "Content-Type: application/json" -X PUT http://localhost:5000/complete_cart/
```
**with security feature implemented:**
```
curl -u Henry:Xu -i -H "Content-Type: application/json" -X PUT http://localhost:5000/complete_cart/
```
**The current test data include the following, with title, price, and inventory count of data. I did not set up a database as the focus of this task to be able to handle all the requests, and the data that I made are sufficient for this project.**
```
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
```
