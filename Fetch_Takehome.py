#install necessary packages
import pandas as pd
import numpy as np
import pandasql as psql

#load datasets
df_prod = pd.read_csv('/Users/samanthaheerlein/Downloads/PRODUCTS_TAKEHOME.csv')
df_trans = pd.read_csv('/Users/samanthaheerlein/Downloads/TRANSACTION_TAKEHOME.csv')
df_user= pd.read_csv('/Users/samanthaheerlein/Downloads/USER_TAKEHOME.csv')

pd.set_option('display.max_columns', 100)

#EXERCISE 1
#create report of data quality
def data_quality_report(df):
    
    #review top 10 rows
    print(df.head())

    #review column names and data types
    print('Missing Data:')
    print(df.dtypes)

    #check for missing data
    print('Missing Data:')
    missing_data = df.isnull().sum()
    print(missing_data)
    missing_percentage = (missing_data / len(df)) * 100
    print(f'Percentage of Missing Data:\n{missing_percentage}\n')

    #check for duplicate rows
    print(f'Number of Duplicate Rows: {df.duplicated().sum()}\n')

    #check for outliers
    #include if statement to avoid errors on tables without numeric data types
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty:
        print ('No numeric columns available for description.')
        return
    print(numeric_df.describe())
    return

print('Product Data Quality Report')
data_quality_report(df_prod)
print('Transaction Data Quality Report')
data_quality_report(df_trans)
print('User Data Quality Report')
data_quality_report(df_user)

def referential_integrity_test(df_primary, df_foreign, primary_key, foreign_key):
    # Identify foreign key values that don't exist in the primary database
    invalid_references = df_foreign[~df_foreign[foreign_key].isin(df_primary[primary_key])]
    
    if invalid_references.empty:
        print ('Referential integrity is valid: All foreign key values exist in the primary key.')
        return
    print(f'Referential integrity is broken: {len(invalid_references)} invalid foreign key values found.')
    return


referential_integrity_test(df_user, df_trans, 'ID', 'USER_ID')
referential_integrity_test(df_prod, df_trans, 'BARCODE', 'BARCODE')


#EXCERCISE 2
#Since I already have a python script, I decided to use pandasql for exercise 2 but have worked in various other SQL editors in the past
#for all excersises, I assumed the quality of the data as is is sufficent, and did not make any changes to account for data quality errors found in part 1

#What are the top 5 brands by receipts scanned among users 21 and over?
#assumption: I filtered out brand as null since it was otherwise appearing in the top 5

query1 = query = '''
SELECT 
    p.BRAND,
    COUNT(t.RECEIPT_ID) AS RECEIPT_COUNT
FROM 
    df_user u
JOIN 
    df_trans t ON u.ID = t.USER_ID
JOIN 
    df_prod p ON t.BARCODE = p.BARCODE
WHERE 
    julianday('now') - julianday(u.BIRTH_DATE) / 365.25 >= 21 and p.BRAND <> ''
GROUP BY 
    p.BRAND
ORDER BY 
    RECEIPT_COUNT DESC
LIMIT 5;
'''

result1 = psql.sqldf(query1, locals())
print(f'Top 5 brands by receipts scanned among users 21 and over:\n {result1}')

#What are the top 5 brands by sales among users that have had their account for at least six months?
#assumption: used 183 days to represent approximately 6 months

query2 = query = '''
SELECT 
    p.BRAND,
    SUM(t.FINAL_SALE * t.FINAL_QUANTITY) AS TOTAL_SALES
FROM 
    df_user u
JOIN 
    df_trans t ON u.ID = t.USER_ID
JOIN 
    df_prod p ON t.BARCODE = p.BARCODE
WHERE 
    julianday('now') - julianday(u.CREATED_DATE) >= 183 and p.BRAND <> ''
GROUP BY 
    p.BRAND
ORDER BY 
    TOTAL_SALES DESC
LIMIT 5;
'''

result2 = psql.sqldf(query2, locals())
print(f'Top 5 brands by sales among users that have had their account for at least six months:\n {result2}')

#Who are Fetch’s power users?
#assumption: given the absence of point-earning data, I have defined a power user as someone who scans the most reciepts
#I selected reciept scans over total transaction value as more scans means more interaction with the Fetch app than scanning a single high value receipt

query3 = query = '''
SELECT 
    u.ID, 
    COUNT(t.RECEIPT_ID) AS RECEIPT_COUNT
FROM 
    df_user u
JOIN 
    df_trans t ON u.ID = t.USER_ID
GROUP BY 
    u.ID
ORDER BY 
    RECEIPT_COUNT DESC
LIMIT 10;
'''

result3 = psql.sqldf(query3, locals())
print(f'Top 10 power users:\n {result3}')
