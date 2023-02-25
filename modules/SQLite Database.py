import pandas as pd
import sqlite3
import uuid
from Activestudents import ActiveStudents

def create_students_table(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Students (
      InternalID INTEGER PRIMARY KEY AUTOINCREMENT, 
      SchoolID INTEGER,
      LastName TEXT,
      FirstName TEXT,
      StudentSchoolID TEXT,
      SourceTagID INTEGER,
      FOREIGN KEY (SchoolID) REFERENCES Schools(SchoolID),
      FOREIGN KEY (SourceTagID) REFERENCES SourceTags(SourceTagID)
        )
    ''')

def add_students_to_database(conn):
    # Get the active students DataFrame
    active_students = ActiveStudents()
    student_df = active_students[['SchoolStudentID', 'LastName', 'FirstName']]

    # Generate unique IDs for each student
    student_df['SchoolID'] = [str(uuid.uuid4()) for _ in range(len(student_df))]

    # Set the SchoolID to '2' for all rows
    student_df['SchoolID'] = '2'

    # Update or insert students into the database
    cur = conn.cursor()
    for _, row in student_df.iterrows():
        cur.execute('''
            UPDATE Students SET LastName=?, FirstName=?, SchoolID=?
            WHERE StudentSchoolID=?
        ''', (row['LastName'], row['FirstName'], row['SchoolID'], row['SchoolStudentID']))
        if cur.rowcount == 0:
            cur.execute('''
                INSERT INTO Students (SchoolID, LastName, FirstName, StudentSchoolID)
                VALUES (?, ?, ?, ?)
            ''', (row['SchoolID'], row['LastName'], row['FirstName'], row['SchoolStudentID']))
    conn.commit()

def SQLIteDB():
    # Create/connect to a sqlite database
    with sqlite3.connect('NAU.db') as conn:
        create_students_table(conn)
        add_students_to_database(conn)

SQLIteDB()

import pandas as pd