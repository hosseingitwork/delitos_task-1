import pandas as pd
import sqlite3
import datetime
import os
### @autor Hossein Yahyazadeh
### pcd systems challenge

###SECTION - file name function
def filename_creator():
    # getting the current date in the format 'YYYY_MM_DD'
    current_date = datetime.datetime.now().strftime('%Y_%m_%d')

    # creating the filename using the current date
    filename = f'queries_{current_date}.txt'

    # check if the file already exists
    if os.path.exists(filename):
        # reoving the existing file
        os.remove(filename)

    return filename


###SECTION - 6. Execute the queries to the DB.
def execute_queries_from_file(database_file, queries_file):
   
    # establish connection to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # read queries from the file
    with open(queries_file, 'r') as file:
        queries = file.readlines()

    # execute each query
    for query in queries:
        cursor.execute(query)

    # commit changes and close connection
    conn.commit()
    conn.close()

###SECTION - query function:
def save_queries_to_file(queries, filename):
    
    # openning the file in write mode
    with open(filename, 'a') as file:
        # write each query to the file
        for query in queries:
            file.write(query + '\n')


###SECTION - 5. Save all the queries into a file 
# ‘queries_[DATE].txt’. a. Replace [DATE] with the current 
# date using the format ‘2023_05_04’ for May 4th, 2023.
###SECTION - 4. Create the SQL queries to insert the rows
# where ‘Delitos_fuero_comun’ is higher than 100. 
# Preferably using a transaction.
def insert_cells_into_table(dataframe, database_headers, filename):
    
    # create a list to store the insert queries
    queries = []

    # iterate over each row of the DataFrame
    for index, row in dataframe.iterrows():
        # check if 'Delitos_fuero_comun' value is higher than 100
        if row['Delitos_fuero_comun'] > 100:
            # create the insert query
            values = "', '".join(str(row[column]) for column in database_headers)
            query = f"INSERT INTO delitos ({', '.join(database_headers)}) VALUES ('{values}')"
            # append the query to the list
            queries.append(query)

    save_queries_to_file(queries, filename)


###SECTION - 3. Execute on Python the SQL query required 
# to create a table called ‘delitos’. (Drop the table if 
# exists, so there is no previous data) a. Use the same 
# column names as in the Excel file.
def create_delitos_table(database_headers, filename):

    # list of all the queries
    queries = [] 

    # adding queries to the list
    queries.append('DROP TABLE IF EXISTS delitos')
    column_definitions = ([f"{column} TEXT" for column in database_headers])
    queries.append(f"CREATE TABLE delitos ({', '.join(column_definitions)})")

    save_queries_to_file(queries, filename)

###SECTION -  2. In each cell, remove unneeded white spaces before and after the text
def clean_cell_whitespace(data):
    cleaned_data = data.copy()  # create a copy of the original DataFrame

    # iterate over each cell and clean whitespace
    for i in range(len(cleaned_data.index)):
        for j in range(len(cleaned_data.columns)):
            if isinstance(cleaned_data.iat[i, j], str):
                cleaned_data.iat[i, j] = cleaned_data.iat[i, j].strip()

    return cleaned_data

###SECTION - 1. Read the file ‘delitos_fuero_comun.xlsx’
def readXlsx(file):
    
    data = pd.read_excel(file)
    cleaned_data = clean_cell_whitespace(data)

    return cleaned_data

###SECTION - main 
def main():

    ###NOTE - constant project variables 
    file = './delitos_fuero_comun.xlsx'
    databaseSqlLite3 = 'delitos.db'
    filename = filename_creator()

    ###NOTE - process starts
    ### reding file and removing whitespaces in the same call (step 1 and 2)
    data = readXlsx(file)

    ### making the table headers list
    column_names = data.columns.tolist()
    
    ### making sql queries of step 3 y 5
    create_delitos_table(column_names, filename)

    ### making sql queries of step 4 y 5
    insert_cells_into_table(data, column_names, filename)

    ### executing the file
    execute_queries_from_file(databaseSqlLite3, filename)
    print('finnished!')

main()