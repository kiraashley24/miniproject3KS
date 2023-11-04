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
    return render_template('poll_list.html', polls=polls, poll_id=None)


# Create a new poll
@app.route('/polls/create', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form['question']
        poll_id = db.add_poll(question)
        options = request.form.getlist('option_text')

        # Remove empty options
        options = [option for option in options if option.strip()]

        # Ensure that there are up to 5 options
        if len(options) > 5:
            flash('You can have up to 5 options for a poll.', 'danger')
            return redirect(url_for('create_poll'))

        for option_text in options:
            db.add_option_to_poll(poll_id, option_text)

        flash('Poll created successfully!', 'success')
        return redirect(url_for('list_polls'))
    return render_template('create_poll.html')



# View a specific poll
@app.route('/polls/<int:poll_id>')
def view_poll(poll_id):
    user_id = session.get('user_id')
    options = db.get_poll_options(poll_id)

    # Check if the user has already voted in this poll
    user_has_voted = db.has_user_voted(user_id, poll_id)

    return render_template('view_poll.html', user_has_voted=user_has_voted, poll_id=poll_id, options=options)



# Vote on a poll option
@app.route('/polls/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    if 'user_id' not in session:
        flash('You must be logged in to vote.', 'danger')
        return redirect(url_for('login'))

    option_id = request.form.get('option_id')

    if not option_id:
        flash('Please select an option to vote.', 'danger')
    else:
        user_id = session['user_id']

        # Check if the user has already voted in this poll
        if db.has_user_voted(user_id, poll_id):
            flash('You have already voted in this poll.', 'danger')
        else:
            # Record the vote in the database
            db.record_vote(user_id, poll_id, option_id)
            flash('Vote recorded!', 'success')

    return redirect(url_for('view_poll', poll_id=poll_id))


@app.context_processor
def inject_db_functions():
    # Define functions you want to make available in templates
    def get_vote_count(option_id):
        return db.get_vote_count(option_id)

    # Return the functions as a dictionary
    return dict(
        get_vote_count=get_vote_count
    )

# Add a route to display vote counts
@app.route('/votes')
def votes():
    polls = db.get_all_polls()
    vote_counts = {}

    for poll_id, _ in polls:
        vote_counts[poll_id] = db.get_vote_counts(poll_id)

    return render_template('votes.html', polls=polls, vote_counts=vote_counts)




if __name__ == '__main__':
    app.run(debug=True)
