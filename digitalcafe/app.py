from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

navbar = """
    <a href='/'> Home </a> | <a href='/products'> Products </a> | <a href='/branches'> Branches </a> | <a href='/aboutus'> AboutUs </a>
    <p/>
    """

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))
    print(branches)
    return render_template('branchdetails.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route( '/login' , methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route( '/auth' , methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username,password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/loginerror')

@app.route('/loginerror')
def loginerror():
    return render_template('loginerror.html', page="Loginerror")

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/addtocart' , methods=['GET', 'POST'])
def addtocart():
    code = request.form.get('code', '')
    product = db.get_product(int(code))
    quantity = request.form.get('quantity')
    item=dict()
    # A click to add a product translates to a quantity of 1

    item["qty"] = int(quantity)
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/clearcart')
def clearcart():
    del session["cart"]
    return redirect('/cart')

def removeitem():
    code = request.form.get('code', '')
    product = db.get_product(int(code))
    quantity = request.form.get('quantity')
    item=dict()

    if request_type == "Remove":
        del cart[code]

    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/formsubmission', methods = ['POST'])
def form_submission():
    qty = request.form.getlist("qty")
    return render_template('formsubmission.html',qty=qty)

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route('/orderhistory')
def orderhistory():
    user = session["user"]
    username = user["username"]

    arethereorders = om.check_user(username)

    if arethereorders == True:
        order_list = db.get_orders(username)
        return render_template('orderhistory.html', page="Orders", order_list=order_list)

    else:
        return render_template('orderempty.html')

@app.route('/changepassword', methods = ['GET', 'POST'])
def changepassword():
    oldpassword = request.form.get("oldpassword")
    newpassword = request.form.get("newpassword")
    renewpassword = request.form.get("renewpassword")
    user = session["user"]
    username = user["username"]
    password = db.get_password(username)

    if oldpassword == password and newpassword == renewpassword:
        changepassword = db.change_db(password)
        change_message = "Password update successful"
        return render_template('changepassword.html')

    elif oldpassword != password:
        change_message = "Wrong password"
        return render_template('changepassword.html')

    else:
        change_message = "New passwords do no match!"
        return render_template('changepassword.html')
