class QuizLogic:
    def __init__(self, db):
        self.db = db

    def get_quiz_questions(self):
        # Retrieve questions from the database
        questions = []
        query = "SELECT question, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3 FROM questions"
        cursor = self.db.execute_query(query)

        if cursor:
            for row in cursor:
                question = {
                    "question": row['question'],
                    "correct_answer": row['correct_answer'],
                    "incorrect_answers": [
                        row['incorrect_answer_1'],
                        row['incorrect_answer_2'],
                        row['incorrect_answer_3']
                    ]
                }
                questions.append(question)

        return questions
