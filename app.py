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
    polls = db.get_all_polls()
    return render_template('index.html', polls=polls)

# Registration route
# (Existing registration route)

# Login route
# (Existing login route)

# Logout route
# (Existing logout route)

# List all polls
@app.route('/polls')
def poll_list():
    polls = db.get_all_polls()
    return render_template('poll_list.html', polls=polls)

# View a specific poll and its options
@app.route('/poll/<int:poll_id>')
def view_poll(poll_id):
    poll = db.get_poll_by_id(poll_id)
    options = db.get_options_by_poll_id(poll_id)
    return render_template('view_poll.html', poll=poll, options=options)

# Vote on a poll
@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    if request.method == 'POST':
        user_id = session.get('user_id')
        option_id = request.form.get('option_id')

        if not user_id:
            flash('You must be logged in to vote.', 'danger')
        else:
            # Check if the user has already voted in this poll
            if not db.has_user_voted(user_id, poll_id):
                # Insert the vote into the database
                db.add_vote(user_id, poll_id, option_id)
                flash('Your vote has been recorded.', 'success')
            else:
                flash('You have already voted in this poll.', 'danger')

    return redirect(url_for('view_poll', poll_id=poll_id))

# Create a new poll
@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        # Retrieve the poll question and options from the form
        question = request.form.get('question')
        options = request.form.getlist('option')

        # Insert the poll and options into the database
        poll_id = db.add_poll(question)
        db.add_options(poll_id, options)
        flash('Poll created successfully.', 'success')
        return redirect(url_for('view_poll', poll_id=poll_id))

    return render_template('create_poll.html')

if __name__ == '__main__':
    app.run(debug=True)
