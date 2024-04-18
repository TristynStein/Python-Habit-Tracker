from habit import Habit
from db import get_db, add_habit, update_habit, complete_habit
from analyse import calculate_streak


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")

        add_habit(self.db, "test", "test", "daily")
        update_habit(self.db, "test", "test_updated", "daily_updated")
        complete_habit(self.db, "test")

    def test_habit(self):
        habit = Habit("test_habit", "test_habit", "test_daily")
        habit.store(self.db)

    def test_calculate_streak(self):
        streak = calculate_streak(self.db, "test")
        assert streak == 1

    def teardown_method(self):
        import os
        self.db.close()
        os.remove("test.db")
