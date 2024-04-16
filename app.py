from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os

app = Flask(__name__)
app.secret_key = 'slepena'  # Replace with your own secret key

@app.route("/")
def home():
    return render_template('login.html')

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
                    return redirect(url_for('main_page'))  # Redirect to main_page if login is successful
            return "Invalid credentials"  # Return an error message if login is unsuccessful
    else:
        return render_template('login.html')  # Render the login form

@app.route("/main_page")
def main_page():
    return render_template('home.html')

@app.route("/user", methods=["GET"])
def user_profile():
    return render_template('user.html')

@app.route('/api/username', methods=['GET'])
def get_username():
    return jsonify(username='Guest')

if __name__ == "__main__":
    app.run(debug=True)