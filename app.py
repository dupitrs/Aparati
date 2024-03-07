# app.py

from flask import Flask, render_template, request, jsonify
import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def get_users():
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        return {row[0]: row[1] for row in reader}

def write_user(username, password):
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

def check_credentials(username, password):
    users = get_users()
    hashed_password = users.get(username)

    return hashed_password and check_password_hash(hashed_password, password)

def user_exists(username):
    users = get_users()
    return username in users

def add_user(username, password):
    hashed_password = generate_password_hash(password)
    write_user(username, hashed_password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if check_credentials(username, password):
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not user_exists(username):
        add_user(username, password)
        return jsonify(success=True)
    else:
        return jsonify(success=False)

if __name__ == '__main__':
    app.run(debug=True)
