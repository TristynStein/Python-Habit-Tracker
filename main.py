import questionary
from db import get_db, get_habits
from habit import Habit
from analyse import (return_max_habit_streaks, break_streak, habit_status, get_habit_names,
                     get_streak_counter, get_name_of_longest_streak)


def cli():
    """
    Command line interface for managing habits. Allows users to add, remove, and mark habits as complete,
    as well as view and manage habit streaks. Upon initialization, checks if there are any habits in the database and
    calls the corresponding function to check the status of each habit, overwriting streak data if necessary.
    """
    db = get_db()
    habit_names = get_habit_names(db)
    # Checks for habits in the database and breaks streaks if necessary
    for i in range(len(habit_names)):
        if habit_status(db, habit_names[i]) == 2:
            break_streak(db, habit_names[i])

    # Main loop for user interaction
    stop = False
    while not stop:
        # Present user with options
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Add habit", "Remove habit", "Mark habit complete",
                "Show habits", "Show a habit's streak", "Show my highest streak",
                "Exit"],
        ).ask()

        if choice == "Show habits":
            # Display all habits within the database
            habits = get_habits(db)
            if not habits:
                print("No habits found")
            else:
                print(get_habits(db))

        elif choice == "Add habit":
            # Write a new habit to the database
            name = questionary.text("Enter the name of the habit").ask()
            if get_habit_names(db) is not None and name in get_habit_names(db):
                print("Habit already exists")
            elif name == "":
                print("Habit name cannot be empty")
            else:
                description = questionary.text("Enter the description of the habit").ask()
                periodicity = questionary.select(
                    "Enter the periodicity of the habit",
                    choices=["daily", "weekly"],
                ).ask()
                habit = Habit(name, description, periodicity)
                habit.store(db)

        elif choice == "Remove habit":
            # Remove a habit and all corresponding tracker data from the database
            if not get_habits(db):
                print("No habits found")
            else:
                name = questionary.text("Enter the name of the habit").ask()
                if name == "":
                    print("Habit name cannot be empty")
                elif name not in get_habit_names(db):
                    print("Habit does not exist")
                habit = Habit(name, "", "")
                habit.remove(db)

        elif choice == "Mark habit complete":
            # Write a new row entry to the database, incrementing the previous streak counter value by 1
            if not get_habits(db):
                print("No habits found")
            else:
                name = questionary.text("Enter the name of the habit").ask()
                if name not in get_habit_names(db):
                    print("Habit does not exist")
                else:
                    habit = Habit(name, "", "")
                    status = habit_status(db, name)
                    if status == 1:
                        habit.complete(db)
                    elif status == 3:
                        print("Habit has been marked completed already today")
                    elif status == 4:
                        print("Habit has been marked completed already this week")
                    elif status == 2:
                        habit.complete(db)
                        break_streak(db, name)
                        print("Habit has been broken")

        elif choice == "Show a habit's streak":
            # Display the current streak for a given habit
            if not get_habits(db):
                print("No habits found")
            else:
                name = questionary.text("Enter the name of the habit").ask()
                if name not in get_habit_names(db):
                    print("Habit does not exist")
                elif name == "":
                    print("Habit name cannot be empty")
                else:
                    streak = get_streak_counter(db, name)
                    print(f'The habit "{name}" has a streak of {streak} days!')

        elif choice == "Show my highest streak":
            # Display the name(s) of the habit(s) with the longest streak
            if not get_habits(db):
                print("No habits found")
            else:
                print(f'The habit(s) with the longest streak are {get_name_of_longest_streak(db)}'
                      f' with a streak of {return_max_habit_streaks(db)}!')

        elif choice == "Exit":
            exit()


if __name__ == "__main__":
    cli()
