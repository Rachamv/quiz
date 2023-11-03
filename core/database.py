import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return False

    def execute_query(self, query, values=None):
        if not self.conn:
            if not self.connect():
                print("Can't establish database connection")
                return None

        cursor = self.conn.cursor()
        try:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
