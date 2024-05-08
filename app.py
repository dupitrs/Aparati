from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_session import Session
from datetime import timedelta
import csv
import os
from csv import DictReader


app = Flask(__name__)
app.secret_key = 'slepena'  
app.permanent_session_lifetime = timedelta(minutes=60) 
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
        
        # simboli
        if not username.isalnum():
            flash('Username must contain only letters and numbers')  # Flash error
            return redirect(url_for('register'))  # atpakal uz register
        
        # Check if file is empty and write headers
        if os.stat('users.csv').st_size == 0:
            with open('users.csv', 'a', newline='') as csvfile:
                userwriter = csv.writer(csvfile, delimiter=',')
                userwriter.writerow(['username', 'password', 'balance'])  # pirma rinda ar kolonnu nosaukumiem
        
        # uzraksta jauno lietotaju faila
        with open('users.csv', 'a', newline='') as csvfile:
            userwriter = csv.writer(csvfile, delimiter=',')
            userwriter.writerow([username, password, 1500])  # 1500 naudas uzreiz
        
        return redirect(url_for('login'))  # atpakal uz login
    else:
        return render_template('register.html')  # redero register formu
    
@app.route("/login", methods=["GET", "POST"])  
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # parbauda vai lietotajs ir pareizs
        with open('users.csv', 'r') as csvfile:
            userreader = csv.reader(csvfile, delimiter=',')
            for row in userreader:
                if row[0] == username and row[1] == password:
                    session['username'] = username  # glabaja lietotajvārdu sesijā
                    print("Username stored in session:", session['username'])  
                    return redirect(url_for('main_page'))  # atpakal uz galveno lapu
            
            flash('Invalid credentials')  # Flash error
            return redirect(url_for('login'))
    else:
        return render_template('login.html')  # redero login formu

@app.route("/user", methods=["GET"])
def user_profile():
    username = session.get('username')  # nemam lietotajvārdu no sesijas
    if username:  
        # fetcho balance from the CSV
        with open('users.csv', 'r') as csvfile:
            userreader = csv.reader(csvfile, delimiter=',')
            for row in userreader:
                if row[0] == username:
                    balance = row[2]  
                    break
            else:
                return redirect(url_for('login'))  # ja lietotajs nav atrasts, atpakal uz login
        return render_template('user.html', username=username, balance=balance)  # parada lietotaju un naudu
    else:
        return redirect(url_for('login'))  # ja nav lietotajvārda, atpakal uz login
    
@app.route("/main_page")
def main_page():
    return render_template('home.html')

@app.route("/logout")
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))  # redirect to login page

@app.route("/index")
def index():
    return render_template('home.html')  # redero index lapu

@app.route("/user")
def user():
    return render_template('user.html')  # Rendero  user page

@app.route("/aparats")
def aparats():
    username = session.get('username')  # nemam lietotajvārdu no sesijas
    if username:  # ja lietotajs ir ielogojies
        balance = None
        try:
            with open('users.csv', 'r') as csvfile:
                userreader = DictReader(csvfile, delimiter=',')
                for row in userreader:
                    if row['username'] == username:
                        balance = row['balance']  
                        break
        except FileNotFoundError:
            print("users.csv file not found")
        if balance is not None:
            return render_template('aparats.html', username=username, balance=balance) 
    return redirect(url_for('login'))  
@app.route('/deposit', methods=['POST'])
def deposit():
    amount = 100  
    username = session['username']  
    update_balance(username, amount)
    return redirect(url_for('user'))  


        
        
        
        
        
        



@app.route('/bet', methods=['POST'])
def bet():
    bet_amount = request.form.get('amount')  # get bet amount from form data
    total_Winning_Length = request.form.get('totalWinningLength')  # get total winning length from form data
    print(f"Bet Amount: {bet_amount}, Total Winning Length: {total_Winning_Length}")  # debug print
    username = session['username']  # get username from session

    # deduct the bet amount from user's balance
    update_balance(username, -int(bet_amount))

    # if user wins, add the winnings to user's balance
    if int(total_Winning_Length) > 0:  # user wins if total_Winning_Length > 0
        winnings = int(bet_amount) * int(total_Winning_Length)
        update_balance(username, winnings)

    return redirect(url_for('user'))  # redirect to user after bet

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
    