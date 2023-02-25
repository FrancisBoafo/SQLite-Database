import pandas as pd
import sqlite3
import uuid

import glob
from Activestudents import ActiveStudents
from Activestudents import SourceTagNames
from Activestudents import SchoolNames

def create_students_table(conn): 
    # Create/connect to a sqlite database
    conn = sqlite3.connect('NAU.db') 
    cur = conn.cursor()
    cur.execute(''' 
            CREATE TABLE IF NOT EXISTS Students (
                InternalID INTEGER PRIMARY KEY AUTOINCREMENT, 
                SchoolID INTEGER,
                StudentSchoolID TEXT,
                LastName TEXT,
                FirstName TEXT,
                SourceTagID INTEGER,
                FOREIGN KEY (SchoolID) REFERENCES Schools(SchoolID),
                FOREIGN KEY (SourceTagID) REFERENCES SourceTags(SourceTagID)
            )
        ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS SourceTags (
      SourceTagID INTEGER PRIMARY KEY AUTOINCREMENT,
      SourceID INTEGER,
      TagDate DATETIME, 
      Notes TEXT,
      FOREIGN KEY (SourceID) REFERENCES Sources(SourceID)
      )
    ''')
    cur.execute('''
      CREATE TABLE IF NOT EXISTS Sources (
        SourceID INTEGER PRIMARY KEY AUTOINCREMENT,
        SourceName TEXT,
        SchoolID INTEGER,
        Priority TEXT,
        FOREIGN KEY (SchoolID) REFERENCES School(SchoolID)
      )
    ''')
        # Create the SchoolID table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Schools (
          SchoolID INTEGER PRIMARY KEY AUTOINCREMENT,
          SchoolName TEXT
        )
    ''')
    conn.commit()
def add_students_to_database(conn):
    # Get the active students DataFrame
    conn = sqlite3.connect('NAU.db')
    cur = conn.cursor()
    active_students = ActiveStudents()
    student_df = active_students[['StudentSchoolID', 'LastName', 'FirstName']]

    # Get the sources DataFrame
    source_tag = SourceTagNames()
    sources = source_tag[['SourceTagName']]

    # Get the school DataFrame
    School_names = SchoolNames()
    Schools = School_names[['SchoolName ']]

    #SET THE STUDENTID in STUDENTS TABLE TO 2
    cur.execute("UPDATE Students SET SchoolID = 2;")

    #SET THE Sources in STUDENTS TABLE TO 2
    cur.execute("UPDATE Sources SET SchoolID = 2;")

    # Add the sources to the Sources table
    for _, row in sources.iterrows():
        cur.execute('''INSERT INTO Sources(SourceName)
                        SELECT ?
                   WHERE NOT EXISTS (SELECT SourceName FROM Sources WHERE SourceName = ?)
               ''', (row['SourceTagName'],row['SourceTagName']))

    # Add the schools to the Schools table
    for _, row in Schools.iterrows():
        cur.execute('''INSERT INTO Schools (SchoolName)
                     SELECT ?
                     WHERE NOT EXISTS (SELECT SchoolName FROM Schools WHERE SchoolName = ?)
                  ''', (row['SchoolName '],row['SchoolName ']))
        
    # Create a trigger to add a SourceTagID to the Students table
        cur.execute('''
            CREATE TRIGGER IF NOT EXISTS Student_trigger
            AFTER INSERT ON Students
            BEGIN
                INSERT INTO SourceTags (SourceID, TagDate, Notes)
                SELECT SourceID, datetime("now"), 'Pushed'
                FROM Sources
                WHERE Sources.SourceID = 1
                AND NOT EXISTS (
                    SELECT SourceID FROM SourceTags WHERE SourceID = 1 
                    AND TagDate = datetime("now") AND Notes = 'Pushed'
                );
                UPDATE Students
                SET SourceTagID = (
                    SELECT SourceTagID 
                    FROM SourceTags 
                    WHERE SourceID = 1 
                );
            END;
        ''')

    # Add the students to the Students table
    for _, row in student_df.iterrows():
        cur.execute('''INSERT INTO Students (StudentSchoolID, LastName, FirstName)
               SELECT ?, ?, ?
               WHERE NOT EXISTS (SELECT 1 FROM Students WHERE StudentSchoolID = ?)
               ''',(row['StudentSchoolID'], row['LastName'], row['FirstName'], row['StudentSchoolID'])) 
    conn.commit()

def SQLIteDB():
    # Create/connect to a sqlite database
    with sqlite3.connect('NAU.db') as conn:
        create_students_table(conn)
        add_students_to_database(conn) 
    conn.commit()
SQLIteDB()
