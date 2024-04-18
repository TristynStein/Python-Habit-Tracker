from db import (get_elapsed_time, get_periodicity)
from datetime import date


def get_habit_names(db):
    """
    Return a list of habit names from the database.

    :param db: the database connection object
    :return: a list of habit names
    """
    cur = db.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute("SELECT name FROM habits")
    data = cur.fetchall()
    return data


def return_max_habit_streaks(db):
    """
    Return the maximum habit streaks from the database.
    Parameters:
    - db: The database containing habit and streak information.
    Return:
    - The maximum habit streak.
    """
    habits = get_habit_names(db)
    print(habits)
    for i in range(len(habits)):
        streaks = get_streak_counter(db, habits[i])
        print(streaks)
        return max(str(streaks))


def get_name_of_longest_streak(db):
    """
    Return the name(s) of the habit(s) with the longest streak from the database.

    Parameters:
    db (database connection): The database connection object.

    Returns:
    str: A comma-separated string containing the names of habits with the longest streak.
    """
    cur = db.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute("SELECT habitName FROM tracker WHERE streakCounter = ?", (return_max_habit_streaks(db),))
    data = cur.fetchall()
    concatenated_data = ""
    for x in range(len(data)):
        if x == 0:
            concatenated_data += str(data[x])
        else:
            concatenated_data += ", " + str(data[x])
    return concatenated_data


def habit_status(db, habit):
    """
    Generate and return the status of a habit based on elapsed time and habit periodicity.

    Parameters:
    db (database): The database containing habit data.
    habit (string): The specific habit to check the status for.

    Returns:
    int: The status code indicating the habit status.
    """
    data = get_elapsed_time(db, habit)
    habit_period = str(get_periodicity(db, habit))[2:-3]
    if data == 1 and habit_period == "daily":
        return 1
        # 1 = Habit is ready to complete again
    if data == 7 and habit_period == "weekly":
        return 1
        # 1 = Habit is ready to complete again
    elif data < 1 and habit_period == "daily":
        return 3
        # 3 = Habit has been marked completed already today
    elif data < 7 and habit_period == "weekly":
        return 4
        # 4 = Habit has been marked completed already this week
    else:
        return 2
        # 2 = Habit has been broken


def break_streak(db, habit):
    """
    A function to break the streak for a given habit in the database.

    Parameters:
    - db: the database connection
    - habit: the name of the habit to break the streak for
    """
    cur = db.cursor()
    cur.execute("INSERT or IGNORE INTO tracker VALUES (?, ?, 0)", (date.today(), habit))
    cur.execute("UPDATE tracker SET streakCounter = 0 WHERE habitName = ? AND date = ?", (habit, date.today()))
    db.commit()


def get_streak_counter(db, habit):
    """
    Returns the most recent streak counter value for a specific habit from the tracker database.

    Parameters:
    - db: The database connection object.
    - habit: The name of the habit to retrieve the streak counter for.

    Returns:
    - The streak counter value for the specified habit.
    """
    cur = db.cursor()
    cur.execute("SELECT MAX(date) FROM tracker WHERE habitName = ?", (habit,))
    latest_date = cur.fetchone()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute("SELECT streakCounter FROM tracker WHERE habitName = ? AND date = ?", (habit, latest_date[0]))
    data = cur.fetchone()
    return data
