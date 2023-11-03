import sqlite3
import logging
from quizsdata import quiz_data

# Configure logging to save errors to a file
logging.basicConfig(filename='databaselog.txt', level=logging.ERROR)

# Connect to the SQLite database
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Create a table to store the quiz questions if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    type TEXT,
                    difficulty TEXT,
                    question TEXT,
                    correct_answer TEXT,
                    incorrect_answers TEXT
                )''')

# Count the number of questions before insertion
cursor.execute("SELECT COUNT(*) FROM questions")
previous_count = cursor.fetchone()[0]
print(f"Total number of questions before insertion: {previous_count}")

# Insert the quiz data into the database, checking for duplicates and logging errors
for question in quiz_data:
    # Check if the question already exists
    cursor.execute("SELECT id FROM questions WHERE question = ?", (question['question'],))
    existing_question = cursor.fetchone()

    if existing_question is None:
        # Convert incorrect_answers to a string for insertion
        incorrect_answers = ",".join(question['incorrect_answers'])

        # Insert the question into the database
        cursor.execute('''INSERT INTO questions (category, type, difficulty, question, correct_answer, incorrect_answers)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                       (question['category'], question['type'], question['difficulty'], question['question'],
                        question['correct_answer'], incorrect_answers))
    else:
        # Log the error to the file
        logging.error(f"Duplicate question found: {question['question']}")

# Count the number of questions after insertion
cursor.execute("SELECT COUNT(*) FROM questions")
current_count = cursor.fetchone()[0]
print(f"Total number of questions after insertion: {current_count}")

conn.commit()  # Commit the changes
conn.close()  # Close the connection
