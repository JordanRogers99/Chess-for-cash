import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from chess import Chess  # Import the chess module to handle game logic

app = Flask(__name__)
app.secret_key = 'some_random_key'  # Required for flashing messages and sessions

# Path to the file where the user data will be stored
USER_DB_FILE = 'users.json'


# Function to load the user data from the file
def load_users_db():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {}


# Function to save the user data to the file
def save_users_db(users_db):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users_db, f)


# Load the user data into memory at the start of the app
users_db = load_users_db()


# Home route
@app.route('/')
def index():
    return render_template('index.html')


# Login and Register route (same route for both actions)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')  # Check if it's login or register

        if action == 'login':  # Handle login action
            username = request.form['username']
            password = request.form['password']

            # Check if username exists in the "database"
            if username in users_db:
                stored_password_hash = users_db[username]

                # Check if entered password matches the stored hashed password
                if check_password_hash(stored_password_hash, password):
                    flash('Login Successful!', 'success')
                    return redirect(url_for('index'))  # Redirect to homepage
                else:
                    flash('Invalid Credentials. Try again.', 'error')
            else:
                flash('Username not found. Please register first.', 'error')

        elif action == 'register':  # Handle registration action
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Check if the username already exists
            if username in users_db:
                flash('Username already taken. Please choose another.',
                      'error')
                return redirect(url_for('login'))

            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match. Please try again.', 'error')
                return redirect(url_for('login'))

            # Hash the password before storing
            hashed_password = generate_password_hash(password)

            # Save the user to the "database" (in-memory dictionary)
            users_db[username] = hashed_password
            save_users_db(users_db)  # Save the updated user data to the file

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('login.html')  # Render the login form


# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')  # Make sure you create this file


# Tournaments page route
@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html')  # Make sure you create this file


# FAQ page route
@app.route('/faq')
def faq():
    return render_template('faq.html')  # Make sure you create this file


# Play route for chess game
@app.route('/play')
def play():
    return render_template('play.html')  # Render the play.html page

if __name__ == '__main__':
    app.run(debug=True)
