from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to your actual secret key

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # You might want to add validation and hashing of the password here

        # Write to CSV
        with open('users.csv', 'a', newline='') as csvfile:
            userwriter = csv.writer(csvfile, delimiter=',')
            userwriter.writerow([username, password])

        return redirect(url_for('home'))  # Redirect to the home page after registration
    else:
        return render_template('register.html')  # Show the registration form
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Open the CSV and use DictReader to read rows into a dictionary
        with open('users.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Compare the form input with the CSV content
                if row['username'].strip() == username and row['password'].strip() == password:
                    # If a match is found, return success message
                    return jsonify({'success': True, 'message': 'Login successful'})
            # If no match is found after checking all rows, print message
            print("No matching credentials found.")
            return jsonify({'success': False, 'message': 'Login failed. Please check your username and password.'})

    # If it's a GET request or the else part of POST, show the login form
    return render_template('login.html')







@app.route("/main_page")
def main_page():
    return render_template('main.html')  # Render the main page template

if __name__ == "__main__":
    app.run(debug=True)
