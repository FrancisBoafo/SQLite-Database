import pandas as pd

# Read the csv file into a DataFrame
def ActiveStudents():
    file_path = "/Users/francisboafo/Library/CloudStorage/OneDrive-Personal/SQLite Database Environment/Datasets"
    active = f"{file_path}/NAU.csv"
    active_students = pd.read_csv(active)
    return active_students
ActiveStudents()
def SourceTagNames():
    sourcetag = f"/Users/francisboafo/Library/CloudStorage/OneDrive-Personal/SQLite Database Environment/Datasets/SourceTagNames.csv"
    Source_tag= pd.read_csv(sourcetag) 
    print(len(Source_tag))
    return Source_tag
def SchoolNames():
    school = f"/Users/francisboafo/Library/CloudStorage/OneDrive-Personal/SQLite Database Environment/Datasets/Schools.xlsx"
    School_names = pd.read_excel(school)
    return School_names
# Call the ActiveStudents() function and store the result in a variable
active_students = ActiveStudents()
Source_tag = SourceTagNames()
School_names = SchoolNames()

