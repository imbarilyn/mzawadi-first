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



@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        # x = request.form
        # print(x)
        email = request.form["email"]
        session["email"] = email        
        password = request.form.get("password")
        if len(email) < 12:
            flash("Email to short") 
        elif len(password) < 8:      
            flash("Password too short")
        else:
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
        reg = request.form
        print(reg)
        email = request.form["email"]
        session["email"] = email
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        password = request.form.get("password")
        email_address = request.form.get("email")
        confirm_password = request.form.get("confirmPassword")
        if len(first_name) <= 1:
            flash("please enter more than one character", category="error")
        elif len(last_name) < 1:
            flash("please enter more than one character", category="error")
        elif len(email_address) < 8:
          flash("Email too short")        
        elif password != confirm_password:
            flash("Password don't match", category="error")
        elif len(password) <  8:
            flash("Password is too short!", category="error")
        else:        
            return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug = True)