import pandas as pd
import sqlite3
import uuid


def SQLIteDB():
    # Create/connect to a sqlite database
    connection = sqlite3.connect('NAU.db')

    # Create the Students table
    cur = connection.cursor()
    cur.execute('''
    CREATE TABLE Students (
      InternalID INTEGER PRIMARY KEY AUTOINCREMENT,
      SchoolID INTEGER,
      LastName TEXT,
      FirstName TEXT,
      StudentSchoolID TEXT,
      AdditionalSchools TEXT,
      SourceTagID INTEGER,
      FOREIGN KEY (SchoolID) REFERENCES Schools(SchoolID),
      FOREIGN KEY (SourceTagID) REFERENCES SourceTags(SourceTagID)
    )
    ''')

    # Define the DataFrame with columns StudentSchoolID, LastName, FirstName

    df = pd.DataFrame({ 
    'StudentSchoolID': ['123', '456', '789', '453'],
    'LastName': ['Smith', 'Johnson', 'Williams','Osei Akoto'],
    'FirstName': ['John', 'Mary', 'James', 'Kwame'],
    'SchoolID': ['1123', '1123', '1123', '1123']
    })
    # Generate unique IDs for each student
    df['StudentID'] = [str(uuid.uuid4()) for _ in range(len(df))]

    # Add the students to the database
    for i, row in df.iterrows():
        cur.execute('''
        INSERT INTO Students (SchoolID, LastName, FirstName, StudentSchoolID)
         VALUES (?, ?, ?, ?)
    ''', (row['SchoolID'], row['LastName'], row['FirstName'], row['StudentSchoolID']))
    connection.commit()

SQLIteDB()

import pandas as pd