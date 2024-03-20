from flask import Flask, render_template, request, session, redirect, url_for,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "kjhfgdjkouae"
app.permanent_session_lifetime = timedelta(days=7)

#creating the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3 '
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id  = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    confirmPassword = db.Column(db.String(100))
    
    def __init__(self, fname, lname, email, password, confirmPassword):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.confirm_password = confirmPassword

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        # x = request.form
        # print(x)
        email = request.form["email"]
        # session["email"] = email        
        password = request.form.get("password")
        if len(email) < 12:
            flash("Email to short") 
        elif len(password) < 8:      
            flash("Password too short")
        else:
            user = users.query.filter_by(name=email).first()
            if user and user.password == password:
                session["email"] = email
                return redirect(url_for("index"))
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
    if request.method == "POST":
        session.permanent = True
        # user = request.form
        # print(user)
        email = request.form["email"]
        session["email"] = email
        # print(session["email"])
        fname= request.form.get("fname")
        lname= request.form.get("lname")
        password = request.form.get("password")
        email = request.form.get("email")
        confirmPassword = request.form.get("confirmPassword")
        if len(fname) <= 1:
            flash("please enter more than one character", category="error")
        elif len(lname) < 1:
            flash("please enter more than one character", category="error")
        elif len(email) < 8:
          flash("Email too short")        
        elif password != confirmPassword:
            flash("Password don't match", category="error")
        elif len(password) <  8:
            flash("Password is too short!", category="error")
        else:
            user = request.form
            usr = users(user)
            email = usr.email
            if users.query.filter_by(name = email).all().count() > 0:
                flash("Account already exists!")
            else:                            
                db.session.add(usr)
                db.session.commit()
                return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)