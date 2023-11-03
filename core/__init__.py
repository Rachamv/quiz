# core/__init__.py

# Import necessary modules or classes to expose them when the package is imported
from .database import Database
from .quiz_logic import QuizLogic
from .models import Question, LeaderboardEntry, User

# Define any initialization code if needed
# For example, setting up global variables, constants, or executing initial setup logic

# Optionally, define the __all__ variable to specify which modules will be imported
__all__ = ['Database', 'QuizLogic', 'Question', 'LeaderboardEntry', 'User' ]
