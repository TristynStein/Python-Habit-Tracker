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
    for i in range(len(habits)):
        streaks = get_streak_counter(db, habits[i])
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
    cur.execute("SELECT DISTINCT habitName FROM tracker WHERE streakCounter = ?", (return_max_habit_streaks(db),))
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


def get_single_alltime_streak(db, habit):
    """
    Returns the highest streak counter value for a specific habit from the tracker database.

    Parameters:
    - db: The database connection object.
    - habit: The name of the habit to retrieve the streak counter for.

    Returns:
    - The total streak counter value for the specified habit.
    """
    cur = db.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute("SELECT MAX(streakCounter) FROM tracker WHERE habitName = ?", (habit,))
    data = cur.fetchone()
    return data


def get_alltime_streak(db, periodicity):
    """
    Returns the highest streak counter value for a given periodicity from the tracker database.

    Parameters:
    - db: The database connection object.
    - periodicity: The periodicity of the habit to retrieve the streak counter for.

    Returns:
    - The total streak counter value for the specified habit.
    """
    cur = db.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute("SELECT MAX(streakCounter) FROM tracker WHERE habitName IN "
                "(SELECT name FROM habits WHERE periodicity = ?)", (periodicity,))
    streak_value = cur.fetchone()
    return streak_value


def get_alltime_habit(db, periodicity):
    """
    A function to retrieve habit names that match both streak and periodicity criteria.

    Parameters:
    - db: the database connection
    - periodicity: the period for which habits are checked

    Returns:
    - concatenated_data: a list containing the names of habits that match both criteria
    """
    streak_value = get_alltime_streak(db, periodicity)
    cur = db.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute("SELECT name FROM habits WHERE periodicity = ?", (periodicity,))
    periodic_habit_names = cur.fetchall()
    cur.execute("SELECT habitName FROM tracker WHERE streakCounter = ?", (streak_value,))
    streak_habit_names = cur.fetchall()
    data = [i for i in streak_habit_names if i in periodic_habit_names]
    concatenated_data = ""
    for x in range(len(data)):
        if x == 0:
            concatenated_data += str(data[x])
        else:
            concatenated_data += ", " + str(data[x])
    return concatenated_data


def get_habits_by_periodicity(db, periodicity):
    """
    Retrieves habits from the database based on the given periodicity.

    :param db: The database connection object.
    :param periodicity: The periodicity value to filter habits by.
    :return: A list of habit names that match the given periodicity.
    """
    cur = db.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute("SELECT DISTINCT name FROM habits WHERE periodicity = ?", (periodicity,))
    data = cur.fetchall()
    concatenated_data = ""
    for x in range(len(data)):
        if x == 0:
            concatenated_data += str(data[x])
        else:
            concatenated_data += ", " + str(data[x])
    return concatenated_data
