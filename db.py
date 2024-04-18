import sqlite3
from datetime import date


def get_db(name="main.db"):
    """
    Function to get a database connection.
    Args:
        name (str): The name of the database file. Defaults to "main.db".
    Returns:
        sqlite3.Connection: A connection object to the specified database.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Create tables in the database if they do not already exist.
    :param db: the database connection object
    :return: None
    """
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS habits (
        name TEXT PRIMARY KEY, 
        description TEXT,
        periodicity TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        habitName TEXT,
        streakCounter INTEGER,
        FOREIGN KEY(habitName) REFERENCES habits(name))""")
    db.commit()


def add_habit(db, name, description, periodicity):
    """
    A function that adds a new habit to the database.

    Parameters:
    - db: the database connection object
    - name: the name of the habit
    - description: a description of the habit
    - periodicity: how often the habit should be tracked

    Returns:
    This function does not return anything.
    """
    cur = db.cursor()
    cur.execute("INSERT or IGNORE INTO habits VALUES (?, ?, ?)", (name, description, periodicity))
    cur.execute("INSERT INTO tracker VALUES (?, ?, 0)", (date.today(), name))
    db.commit()


def remove_habit(db, name):
    """
    Remove a habit from the database.

    Args:
        db: the database connection object.
        name: Name of the habit to be removed.

    Returns:
        None
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE name = ?", (name,))
    cur.execute("DELETE FROM tracker WHERE habitName = ?", (name,))
    db.commit()


def update_habit(db, name, description, periodicity):
    """
    Updates a habit's description and periodicity in the database.

    Parameters:
    db: The database connection object.
    name: The name of the habit to update.
    description: The new description for the habit.
    periodicity: The new periodicity for the habit.

    Returns:
    None
    """
    cur = db.cursor()
    cur.execute("UPDATE habits SET description = ?, periodicity = ? WHERE name = ?", (description, periodicity, name))
    db.commit()


def complete_habit(db, name):
    """
    Generates a new streak for a given habit in the database,
    or updates a streak if one already exists.

    Parameters:
    db (database connection): The database connection object.
    name (string): The name of the habit to update.

    Returns:
    None
    """
    date_row = calculate_most_recent_date(db, name)
    cur = db.cursor()
    cur.execute("SELECT streakCounter FROM tracker WHERE date = ?", (date_row[0],))
    streak = cur.fetchone()
    cur.execute("INSERT or IGNORE INTO tracker VALUES (?, ?, ?)", (date.today(), name, streak[0] + 1))
    db.commit()


def get_habits(db):
    """
    Retrieves all habits from the database and returns the result.

    Parameters:
    db : the database connection object

    Returns:
    list : a list of tuples representing the retrieved habits
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    return cur.fetchall()


def get_tracker_data(db, name):
    """
    Get tracker data for a specific habit name from the database.

    Args:
        db: The database connection object.
        name: The name of the habit to retrieve tracker data for.

    Returns:
        A list of tuples containing the retrieved tracker data.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE habitName = ?", (name,))
    return cur.fetchall()


def get_habit_streak(db, name):
    """
    A function to retrieve the streakCounter value from the database for a given habit name.

    Parameters:
    - db: the database connection object
    - name: the name of the habit to retrieve the streak for

    Returns:
    - A single row from the database containing the streakCounter value for the specified habit
    """
    cur = db.cursor()
    cur.execute("SELECT streakCounter FROM tracker WHERE habitName = ?", (name,))
    return cur.fetchone()


def get_elapsed_time(db, habit):
    """
    Calculate the elapsed time between the start date of a habit and the current date.

    Parameters:
    - db: the database connection object
    - habit: the name of the habit to retrieve the start date for

    Returns:
    - elapsed_delta: the number of days between the start date of the habit and the current date
    """
    cur = db.cursor()
    cur.execute("SELECT MAX(date) FROM tracker WHERE habitName = ?", (habit,))
    habit_start_date = cur.fetchone()
    start_date = date.fromisoformat(habit_start_date[0])
    end_date = date.today()
    elapsed_time = end_date - start_date
    elapsed_delta = elapsed_time.days
    return elapsed_delta


def get_periodicity(db, habit):
    """
    Retrieves the periodicity of a specific habit from the database.

    Parameters:
    - db: the database connection object
    - habit: the name of the habit to retrieve periodicity for

    Returns:
    - The periodicity of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habits WHERE name = ?", (habit,))
    periodicity = cur.fetchone()
    return periodicity


def calculate_most_recent_date(db, habit):
    """
    Calculate the most recent date for a given habit.

    Parameters:
        db: The database connection object.
        habit: The name of the habit.

    Returns:
        tuple: A tuple containing the most recent date for the habit.
    """
    cur = db.cursor()
    cur.execute('SELECT MAX(date) FROM tracker WHERE habitName = ?', (habit,))
    return cur.fetchone()
