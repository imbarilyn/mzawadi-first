from flask import Flask, render_template, request, session, redirect, url_for,flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "kjhfgdjkouae"
app.permanent_session_lifetime = timedelta(days=7)

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        # x = request.form
        # print(x)
        session["email"] = email
        flash("Welcome aboard")
        return redirect(url_for("index"))
    else:        
        if "email" in session:
            flash("You are logged in already!")
            return redirect(url_for("index"))
        return render_template("login.html")   

@app.route("/index")
def index():
    user = session["email"]
    if "email" in session:
        return render_template("index.html", user=user)
    else:
        return render_template("login.html")

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        session.permanent = True
        # reg = request.form
        # print(reg)
        fname = request.form["fname"]
        session["fname"] = fname
        return redirect(url_for("index"))
    else:
        return render_template("register.html")
        
        
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug = True)