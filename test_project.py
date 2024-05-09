from habit import Habit
from db import get_db, add_habit, update_habit, complete_habit, get_periodicity, calculate_most_recent_date
from analyse import (get_streak_counter, habit_status, break_streak, get_habit_names, return_max_habit_streaks,
                     get_name_of_longest_streak, get_single_alltime_streak, get_alltime_streak, get_alltime_habit,
                     get_habits_by_periodicity)
from datetime import date, timedelta


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")

        add_habit(self.db, "test", "test", "daily")
        update_habit(self.db, "test", "test_updated", "daily")
        complete_habit(self.db, "test")

    def test_habit_creation(self):
        habit = Habit("test_habit_1", "test_habit_1", "daily")
        habit.store(self.db)

    def test_streak(self):
        streak = (get_streak_counter(self.db, "test"))
        assert streak == 0
        calculate_most_recent_date(self.db, "test")

    def test_habit_modules(self):
        habit = Habit("test_habit_2", "test_habit_2", "daily")
        habit.update(self.db)
        habit.remove(self.db)

    def test_habit_complete(self):
        habit = Habit("test_habit_3", "test_habit_3", "daily")
        habit.store(self.db)
        habit.complete(self.db)
        assert get_streak_counter(self.db, "test_habit_3") == 0
        cur = self.db.cursor()
        cur.execute("UPDATE tracker SET date = ? WHERE habitName = ?", (date.today() -
                                                                        timedelta(days=1), "test_habit_3"))
        habit.complete(self.db)
        assert get_streak_counter(self.db, "test_habit_3") == 1
        break_streak(self.db, "test_habit_3")
        assert get_streak_counter(self.db, "test_habit_3") == 0
        data = get_habit_names(self.db)
        assert len(data) == 2

    def test_get_functions(self):
        return_max_habit_streaks(self.db)
        get_habit_names(self.db)
        get_name_of_longest_streak(self.db)
        habit = Habit("test_habit_3", "test_habit_3", "daily")
        habit.store(self.db)
        cur = self.db.cursor()
        cur.execute("UPDATE tracker SET streakCounter = ? WHERE habitName = ?", (5, "test_habit_3"))
        data = get_single_alltime_streak(self.db, "test_habit_3")
        assert data == 5
        periodicity = str(get_periodicity(self.db, "test_habit_3"))[2:-3]
        assert periodicity == "daily"
        get_alltime_streak(self.db, periodicity)
        alltime_habit = get_alltime_habit(self.db, periodicity)
        assert alltime_habit == "test_habit_3"
        get_habits_by_periodicity(self.db, periodicity)

    def test_habit_status(self):
        habit = Habit("test_habit_4", "test_habit_4", "daily")
        habit.store(self.db)
        status = habit_status(self.db, "test_habit_4")
        assert status == 3
        cur = self.db.cursor()
        cur.execute("UPDATE tracker SET date = ? WHERE habitName = ?", (date.today() -
                                                                        timedelta(days=1), "test_habit_4"))
        status = habit_status(self.db, "test_habit_4")
        assert status == 1

    def teardown_method(self):
        import os
        self.db.close()
        os.remove("test.db")
