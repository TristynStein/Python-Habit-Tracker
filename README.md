# Python Habit Tracker

 Simple backend for a habit tracker, built in python with SQLite3 integration.
A basic command line interface, built using the 'questionary' package, 
 allows for users to navigate and use the program without coding knowledge.
Users can add, remove, and update, custom daily or weekly habits. 5 sample habits are included,
with 4 weeks of sample tracker data. 

## How It Works

On startup, the user will be prompted to select one of the functions of the program, such as adding, removing, updating
a habit, or viewing an analysis of the data. Navigating through the options is accomplished through the arrow keys, and
the 'enter' key is used to select an option.

Depending on which option is selected, the user will be prompted to enter the necessary information, such as the name of
the habit they wish to manipulate or view, or the periodicity of which they wish to analyse habits for.

### Add Habit
* The user will be prompted to enter the name of the habit they wish to add, followed by a description, and then a 
choice between daily or weekly periodicity.
#### Errors:
* Should the name of the habit already exist in the database, or the data field be left empty, 
the user will be notified that the habit already exists, and will be returned to the main menu.

### Remove Habit
* The user will be prompted to enter the name of the habit they wish to remove.
#### Errors:
* Should the name of the habit not exist in the database, or the data field be left empty, 
the user will be notified that the habit does not exist, and will be returned to the main menu.
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Mark Habit Complete
* The user will be prompted to enter the name of the habit they wish to mark as complete.
* Should the habit exist in the database, and it has not been marked as complete within the current period, 
the user will be notified that the habit has been marked as complete.
#### Errors: 
* Should the name of the habit not exist in the database, or the data field be left empty,
the user will be notified that the habit does not exist, and will be returned to the main menu.
* Should the habit exist in the database, but it has already been marked as complete within the current period,
the user will be notified that the habit has already been marked as complete, and will be returned to the main menu.
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Update Habit
* The user will be prompted to enter the name of the habit they wish to update.
* Should the habit exist in the database, the user will be prompted to enter its new description and periodicity.
#### Errors:
* Should the name of the habit not exist in the database, or the data field be left empty, 
the user will be notified that the habit does not exist, and will be returned to the main menu.
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Show habits
* The program will return a list of all habits currently in the database.
#### Errors:
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Show habits by periodicity
* The user will be prompted to choose the periodicity of the habits they wish to view.
#### Errors:
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Show a habit's streak
* The user will be prompted to enter the name of the habit they wish to view.
* Should the habit exist in the database, the program will return the current streak of the habit.
To return the longest streak recorded for a specific habit, use the "Show a habit's longest streak" option.
#### Errors:
* Should the name of the habit not exist in the database, or the data field be left empty,
the user will be notified that the habit does not exist, and will be returned to the main menu.
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Show my longest streak
* The program will return the name and streak value of the longest streak in the database.
#### Errors:
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Show a habit's longest streak
* The user will be prompted to enter the name of the habit they wish to view.
#### Errors:
* Should the name of the habit not exist in the database, or the data field be left empty,
the user will be notified that the habit does not exist, and will be returned to the main menu.
* Should no habits exist in the database, the user will be notified and returned to the main menu.

### Show the longest streak by periodicity
* The user will be prompted to choose the periodicity of the habits they wish to view analysis for.
#### Errors:
* Should no habits exist in the database, the user will be notified and returned to the main menu.

## Dependencies
```shell
pip install -r requirements.txt
```

## Usage
```shell
python3 main.py
```

## Testing
```shell
pytest .
```