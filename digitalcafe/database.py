import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]

order_management_db = myclient["order_management"]

branches_db = myclient["branches"]

def get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code})
    return product

def get_products():
    product_list = []
    products_coll = products_db["products"]
    for p in products_coll.find({}):
        product_list.append(p)
    return product_list

def get_branch(code):
    branches_coll = branches_db["branches"]
    branches = branches_coll.find_one({"code":code})
    return branch

def get_branches():
    branch_list = []
    branches_coll = branches_db["branches"]
    for p in branches_coll.find({}):
        branch_list.append(p)
    return branch_list

def get_user(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username":username})
    return user

def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

def count_orders(username):
    orders_coll = order_management_db ['orders']
    numberoforders = []
    numberoforders = orders_coll.count ({"username": username} )
    return numberoforders

def get_orders(username):
    order_list = []
    orders_coll = order_management_db["orders"]

    for p in orders_coll.find({"username":username}):
        order_list.append(p)
    return order_list

def get_password(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username":username})
    password = user['password']
    return password

def change_db(password):
    password_coll = order_management_db['password']
    user = ({"username" : username})
    change_now = ({"$set":{"password":newpassword}})
    password_coll.find_one_and_update(username, password)
    order_management_db.update_one(username, newpassword)
    return
