import pandas as pd
from datetime import datetime, timedelta
from openpyxl import Workbook


# Load the '23-10 Post-Move Data' dataset (replace 'your_data.csv' with the actual file path)
data = pd.read_csv('Postmove_summary.csv')

OCC_Member_Directory = pd.read_csv('occ_member_directory.csv') 

# Define the conditions for each formula using the column name mappings
condition_1 = (data['Pty_R'] == 1) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 0) & (data['ORFInd'].isna() | (data['ORFInd'] == ''))
condition_2 = (data['Pty_R'] == 1) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 0) & (data['ORFInd'] == 'Y')
condition_3 = (data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 0) & (data['ORFInd'].isna() | (data['ORFInd'] == ''))
condition_4 = (data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 0) & (data['ORFInd'] == 'Y')

# Create new columns based on the conditions
data['-From'] = -data['Total_Quantity'].where(condition_1, 0)
data['+From ORFInd'] = data['Total_Quantity'].where(condition_2, 0)
data['+To'] = data['Total_Quantity'].where(condition_3, 0)
data['-To ORF Ind'] = -data['Total_Quantity'].where(condition_4, 0)

# Group the data by 'Ultimate_Clearing_Firm' (column D) and calculate the sums for each of the new columns
result_minus_from = data.groupby('Ultimate_Clearing_Firm')['-From'].sum()
result_plus_from_orf_ind = data.groupby('Ultimate_Clearing_Firm')['+From ORFInd'].sum()
result_plus_to = data.groupby('Ultimate_Clearing_Firm')['+To'].sum()
result_minus_to_orf_ind = data.groupby('Ultimate_Clearing_Firm')['-To ORF Ind'].sum()

# Create a new DataFrame to store the results
results_df = pd.DataFrame({'-From': result_minus_from, '+From ORFInd': result_plus_from_orf_ind, '+To': result_plus_to, '-To ORF Ind': result_minus_to_orf_ind})

results_df['Total_New'] = results_df.sum(axis=1)#

#print(results_df)
'''
# Define the conditions for the second set of formulas
condition_1_cancel_from = (data['Pty_R'] == 1) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'].isin([1, 4])) & (data['ORFInd'].isna() | (data['ORFInd'] == ''))
condition_2_cancel_from_orfind = ((data['Pty_R'] == 1) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 1) & (data['ORFInd'] == 'Y')) ^ ((data['Pty_R'] == 1) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 4) & (data['ORFInd'] == 'Y'))
condition_3_cancel_to = ((data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 1) & (data['ORFInd'].isna() | (data['ORFInd'] == ''))) ^ ((data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 4) & (data['ORFInd'] == 'Y'))
condition_4_cancel_to_orfind = ((data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 1) & (data['ORFInd'] == 'Y')) ^ ((data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'] == 4) & (data['ORFInd'] == 'Y'))
'''

# Define the conditions for the second set of formulas
condition_1_cancel_from = (data['Pty_R'] == 1) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'].isin([1, 4])) & (data['ORFInd'].isna() | (data['ORFInd'] == ''))
condition_2_cancel_from_orfind = (data['Pty_R'] == 1) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'].isin([1, 4])) & (data['ORFInd'] == 'Y')
condition_3_cancel_to = (data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'].isin([1, 4])) & (data['ORFInd'].isna() | (data['ORFInd'] == ''))
condition_4_cancel_to_orfind = (data['Pty_R'] == 18) & (data['Sub_ID'] == 'C') & (data['TRANS_TYPE'].isin([1, 4])) & (data['ORFInd'] == 'Y')


# Create new columns based on the conditions
data['cancel-From'] = data['Total_Quantity'].where(condition_1_cancel_from, 0)
data['cancel+From ORFInd'] = -data['Total_Quantity'].where(condition_2_cancel_from_orfind, 0)
data['cancel+To'] = -(data['Total_Quantity'].where(condition_3_cancel_to, 0))
data['cancel-To ORF Ind'] = data['Total_Quantity'].where(condition_4_cancel_to_orfind, 0)


# Group the data by 'Ultimate_Clearing_Firm' (column D) and calculate the sums for each of the new columns
result_cancel_from = data.groupby('Ultimate_Clearing_Firm')['cancel-From'].sum()
result_cancel_from_orf_ind = data.groupby('Ultimate_Clearing_Firm')['cancel+From ORFInd'].sum()
result_cancel_to = data.groupby('Ultimate_Clearing_Firm')['cancel+To'].sum()
result_cancel_to_orf_ind = data.groupby('Ultimate_Clearing_Firm')['cancel-To ORF Ind'].sum()

# Create a new DataFrame to store the results
results_df1 = pd.DataFrame({'cancel-From': result_cancel_from, 'cancel+From ORFInd': result_cancel_from_orf_ind, 'cancel+To': result_cancel_to, 'cancel-To': result_cancel_to_orf_ind})

results_df1['Total_Cancel'] = results_df1.sum(axis=1)

# Print the updated results DataFrame
#print(results_df1)

# Combine the results_df and results_df1 dataframes
#combined_df = results_df.join(results_df1, on='Ultimate_Clearing_Firm', lsuffix='_left', rsuffix='_right')
combined_df = results_df.join(results_df1, on='Ultimate_Clearing_Firm', lsuffix='_left', rsuffix='_right')

# Calculate 'Population Post Move Transfers' as the sum of 'Total_New' and 'Total_Cancel'
combined_df['Population Post Move Transfers'] = combined_df['Total_New'] + combined_df['Total_Cancel']

# Print the combined results DataFrame


combined_df.reset_index(inplace=True)

# Define the lookup_member_apps function
def lookup_member_apps(value):
    if pd.isna(value):
        return "N"
    
    result = OCC_Member_Directory['Member - Apps'].loc[OCC_Member_Directory['Number for lookup'] == value]
    if not result.empty:
        return result.iloc[0]
    else:
        return "N"

combined_df['MEMX Member'] = combined_df['Ultimate_Clearing_Firm'].apply(lookup_member_apps)

# Define a custom function to calculate 'MEMX Post-Move Transfers' based on conditions
def calculate_memx_post_moves(row):
    if row['MEMX Member'] == 'Y':
        return row['Population Post Move Transfers']
    else:
        return 0

combined_df['MEMX Post-Move Transfers'] = combined_df.apply(calculate_memx_post_moves, axis=1)



# Print the combined results DataFrame
##print(combined_df)


#Function ot return member or not

#import pandas as pd

# Load the OCC Member Directory DataFrame
#OCC_Member_Directory = pd.read_csv('occ_member_directory.csv')  # Replace with the correct file path

# Load the summary_trade.csv into a DataFrame
trade_df = pd.read_csv('summary_trade.csv')

# Define a function to convert 'Ultimate_Clearing_Firm' to int and handle NaN
def convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

# Apply the conversion function to 'Ultimate_Clearing_Firm' column
trade_df['Ultimate_Clearing_Firm'] = trade_df['Ultimate_Clearing_Firm'].apply(convert_to_int)

# Define the function to calculate adj_total
def calculate_adj_total(row):
    if row['TRANS_TYPE'] in [1, 4]:
        return -row['Total_Quantity']
    else:
        return row['Total_Quantity']

# Apply the calculate_adj_total function to create the adj_total column
trade_df['adj_total'] = trade_df.apply(calculate_adj_total, axis=1)

# Define the lookup_member_apps function
def lookup_member_apps(value):
    if pd.isna(value):
        return "N"
    
    result = OCC_Member_Directory['Member - Apps'].loc[OCC_Member_Directory['Number for lookup'] == value]
    if not result.empty:
        return result.iloc[0]
    else:
        return "N"

# Apply the lookup_member_apps function to create the 'Ultimate_Clearing_Firm_Member' column
trade_df['Ultimate_Clearing_Firm_Member'] = trade_df['Ultimate_Clearing_Firm'].apply(lookup_member_apps)

# Apply the lookup_member_apps function to create the 'Entering_Firm_Col1_Member' column
trade_df['Entering_Firm_Col1_Member'] = trade_df['Entering_Firm_Col1'].apply(lookup_member_apps)

# Add 'Population ORF Ultimate CC' column
trade_df['Population ORF Ultimate CC'] = trade_df.apply(lambda row: row['Entering_Firm_Col1'] if pd.isna(row['Ultimate_Clearing_Firm']) else row['Ultimate_Clearing_Firm'], axis=1)


# Create the 'MEMX ORF Member CC' column using the formula
trade_df['MEMX ORF Member CC'] = trade_df.apply(lambda row: row['Ultimate_Clearing_Firm'] if row['Ultimate_Clearing_Firm_Member'] == 'Y' else (row['Entering_Firm_Col1'] if row['Entering_Firm_Col1_Member'] == 'Y' else ''), axis=1)



def calculate_memx_total_contracts(row):
    if row['EXCH'] == 'MXOP' and row['Sub_ID'] == 'C':
        return row['adj_total']
    elif row['Ultimate_Clearing_Firm_Member'] == 'Y' and row['Sub_ID'] == 'C':
        return row['adj_total']
    elif row['Ultimate_Clearing_Firm_Member'] == 'N' and row['Entering_Firm_Col1_Member'] == 'Y' and row['Sub_ID'] == 'C':
        return row['adj_total']
    else:
        return 0

# Apply the calculate_memx_total_contracts function to create the 'MEMX Total Contracts' column
trade_df['MEMX Total Contracts'] = trade_df.apply(calculate_memx_total_contracts, axis=1)



# Get unique values from 'Ultimate_Clearing_Firm' and 'Entering_Firm_Col1' in trade_df
unique_values_trade = set(trade_df['Ultimate_Clearing_Firm'].dropna()).union(trade_df['Entering_Firm_Col1'].dropna()) 


# Get unique values from 'Ultimate_Clearing_Firm' in combined_df
unique_values_combined = set(combined_df['Ultimate_Clearing_Firm'].dropna())

# Combine unique values from both DataFrames
unique_values = unique_values_trade.union(unique_values_combined)

# Create a DataFrame from the unique values
unique_df = pd.DataFrame({'Unique_Column': list(unique_values)})

def lookup_member_apps(value):
    if pd.isna(value):
        return "N"
    
    result = OCC_Member_Directory['Member - Apps'].loc[OCC_Member_Directory['Number for lookup'] == value]
    if not result.empty:
        return result.iloc[0]
    else:
        return "N"

# Apply the lookup_member_apps function to create the 'Ultimate_Clearing_Firm_Member' column
unique_df['Is_MEMX_Member'] = unique_df['Unique_Column'].apply(lookup_member_apps)

# Define a function to calculate MEMX ORF Trade Contracts
def calculate_memx_orf_trade_contracts(value):
    matching_rows = trade_df[trade_df['MEMX ORF Member CC'] == value]
    return matching_rows['MEMX Total Contracts'].sum()

# Calculate MEMX ORF Trade Contracts and add them to unique_df
unique_df['MEMX ORF Trade Contracts'] = unique_df['Unique_Column'].apply(calculate_memx_orf_trade_contracts)

# Define a function to calculate MEMX ORF Post-Move Contracts
def calculate_memx_orf_post_move_contracts(value):
    matching_rows = combined_df[combined_df['Ultimate_Clearing_Firm'] == value]
    return matching_rows['MEMX Post-Move Transfers'].sum()

# Calculate MEMX ORF Post-Move Contracts and add them to unique_df
unique_df['MEMX ORF Post-Move Contracts'] = unique_df['Unique_Column'].apply(calculate_memx_orf_post_move_contracts)

unique_df['Total ORF Contracts'] = unique_df['MEMX ORF Post-Move Contracts'] + unique_df['MEMX ORF Trade Contracts']

# Print or use the updated unique_df with the new column
#print(unique_df)



# Define a function to calculate MEMX ORF Trade Contracts
def calculate_non_memx_orf_trade_contracts(value):
    matching_rows = trade_df[trade_df['Population ORF Ultimate CC'] == value]
    return matching_rows['MEMX Total Contracts'].sum()

# Calculate MEMX ORF Trade Contracts and add them to unique_df
unique_df['NON MEMX ORF Trade Contracts'] = unique_df['Unique_Column'].apply(calculate_non_memx_orf_trade_contracts)


# Define a function to calculate MEMX ORF Post-Move Contracts
def calculate_non_memx_orf_post_move_contracts(value):
    matching_rows = combined_df[combined_df['Ultimate_Clearing_Firm'] == value]
    return matching_rows['MEMX Post-Move Transfers'].sum()

# Calculate MEMX ORF Post-Move Contracts and add them to unique_df
unique_df['NON MEMX ORF Post-Move Contracts'] = unique_df['Unique_Column'].apply(calculate_non_memx_orf_post_move_contracts)

unique_df['Total ALL ORF Contracts'] = unique_df['NON MEMX ORF Post-Move Contracts'] + unique_df['NON MEMX ORF Trade Contracts']

# Define the static variable ORF_Rate
ORF_Rate = 0.0015

# Add a new column "MEMX ORF" to unique_df
unique_df['MEMX ORF'] = ORF_Rate * unique_df['Total ORF Contracts']

# Add a new column "Total ORF" to unique_df
unique_df['Total ORF'] = ORF_Rate * unique_df['Total ALL ORF Contracts']

# Define the lookup_member_apps function
def lookup_member_name(value):
    if pd.isna(value):
        return "NA"
    
    result = OCC_Member_Directory['Trimmed'].loc[OCC_Member_Directory['Number for lookup'] == value]
    if not result.empty:
        return result.iloc[0]
    else:
        return "NA"

unique_df['CC Name'] = unique_df['Unique_Column'].apply(lookup_member_name)

unique_df = unique_df.sort_values(by='Unique_Column', ascending=True)


# Get the current date
current_date = datetime.now()

# Calculate the first day of the current month
first_day_of_current_month = current_date.replace(day=1)

# Calculate the first day of the previous month by subtracting one day from the first day of the current month
first_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

# Get the year and month of the previous month
previous_month_year = first_day_of_previous_month.year
previous_month = first_day_of_previous_month.month

# Create the "yyyy-mm" format
file_name_format = f"Monthly_ORF_Fee_{previous_month_year:04d}-{previous_month:02d}"

# Define the file name
#file_name = f"{file_name_format}.csv"

# Replace 'output_directory' with the desired directory path where you want to save the CSV file.
#output_directory = '/path/to/your/directory'

# Combine the output directory and file name
#output_file_path = f"{output_directory}/{file_name}"

#unique_df.to_csv(output_file_path, index=False)
#unique_df.to_csv(file_name, index=False)

#print(f"Monthly ORF Fee Calc saved to {output_file_path}")

file_name = f"{file_name_format}.xlsx"


# Create a new Excel writer
with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    # Write 'trade_df' to the 'Trade Data' sheet
    trade_df.to_excel(writer, sheet_name='Trade Data', index=False)
    
    # Write 'combined_df' to the 'Combined Data' sheet
    combined_df.to_excel(writer, sheet_name='Postmove Data', index=False)
    
    # Write 'unique_df' to the 'Unique Data' sheet
    unique_df.to_excel(writer, sheet_name='ORF Data', index=False)

print(f"Monthly ORF Fee Calc saved to {file_name}")

#print(unique_df.head(20))
#print(trade_df.head(20))
#print(combined_df.head(20))





