from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
from datetime import timedelta
import csv
import os


app = Flask(__name__)
app.secret_key = 'slepena'  # Replace with your own secret key
app.permanent_session_lifetime = timedelta(minutes=60)  # set session lifetime to 60 minutes
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # Check if username is alphanumeric
        if not username.isalnum():
            return "Username must contain only letters and numbers"
        
        # Check if file is empty and write headers
        if os.stat('users.csv').st_size == 0:
            with open('users.csv', 'a', newline='') as csvfile:
                userwriter = csv.writer(csvfile, delimiter=',')
                userwriter.writerow(['username', 'password', 'balance'])  # Add 'balance' to the headers
        
        # Write the new user's data to the file
        with open('users.csv', 'a', newline='') as csvfile:
            userwriter = csv.writer(csvfile, delimiter=',')
            userwriter.writerow([username, password, 1500])  # Set the initial balance to 1500
        
        return redirect(url_for('login'))  # Redirect to login after registration
    else:
        return render_template('register.html')  # Render the registration form

@app.route("/login", methods=["GET", "POST"])  # Change the route to "/login"
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user's credentials are valid
        with open('users.csv', 'r') as csvfile:
            userreader = csv.reader(csvfile, delimiter=',')
            for row in userreader:
                if row[0] == username and row[1] == password:
                    session['username'] = username  # Store the username in session
                    print("Username stored in session:", session['username'])  # Print the stored username
                    return redirect(url_for('main_page'))  # Redirect to main_page if login is successful
            return "Invalid credentials"  # Return an error message if login is unsuccessful
    else:
        return render_template('login.html')  # Render the login form

@app.route("/user", methods=["GET"])
def user_profile():
    username = session.get('username')  # Get the username from session
    if username:  # If a username is found in the session
        # Fetch the user's balance
        with open('users.csv', 'r') as csvfile:
            userreader = csv.reader(csvfile, delimiter=',')
            for row in userreader:
                if row[0] == username:
                    balance = row[2]  # The balance is in the third column
                    break
            else:
                return redirect(url_for('login'))  # If no matching username is found, redirect to the login page
        return render_template('user.html', username=username, balance=balance)  # Pass the username and balance to the template
    else:
        return redirect(url_for('login'))  # If no username is found, redirect to the login page
    
@app.route("/main_page")
def main_page():
    return render_template('home.html')

@app.route("/logout")
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))  # Redirect to the login page

@app.route("/index")
def index():
    return render_template('home.html')  # Render the home page

@app.route("/user")
def user():
    return render_template('user.html')  # Render the user page

@app.route("/aparats")
def aparats():
    return render_template('aparats.html')  # Render the aparats page

@app.route('/deposit', methods=['POST'])
def deposit():
    amount = 100  # fixed deposit amount
    username = session['username']  # get username from session
    update_balance(username, amount)
    return redirect(url_for('user'))  # redirect to user after deposit

def update_balance(username, amount):
    # read the CSV
    with open('users.csv', 'r') as f:
        users = list(csv.reader(f))

    # find the user and update their balance
    for user in users:
        if user[0] == username:
            user[2] = str(int(user[2]) + amount)
            break

    # write the updated data back to the CSV
    with open('users.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(users)
        
if __name__ == "__main__":
    app.run(debug=True)
    