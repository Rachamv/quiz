from datetime import datetime
# from database import Database

class User:
    def __init__(self, username):
        self.username = username
        self.marks = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"User('{self.username}')"

class Question:
    def __init__(self, question_id, category, difficulty, question, correct_answer, incorrect_answers):
        self.question_id = question_id
        self.category = category
        self.difficulty = difficulty
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "category": self.category,
            "difficulty": self.difficulty,
            "question": self.question,
            "correct_answer": self.correct_answer,
            "incorrect_answers": self.incorrect_answers.split(',')
        }

class LeaderboardEntry:
    def __init__(self, user_id, score):
        self.user_id = user_id
        self.score = score
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def user_score(self):
        return self.score

    @classmethod
    def update_score(cls, user, new_score):
        db = Database('./db/leaderboard.db')
        db.connect()

        user.marks = new_score

        leaderboard_entry = db.execute_query("SELECT * FROM leaderboard WHERE user_id = ?", (user.id,))

        if not leaderboard_entry:
            db.execute_query("INSERT INTO leaderboard (user_id, score, created_at, updated_at) VALUES (?, ?, ?, ?)",
                             (user.id, new_score, datetime.utcnow(), datetime.utcnow()))
        else:
            db.execute_query("UPDATE leaderboard SET score = ?, updated_at = ? WHERE user_id = ?",
                             (new_score, datetime.utcnow(), user.id))

        db.close_connection()

    @classmethod
    def get_leaderboard(cls, limit=10):
        db = Database('./db/leaderboard.db')
        db.connect()

        result = db.execute_query("SELECT * FROM leaderboard ORDER BY score DESC LIMIT ?", (limit,))

        db.close_connection()

        return result

def main():
    db = Database('./db/leaderboard.db')  # Change to your database file
    db.connect()

    # Create tables if they don't exist
    db.execute_query('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            marks INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
    ''')

    db.execute_query('''
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY,
            category TEXT,
            difficulty TEXT,
            question TEXT,
            correct_answer TEXT,
            incorrect_answers TEXT
        );
    ''')

    db.execute_query('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            user_id INTEGER PRIMARY KEY,
            score INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
    ''')

    db.close_connection()

if __name__ == '__main__':
    main()
