"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project-tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    if not row:
        print(f"Cannot find {github}")
    else:
        print(f"Student: {row[0]} {row[1]}\nGitHub account: {row[2]}")


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    Query = """
        INSERT INTO students (first_name, last_name, github)
          VALUES (:first_name, :last_name, :github)
    """

    db.session.execute(Query, {'first_name' : first_name, 
                                'last_name' : last_name, 
                                'github' : github})
    db.session.commit()
    print(f"successfully added student: {first_name} {last_name}")

def make_new_project(title,description,max_grade):
    """Add a new project and print everything"""

    Query = """
        INSERT INTO projects (title, description, max_grade)
          VALUES (:title, :description, :grade)
    """

    db.session.execute(Query, {
        'title':title,'description':description,'grade':max_grade
    })
    db.session.commit()
    print(f"successfully added project:{title} /ndes:{description} /ngrade: {max_grade}")


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    Query = """
        SELECT title, description, max_grade
        FROM projects
        WHERE title = :title
        """
    db_cursor = db.session.execute(Query, {'title':title})

    row = db_cursor.fetchone()
    
    if not row:
        print(f"Cannot find {title}")
    else:
        print(f"Project:\t{row[0]}\ndescription:\t{row[1]}\ngrade:\t{row[2]}")

def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    Query = """
            SELECT project_title,grade
            FROM grades
            WHERE student_github = :github AND project_title = :title
    """

    db_cursor = db.session.execute(Query,{'github':github,'title':title})

    dataone = db_cursor.fetchone()

    print(f"datalist:{dataone}")

def get_grade_by_github(github):
    """Print grade student received and the project title."""
    Query = """
            SELECT project_title,grade            FROM grades
            WHERE student_github = :github
    """

    db_cursor = db.session.execute(Query,{'github':github})

    datalist = db_cursor.fetchall()

    for data in datalist:
        title,grade = data
        print(f"project_title:{title} grade:{grade}")

def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    Query = """
            INSERT INTO grades (student_github, project_title, grade)
            VALUES (:github, :title, :grade)    
    """
    db.session.execute(Query, {'github' : github, 'title' : title, 'grade' : grade})
    db.session.commit()
    print(f'Confirmed that grade {grade} of project {title} has been added for student {github}.')

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "assign":
            github,title,grade = args
            assign_grade(github, title, grade)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)
        
        elif command == "new_project":
            title,description,grade = args
            get_project_by_title(title,description,grade)

        elif command == "get_grade":
            github, title = args
            get_grade_by_github_title(github, title)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
