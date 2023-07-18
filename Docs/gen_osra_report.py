

import xml.etree.ElementTree as ET
import pandas as pd
import datetime

# Read the XML data from trade.xml and parse it into a DataFrame (replace 'trade.xml' with the actual file path)
tree_trade = ET.parse('trade_bak.xml')
root_trade = tree_trade.getroot()

# Create lists to store the parsed trade data
quantity_list = []
side_list = []
pty_id_list = []
pty_r_list = []
sub_id_list = []
rpt_id_list = []
ultimate_clearing_firm_list = []  # List to store Ultimate Clearing Firm
entering_firm_col1_list = []  # List to store Entering Firm - Column 1
entering_firm_col2_list = []  # List to store Entering Firm - Column 2


# Function to determine Ultimate Clearing Firm
def get_ultimate_clearing_firm(sub_id, pty_r, rpt_id):
    if (sub_id in ['C', 'M', 'F']) and (pty_r == '14') and (rpt_id in rpt_id_list):
       for i in range(len(pty_r_list)):
            if pty_r_list[i] in ['18', '1'] and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None


'''
# Function to determine Entering Firm - Column 1
def get_entering_firm_col1(sub_id, pty_r, rpt_id):
    if (sub_id in ['C', 'M', 'F']) and (pty_r in ['18', '1']) and (rpt_id in rpt_id_list):
        return pty_id_list[rpt_id_list.index(rpt_id)][:3] if pty_id_list[rpt_id_list.index(rpt_id)] else None
    else:
        return None

# Function to determine Entering Firm - Column 2
def get_entering_firm_col2(sub_id, pty_r, rpt_id):
    if (sub_id in ['C', 'M', 'F']) and (pty_r in ['2', '26']) and (rpt_id in rpt_id_list):
        return pty_id_list[rpt_id_list.index(rpt_id)][:4] if pty_id_list[rpt_id_list.index(rpt_id)] else None
    else:
        return None

'''
# Function to determine Entering Firm - Column 1
def get_entering_firm_col1(sub_id, pty_r, rpt_id):
    if (sub_id in ['C', 'M', 'F']) and (rpt_id in rpt_id_list):
        for i in range(len(pty_r_list)):
            if pty_r_list[i] in ['18', '1'] and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None

# Function to determine Entering Firm - Column 2
def get_entering_firm_col2(sub_id, pty_r, rpt_id):
    if (sub_id in ['C', 'M', 'F']) and (rpt_id in rpt_id_list):
        for i in range(len(pty_r_list)):
            if pty_r_list[i] in ['2', '26'] and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None


for trd_capt_rpt in root_trade.findall('TrdCaptRpt'):
    rpt_id = trd_capt_rpt.get('RptID')
    side = trd_capt_rpt.find('RptSide').get('Side')

    for rpt_side in trd_capt_rpt.findall('RptSide'):
        side = rpt_side.get('Side')

        for pty in trd_capt_rpt.findall('RptSide/Pty'):
            pty_id = pty.get('ID')
            pty_r = pty.get('R')
            sub_id = pty.find('Sub').get('ID') if pty.find('Sub') is not None else None

            # Append the parsed data to the respective lists
            quantity_list.append(trd_capt_rpt.get('LastQty'))
            side_list.append(side)
            pty_id_list.append(pty_id)
            pty_r_list.append(pty_r)
            sub_id_list.append(sub_id)
            rpt_id_list.append(rpt_id)

            # Determine the Ultimate Clearing Firm
            ultimate_clearing_firm = get_ultimate_clearing_firm(sub_id, pty_r, rpt_id)
            ultimate_clearing_firm_list.append(ultimate_clearing_firm)

            # Determine the Entering Firm - Column 1
            entering_firm_col1 = get_entering_firm_col1(sub_id, pty_r, rpt_id)
            entering_firm_col1_list.append(entering_firm_col1)

            # Determine the Entering Firm - Column 2
            entering_firm_col2 = get_entering_firm_col2(sub_id, pty_r, rpt_id)
            entering_firm_col2_list.append(entering_firm_col2)

# Create the DataFrame
trade_data_frame = pd.DataFrame({
    'Quantity': quantity_list,
    'Side': side_list,
    'Pty ID': pty_id_list,
    'Pty R': pty_r_list,
    'Sub ID': sub_id_list,
    'RptID': rpt_id_list,
    'Ultimate Clearing Firm': ultimate_clearing_firm_list,
    'Entering Firm - Column 1': entering_firm_col1_list,
    'Entering Firm - Column 2': entering_firm_col2_list
})




# Filter rows where at least one of Ultimate Clearing Firm, Entering Firm - Column 1, or Entering Firm - Column 2 is not None
filtered_trade_data_frame = trade_data_frame[
    trade_data_frame[['RptID','Sub ID','Side','Ultimate Clearing Firm', 'Entering Firm - Column 1', 'Entering Firm - Column 2']].notna().any(axis=1)
]

# Group the filtered DataFrame and aggregate the values for Ultimate Clearing Firm, Entering Firm - Column 1, and Entering Firm - Column 2
grouped_trade_data_frame = filtered_trade_data_frame.groupby(['Side', 'Sub ID', 'RptID'], as_index=False).agg({
    'Ultimate Clearing Firm': 'first',
    'Entering Firm - Column 1': 'first',
    'Entering Firm - Column 2': 'first',
    
})

print(grouped_trade_data_frame)


# Replace 'None' with a placeholder value (e.g., 'Unknown')
trade_data_frame.fillna('Unknown', inplace=True)

# Group the data by the desired columns and calculate the count for each group
pivoted_trade_data_frame = trade_data_frame.groupby(['Side', 'Sub ID', 'Ultimate Clearing Firm', 'Entering Firm - Column 1', 'Entering Firm - Column 2'], as_index=False).size()
#pivoted_trade_data_frame = pivoted_trade_data_frame.reset_index(name='Total Qty')
pivoted_trade_data_frame.rename(columns={'size': 'Total Qty'}, inplace=True)

# Print the grouped trade data DataFrame
print(pivoted_trade_data_frame)

# Generate the timestamp for the file name up to minutes
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

# Write the grouped_trade_data_frame and pivoted_trade_data_frame to an Excel file with separate sheets
output_file_name = f'grouped_and_pivoted_trade_data_{timestamp}.xlsx'

with pd.ExcelWriter(output_file_name) as writer:
    grouped_trade_data_frame.to_excel(writer, sheet_name='Grouped Trade Data', index=False)
    pivoted_trade_data_frame.to_excel(writer, sheet_name='Pivoted Trade Data', index=False)

print(f"Data has been written to {output_file_name}")




