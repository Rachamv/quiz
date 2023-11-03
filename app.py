from flask import Flask, render_template, redirect, url_for, request, session
from core.database import Database
from datetime import datetime

app = Flask(__name__)

db = Database('./db/quiz.db')
db.connect()

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = db.execute_query("SELECT * FROM users WHERE username = ?", (form.username.data,))
        if not result:
            return redirect(url_for('login'))
        user = result[0]
        if user['password'] != form.password.data:  # Replace 'password' with your actual column name
            return redirect(url_for('login'))

        session['user_id'] = user['id']  # 'id' should represent the column name for the user ID
        session['marks'] = 0
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db.execute_query("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                         (form.username.data, form.email.data, form.password.data))
        session['user_id'] = db.conn.lastrowid  # Set the session user ID to the last inserted user ID
        session['marks'] = 0
        return redirect(url_for('home'))
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    form = QuestionForm()
    result = db.execute_query("SELECT * FROM questions WHERE q_id = ?", (id,))
    if not result:
        return redirect(url_for('score'))
    q = result[0]
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        option = request.form['options']
        correct_answer = q['correct_answer']  # Replace 'correct_answer' with the actual column name
        if option == correct_answer:
            session['marks'] += 10
        return redirect(url_for('question', id=(id + 1)))
    incorrect_answers = q['incorrect_answers'].split(',') if q['incorrect_answers'] else []
    options = [q['correct_answer']] + incorrect_answers
    form.options.choices = [(option, option) for option in options]
    return render_template('question.html', form=form, q=q, title=f'Question {id}')

@app.route('/score')
def score():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    new_score = session['marks']
    db.execute_query("UPDATE users SET marks = ? WHERE id = ?", (new_score, user_id))
    return render_template('score.html', title='Final Score')

@app.route('/logout')
def logout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    session.pop('user_id', None)
    session.pop('marks', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
