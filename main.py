import pandas as pd

### @autor Hossein Yahyazadeh
### pcd systems challenge


# 3. Execute on Python the SQL query required to create a table called ‘delitos’.
# (Drop the table if exists, so there is no previous data)
# a. Use the same column names as in the Excel file.

# 4. Create the SQL queries to insert the rows where ‘Delitos_fuero_comun’ is
# higher than 100. Preferably using a transaction.

# 5. Save all the queries into a file ‘queries_[DATE].txt’.
# a. Replace [DATE] with the current date using the format ‘2023_05_04’
# for May 4th, 2023.

# 6. Execute the queries to the DB.

# 2. In each cell, remove unneeded white spaces before and after the text
def clean_cell_whitespace(data):
    cleaned_data = data.copy()  # Create a copy of the original DataFrame

    # Iterate over each cell and clean whitespace
    for i in range(len(cleaned_data.index)):
        for j in range(len(cleaned_data.columns)):
            if isinstance(cleaned_data.iat[i, j], str):
                cleaned_data.iat[i, j] = cleaned_data.iat[i, j].strip()

    return cleaned_data

# 1. Read the file ‘delitos_fuero_comun.xlsx’
def readXlsx(file):
    
    data = pd.read_excel(file)
    cleaned_data = clean_cell_whitespace(data)

    print(cleaned_data)
    return clean_cell_whitespace

###SECTION - main 
def main():

    ###NOTE - constant project variables 
    file = './delitos_fuero_comun.xlsx'


    readXlsx(file)

main()