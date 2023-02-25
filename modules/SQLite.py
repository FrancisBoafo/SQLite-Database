import SQLite 
import pandas as pd
import sqlite3
import glob
import os




def load_csv_files_to_sqlite(conn):
    # Connect to the database
    conn = sqlite3.connect('NAU.db')
    file_lst = glob.glob('C:/Users/FrancisOseiBoafo/Documents/Leads List/*.csv')

    # Extract file name individually and puts table name
    for individual_file in range(0,len(file_lst)):
        df = pd.read_csv(file_lst[individual_file])
        df.columns = df.columns.str.strip()
        extracted_file_name = file_lst[individual_file]
        sub1 = '\\\\'
        sub1 = sub1[0]
        sub2 = '.'
        extracted_file_name = extracted_file_name.replace(sub1,"*")
        extracted_file_name = extracted_file_name.replace(sub2,"*")
        extracted_file_name = extracted_file_name.split("*")
        extracted_file_name = extracted_file_name[1]
        df.to_sql(extracted_file_name, conn, if_exists='replace')

 # Create the Sources table
def create_tables(conn):
    # Connect to the database
    conn = sqlite3.connect('NAU.db')
    cur = conn.cursor()

      # Create the Students table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        StudentInternalID INTEGER PRIMARY KEY AUTOINCREMENT,
        SchoolID INTEGER,
        StudentSchoolID INTEGER,
        LastName TEXT,
        FirstName TEXT,
        SourceTagID INTEGER,
        FOREIGN KEY (SchoolID) REFERENCES Schools(SchoolID),
        FOREIGN KEY (SourceTagID) REFERENCES SourceTags(SourceTagID)
      )
    ''')

      # Create the Students table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS SourceTags (
      SourceTagID INTEGER PRIMARY KEY AUTOINCREMENT,
      SourceID INTEGER,
      TagDate DATETIME, 
      Notes TEXT,
      FOREIGN KEY (SourceID) REFERENCES Sources(SourceID)
      )
    ''')
     # Create the SchoolID table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Schools (
          SchoolID INTEGER PRIMARY KEY AUTOINCREMENT,
          SchoolName TEXT
        )
    ''')
    #CREATE SOURCE TABLE
    cur.execute('''
      CREATE TABLE IF NOT EXISTS Sources (
        SourceID INTEGER PRIMARY KEY AUTOINCREMENT,
        SourceName TEXT,
        SchoolID INTEGER,
        Priority TEXT,
        FOREIGN KEY (SchoolID) REFERENCES School(SchoolID)
      )
      ''')
    # Create The ContactInfo
    # THERE ISNT A NO BUILT IN DATATYPE FOR CATEGORICAL VALUE
    cur.execute(''' 
      CREATE TABLE IF NOT EXISTS ContactInfo (
        ContactInfoID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER,
        Phone TEXT,
        Email TEXT,
        TimeZone TEXT, 
        SourceTagID INTEGER,
        FOREIGN KEY (StudentID) REFERENCES Students (StudentInternalID)
        FOREIGN KEY (SourceTagID) REFERENCES SourceTags(SourceTagID)
      )
    ''')
  # Create The EduStatus
    cur.execute('''
      CREATE TABLE IF NOT EXISTS EduStatus (
        EduStatusID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        Program TEXT,
        TotalCredit INTERGER,
        SourceTagID INTEGER,
        FOREIGN KEY (StudentID) REFERENCES Students (StudentSchoolID),
        FOREIGN KEY (SourceTagID) REFERENCES SourceTags (SourceTagID)
      )
    ''')


def insert_and_update(conn):
    conn = sqlite3.connect('NAU.db')
    cur = conn.cursor()
    # INSERT DATA INTO TABLES 
    #SCHOOL
    cur.execute('''INSERT INTO Schools (SchoolName)
                  SELECT School_Names FROM [SchoolID List Raw Data]
                  WHERE NOT EXISTS (SELECT SchoolID FROM Schools WHERE SchoolID = SchoolID)
    ''')
    #SOURCES
    cur.execute('''INSERT INTO Sources (SourceName, SchoolID)
               SELECT SourceTagName, [School ID] FROM [Sources Raw Data]
               WHERE NOT EXISTS (SELECT SourceName FROM Sources WHERE SourceName = SourceTagName)
    ''')
   

    Unique_Standard_Data,close,Gold_standard_Data,unique_term = ActiveStudents.Activestudents()
    student_df = Unique_Standard_Data[['StudentSchoolID', 'LastName', 'FirstName']]

     #STUDENTS
     # insert the data into the Students table
    for _, row in student_df.iterrows():
        cur.execute('''INSERT INTO Students (StudentSchoolID, LastName, FirstName)
                   SELECT ?, ?, ?
                   WHERE NOT EXISTS (SELECT 1 FROM Students WHERE StudentSchoolID = ?)''',
                   (row['StudentSchoolID'], row['LastName'], row['FirstName'], row['StudentSchoolID']))
        cur.execute('''
          CREATE TRIGGER IF NOT EXISTS Student_trigger
          AFTER INSERT ON Students
          BEGIN
              INSERT INTO SourceTags (SourceID,TagDate,Notes)
              SELECT SourceID, datetime('now'), 'Pushed'
              FROM Sources
              WHERE Sources.SourceID = 1
              AND NOT EXISTS (
                  SELECT SourceID FROM SourceTags WHERE SourceID = 1 
                  AND TagDate = datetime('now') AND Notes = 'Pushed'
               )
              LIMIT 1;
              UPDATE Students
              SET SourceTagID = (
                  SELECT SourceTagID 
                  FROM SourceTags 
                  WHERE SourceID = 2 
                  AND TagDate = datetime('now') AND Notes = 'Pushed'
                  AND NOT EXISTS (
                  SELECT 1 FROM Students WHERE Students.SourceTagID = SourceTags.SourceTagID
                  )
              )
              WHERE StudentSchoolID IN (
                  SELECT StudentSchoolID FROM Students);
          END;
        ''')

    #SET THE STUDENTID in STUDENTS TABLE TO 2
    
    cur.execute("UPDATE Students SET SchoolID = 2;")
    # PLACES THE DATA INTO THE STUDENTS TABLE FOR THE SOURCETAGSID
                  # 
    cur.execute('''UPDATE Students
                  SET SourceTagID = (
                  SELECT SourceTagID
                  FROM SourceTags
                  ORDER BY TagDate DESC
                  LIMIT 1
                  )
                  WHERE SourceTagID IS NULL;
    ''')

    #CONTACTINFO
    cur.execute('''INSERT INTO ContactInfo (StudentID,SourceTagID)
                    SELECT StudentSchoolID, SourceTagID FROM Students
                    WHERE NOT EXISTS (SELECT StudentID FROM ContactInfo WHERE StudentID = StudentSchoolID)
    ''')

    contact_Info =close[['primary_contact_primary_phone', 'primary_contact_primary_email', "custom.0.1 Timezone", "EMPLID"]]
    # Iterate over rows of contact_Info
    for _, row in contact_Info.iterrows():
      if pd.isna(row['EMPLID']):
        continue
      cur.execute(f'''
          UPDATE ContactInfo
          SET Phone = '{row['primary_contact_primary_phone']}',
              Email = '{row['primary_contact_primary_email']}',
              Timezone = '{row['custom.0.1 Timezone']}'
           WHERE StudentID = '{int(row['EMPLID'])}';
      ''')

      cur.execute('''
          CREATE TRIGGER IF NOT EXISTS contact_trigger
          AFTER UPDATE ON ContactInfo
          BEGIN
              INSERT INTO SourceTags (SourceID,TagDate,Notes)
              SELECT SourceID, datetime('now'), 'Pushed'
              FROM Sources
              WHERE Sources.SourceID = 2
              AND NOT EXISTS (
                  SELECT SourceID FROM SourceTags WHERE SourceID = 2 
                  AND TagDate = datetime('now') AND Notes = 'Pushed'                 
              )
              LIMIT 1;
              UPDATE ContactInfo
              SET SourceTagID = (
                  SELECT SourceTagID 
                  FROM SourceTags 
                  WHERE SourceID = 2 
                  AND TagDate = datetime('now') AND Notes = 'Pushed'
              )
              WHERE StudentID = NEW.StudentID;
          END;
        ''') 
     

    conn.commit()
def SQLIteDB():
    # Create/connect to a sqlite database
    with sqlite3.connect('NAU.db') as conn:
      load_csv_files_to_sqlite(conn)
      create_tables(conn)
      insert_and_update(conn)      
      conn.commit() 
SQLIteDB()