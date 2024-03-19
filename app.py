from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")





if __name__ == "__main__":
    app.run(debug = True)