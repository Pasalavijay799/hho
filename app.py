from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, secrets
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
import traceback
import logging


db = SQL("sqlite:///database.db")

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    data = db.execute("SELECT * FROM users")
    check_data = dict()
    check_data["usernames"] = []
    check_data["mails"] = []
    check_data["id_nos"] = []
    for row in data:
        check_data["usernames"].append(row["username"])
        check_data["mails"].append(row["mail"])

    if request.method == 'POST':
        username = request.form['username']
        id_no = request.form['id_no']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mobile = request.form['mobile']
        designation = request.form['designation']
        confirm_password = request.form['confirm_password']

        if username in check_data["usernames"]:
            error = "Username already exists"
        elif password != confirm_password:
            error = "password does not match"
        elif email in check_data["mails"]:
            error = "Mail already exists" 
        elif id_no in check_data["id_nos"]:
            error = "ID No already exists" 
        else:
            try:
                password = generate_password_hash(password)
                db.execute("INSERT INTO users (username, id_no, first_name, last_name, designation, mobile, mail, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", username, id_no, first_name, last_name, designation, mobile, email, password)
                flash('You are successfully signed up')
                return redirect(url_for('login'))
            except Exception as e:
                error = logging.error(traceback.format_exc())

        
        
    return render_template('signup.html', error=error)

@app.route('/login')
def login():
    return render_template('login.html')  # Replace with rendering a template for the login page

@app.route('/web-design')
def web_design():
    return "Web Design Service"

@app.route('/seo')
def seo():
    return "SEO Service"

@app.route('/forgot-password')
def forgot_password():
    return "Forgot Password Page"  # Replace with rendering a template for the forgot password page


@app.route('/consulting')
def consulting():
    return "Consulting Service"

if __name__ == '__main__':
    app.run(debug=True)
