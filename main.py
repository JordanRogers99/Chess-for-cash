from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  # Initialize Flask app
app.secret_key = 'your_secret_key'  # Secret key for session management and flash messages

# In-memory database simulation (replace with actual database in production)
users_db = {}


# Function to simulate saving users to a file (or database)
def save_users_db(users_db):
    # You can implement this to save the data to a file or a real database
    pass


# Home route - Index Page
@app.route('/')
def index():
    return render_template('index.html')  # Render the home page


# Login and Registration Route
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
                    return redirect(
                        url_for('index')
                    )  # Redirect to the home page after successful login
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
            return redirect(
                url_for('login')
            )  # Redirect to the login page after successful registration

    return render_template('login.html')  # Render the login form


# Contact route
@app.route('/contact')
def contact():
    return render_template('contact.html')  # Render the contact page


# Tournaments route
@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html')  # Render the tournaments page


# FAQ route - New route added for FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')  # Render the FAQ page


# Play route - New route added for Play Chess page
@app.route('/play')
def play():
    return render_template('play.html')  # Render the Play Chess page


# Logout route
@app.route('/logout')
def logout():
    # Implement logout functionality, e.g., clearing session data
    flash('You have been logged out successfully.', 'success')
    return redirect(
        url_for('index'))  # Redirect to the index page after logout


if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode
