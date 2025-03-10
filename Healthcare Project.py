import pandas as pd
import numpy as np
import os
print(os.getcwd())
"""1) Import the csv file"""
healthcare_dataset = pd.read_csv('C:\\Users\\Michael\\Desktop\\Data Analysis Projects\\Healthcare Project\\healthcare_dataset.csv')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

"""2) Initial inspections"""
# print(type(healthcare_dataset))
# healthcare_dataset.info()
# print(healthcare_dataset.head())
# print(healthcare_dataset.describe())

"""Clean the dataset"""
"""2) Column renaming"""
healthcare_dataset.columns = healthcare_dataset.columns.str.lower().str.replace(' ', '_')
"""3) Fix Name column"""
healthcare_dataset['name'] = healthcare_dataset['name'].str.title()
# print(healthcare_dataset.head(5))
"""4) Check for nulls"""
# print(healthcare_dataset.isnull().sum())
"""5) Check for duplicates"""
# print(f"Number of duplicate rows: {healthcare_dataset.duplicated().sum()}")
duplicates = healthcare_dataset[healthcare_dataset.duplicated()] # Found 534 duplicates
# print(duplicates.head(10))
duplicate_rows = healthcare_dataset[healthcare_dataset.duplicated(keep=False)]
# print(duplicate_rows.sort_values(by=['name', 'age']).head(20))
# duplicate_rows.to_excel('C:\\Users\\Michael\\Desktop\\Data Analysis Projects\\Healthcare Project\\duplicate_rows.xlsx', index=False) # exported to xlsx for better view
# print("Duplicate rows have been exported to 'duplicate_rows.xlsx'.")
identical = duplicate_rows.drop_duplicates().shape[0] == 1 # Checking if all duplicate rows are identical, found that now all rows are identical
# print(f'Are all duplicate rows identical? {identical}')
differing_columns = duplicate_rows.drop_duplicates() # unique rows within the duplicate rows
# print("Columns with differing values in duplicate rows:")
# print(differing_columns)
# differing_columns.to_excel('C:\\Users\\Michael\\Desktop\\Data Analysis Projects\\Healthcare Project\\differing_columns.xlsx', index=False)
# print("Columns with differences have been exported to 'differing_columns.xlsx'.")
duplicate_groups = duplicate_rows.groupby(['name', 'age', 'medical_condition']).size() # Identify how duplicates are grouped
# print(duplicate_groups)
differing_in_duplicates = duplicate_rows.merge(differing_columns,how='inner')
# print(differing_in_duplicates)
# differing_in_duplicates.to_excel('C:\\Users\\Michael\\Desktop\\Data Analysis Projects\\Healthcare Project\\differing_in_duplicates.xlsx', index=False)
# print("Exported differing_in_duplicates to 'differing_in_duplicates.xlsx'")

cleaned_dataset = healthcare_dataset.drop_duplicates() # Drop the duplicate rows entirely from the dataset
cleaned_dataset = pd.concat([cleaned_dataset,differing_in_duplicates]).drop_duplicates() # Add the unique rows from differing_columns
# cleaned_dataset.to_csv('C:\\Users\\Michael\\Desktop\\Data Analysis Projects\\Healthcare Project\\cleaned_healthcare_dataset.csv', index=False)

"""6) Data types"""
# Check current data types and convert columns to the correct data type if needed
# print(cleaned_dataset.info())

# Convert date columns to datetime format
cleaned_dataset['date_of_admission'] = pd.to_datetime(cleaned_dataset['date_of_admission'])
cleaned_dataset['discharge_date'] = pd.to_datetime(cleaned_dataset['discharge_date'])

# Convert categorical columns to category type

categorical_columns = [
    'gender', 'blood_type', 'medical_condition', 'doctor', 'hospital', 'insurance_provider', 'admission_type',
    'medication', 'test_results'
]

for col in categorical_columns:
    cleaned_dataset[col] = cleaned_dataset[col].astype('category')

# Check the updated data
# print(cleaned_dataset.info())

"""7) Billing amount decimal precision"""
# print(cleaned_dataset['billing_amount'].head(10))
cleaned_dataset['billing_amount'] = cleaned_dataset['billing_amount'].round(2)

"""Final review and export"""
# print(cleaned_dataset['billing_amount'].head(10))
# print(cleaned_dataset.head())
# print(cleaned_dataset.info())

# cleaned_dataset.to_csv('C:\\Users\\Michael\\Desktop\\Data Analysis Projects\\Healthcare Project\\healthcare_dataset_final.csv', index=False)
# print("Final cleaned dataset saved as 'healthcare_dataset_final.csv'")

# cleaned_dataset.to_excel('C:\\Users\\Michael\\Desktop\\Data Analysis Projects\\Healthcare Project\\healthcare_dataset_final.xlsx', index=False)


