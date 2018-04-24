from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost", user="root", password="allahpleasehelpme", db="bookit_db")


@app.route("/")
def index():
    return render_template("index.html", title="SignUP")


@app.route("/signUp", methods=["POST"])
def signUp():
    username = str(request.form["user"])
    password = str(request.form["password"])
    email = str(request.form["email"])
    location = "nai"

    cursor = conn.cursor()

    cursor.execute("INSERT INTO user (email,password,username,location)VALUES(%s,%s,%s,%s)", (username, password, email,location))
    conn.commit()
    return redirect(url_for("home"))




@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)