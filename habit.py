from db import add_habit, update_habit, remove_habit, complete_habit, get_habit_streak


class Habit:
    """
    Class to represent a habit

    Parameters
    ----------
    name : str
        The name of the habit
    description : str
        A description of what is required to complete the habit
    periodicity : str
        The periodicity of the habit, either weekly or daily
    """

    def __init__(self, name: str, description: str, periodicity: str):
        self.name = name
        self.description = description
        self.periodicity = periodicity

    def store(self, db):
        add_habit(db, self.name, self.description, self.periodicity)

    def complete(self, db):
        complete_habit(db, self.name)

    def update(self, db):
        update_habit(db, self.name, self.description, self.periodicity)

    def remove(self, db):
        remove_habit(db, self.name)

    def get_streak(self, db):
        get_habit_streak(db, self.name)
