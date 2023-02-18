import pandas as pd

# Read the csv file into a DataFrame
def ActiveStudents():
    file_path = "/Users/francisboafo/Library/CloudStorage/OneDrive-Personal/SQLite Database Environment/NAU Data/NAU.csv"
    active_students = pd.read_csv(file_path)
    print(len(active_students))
    return active_students
ActiveStudents() 
