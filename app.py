from flask import Flask, render_template, request, redirect, url_for, flash, session
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create database tables
db.create_tables()

# Routes and views
@app.route('/')
def index():
    # List all polls
    # Implement poll listing logic here
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user_by_username(username)

        if user:
            flash('Username is already in use. Please choose another.', 'danger')
        else:
            # Hash the password and store it in the database
            db.add_user(username, password)
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        input_password = request.form['password']

        user = db.get_user_by_username(username)

        if user and user[1] == input_password:
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# List all polls
@app.route('/polls')
def list_polls():
    polls = db.get_all_polls()
    return render_template('poll_list.html', polls=polls)

# Create a new poll
@app.route('/polls/create', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form['question']
        poll_id = db.add_poll(question)
        option_text = request.form.getlist('option_text')
        for option in option_text:
            db.add_option_to_poll(poll_id, option)
        flash('Poll created successfully!', 'success')
        return redirect(url_for('list_polls'))
    return render_template('create_poll.html')

# View a specific poll
@app.route('/polls/<int:poll_id>')
def view_poll(poll_id):
    options = db.get_poll_options(poll_id)
    return render_template('view_poll.html', options=options)

# Vote on a poll option
@app.route('/polls/vote/<int:option_id>')
def vote(option_id):
    # Implement vote logic here
    flash('Vote recorded!', 'success')
    return redirect(url_for('list_polls'))
# Other views, voting, and admin functionality

if __name__ == '__main__':
    app.run(debug=True)
