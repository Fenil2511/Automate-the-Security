#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
from config import USERS  # Import users from config

app = Flask(__name__)

# Home Route - Displays Login Page
@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")

# Login Route - Processes Login Form
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if credentials are correct
    if username in USERS and USERS[username] == password:
        return redirect(url_for("success"))
    else:
        return render_template("login.html", error="Invalid credentials. Please try again.")

# Success Route - Displayed on Successful Login
@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
