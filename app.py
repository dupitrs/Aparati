from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import csv

app = Flask(__name__)

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
        username = request.form['username']
        password = request.form['password']
        
        with open('users.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Here we use the keys directly
                if row['username'] == username and row['password'] == password:
                    return redirect(url_for('main_page'))
            flash('Wrong username or password')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route("/main_page")
def main_page():
    return render_template('main.html')  # Render the main page template

if __name__ == "__main__":
    app.run(debug=True)
