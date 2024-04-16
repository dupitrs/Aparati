from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'superslepenaatslega'

@app.route("/")
def home():
    return render_template('login.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        with open('users.csv', mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0].strip() == username and row[1].strip() == password:
                    return redirect(url_for('main_page'))
        flash("Login failed. Please check your username and password.")
    return render_template('login.html')  # No need to pass the error message here


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # Check if file is empty and write headers
        if os.stat('users.csv').st_size == 0:
            with open('users.csv', 'a', newline='') as csvfile:
                userwriter = csv.writer(csvfile, delimiter=',')
                userwriter.writerow(['username', 'password'])
        
        # Write the new user's data to the file
        with open('users.csv', 'a', newline='') as csvfile:
            userwriter = csv.writer(csvfile, delimiter=',')
            userwriter.writerow([username, password])
        
        return redirect(url_for('login'))  # Redirect to login after registration
    else:
        return render_template('register.html')  # Render the registration form
    
    
@app.route("/main_page", methods=["GET", "POST"])
def main_page():
    return render_template('home.html')

@app.route("/user.html", methods=["GET"])
def user_profile():
    return render_template('user.html')

if __name__ == "__main__":
    app.run(debug=True)