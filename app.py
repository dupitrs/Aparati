from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = 'bam'  

@app.route("/")
def home():
    return render_template('index.html')

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

        with open('users.csv', 'a', newline='') as csvfile:
            userwriter = csv.writer(csvfile, delimiter=',')
            userwriter.writerow([username, password])

        return redirect(url_for('home'))  
    else:
        return render_template('register.html')  
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        with open('users.csv', mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0].strip() == username and row[1].strip() == password:
                    return redirect(url_for('main_page'))  # Redirect to main page after successful login

            print("No matching credentials found.")
            return jsonify({'success': False, 'message': 'Login failed. Please check your username and password.'})

    return render_template('login.html')

@app.route("/main_page")
def main_page():
    return render_template('main.html')  # Render the main page template

if __name__ == "__main__":
    app.run(debug=True)