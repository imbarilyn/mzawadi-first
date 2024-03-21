from flask import Flask, render_template, request, session, redirect, url_for,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "kjhfgdjkouae"
app.permanent_session_lifetime = timedelta(days=7)
login_manager = LoginManager()


#creating the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb.sqlite3 '
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager.init_app(app)

class User(db.Model):
    _id  = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirmPassword = db.Column(db.String(100), nullable=False)
    
    def __init__(self, fname, lname, email, password, confirmPassword):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.confirm_password = confirmPassword


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        # x = request.form
        # print(x)
        email = request.form.get("email")      
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session["email"] = email
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password", category="error")
    elif "email" in session:
        flash("You are logged in already!")
        return redirect(url_for("index"))
    return render_template("login.html")
     

@app.route("/index")
def index():
    user = session["email"]
    if "email" in session:
        return render_template("index.html", user = user)
    else:
        return render_template("login.html")

@app.route("/register", methods=["POST","GET"])
def register():
    
    email = request.form.get("email")
    session["email"] = email
    # print(session["email"])
    fname= request.form.get("fname")
    lname= request.form.get("lname")
    password = request.form.get("password")
    email = request.form.get("email")
    confirmPassword = request.form.get("confirmPassword")
    if request.method == "POST":
        # session.permanent = True
        # user = request.form
        # print(user)   
        if len(fname) <= 1:
            flash("please enter more than one character", category="error")
        elif len(lname) < 1:
            flash("please enter more than one character", category="error")
        elif len(email) < 8:
          flash("Email too short") 
        elif len(password) <  8:
            flash("Password is too short!", category="error")       
        elif password != confirmPassword:
            flash("Password don't match", category="error")        
        else:
            usr = User(fname=fname,
                       lname=lname, 
                       email=email, 
                       password=password, 
                       confirmPassword=confirmPassword
                       )
            create_user =  User.query.filter_by(email = email).count()
            if create_user > 1:
                flash("Account already exists! Kindly create account")                
                return render_template("register.html")
            else:
                db.session.add(usr)
                db.session.commit()
                return redirect(url_for("index"))            
            return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()        
    app.run(debug = True)