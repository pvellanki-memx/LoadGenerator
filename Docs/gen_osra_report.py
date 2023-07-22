import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import datetime

# Function to determine Ultimate Clearing Firm
def get_ultimate_clearing_firm(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids):
    if sub_id in ['C', 'M', 'F']:
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '14' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None

# Function to determine Entering Firm - Column 1
def get_entering_firm_col1(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids):
    if sub_id in ['C', 'M', 'F'] and rpt_id in rpt_id_list:
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '18' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '1' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None

# Function to determine Entering Firm - Column 2
def get_entering_firm_col2(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids):
    if sub_id in ['C', 'M', 'F'] and rpt_id in rpt_id_list:
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '2' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '26' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None

def process_batch(batch_data, sub_id_to_rpt_ids):
    quantity_list = batch_data['Quantity']
    side_list = batch_data['Side']
    pty_id_list = batch_data['Pty ID']
    pty_r_list = batch_data['Pty R']
    sub_id_list = batch_data['Sub ID']
    rpt_id_list = batch_data['RptID']
    ultimate_clearing_firm_list = []
    entering_firm_col1_list = []
    entering_firm_col2_list = []

    for i in range(len(quantity_list)):
        rpt_id = rpt_id_list[i]
        sub_id = sub_id_list[i]
        pty_r = pty_r_list[i]

        ultimate_clearing_firm = get_ultimate_clearing_firm(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids)
        ultimate_clearing_firm_list.append(ultimate_clearing_firm)

        entering_firm_col1 = get_entering_firm_col1(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids)
        entering_firm_col1_list.append(entering_firm_col1)

        entering_firm_col2 = get_entering_firm_col2(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids)
        entering_firm_col2_list.append(entering_firm_col2)

    batch_df = {
        'Quantity': np.array(quantity_list),
        'Side': np.array(side_list),
        'Pty ID': np.array(pty_id_list),
        'Pty R': np.array(pty_r_list),
        'Sub ID': np.array(sub_id_list),
        'RptID': np.array(rpt_id_list),
        'Ultimate Clearing Firm': np.array(ultimate_clearing_firm_list),
        'Entering Firm - Column 1': np.array(entering_firm_col1_list),
        'Entering Firm - Column 2': np.array(entering_firm_col2_list)
    }

    return batch_df


# Read the XML data from trade.xml and parse it into NumPy arrays (replace 'trade.xml' with the actual file path)
print("Parsing the XML data...")
tree_trade = ET.parse('trade_pv.xml')
root_trade = tree_trade.getroot()

# Define the namespace
ns = {'fixml': 'http://www.fixprotocol.org/FIXML-4-4'}

# Assuming you have sub_id_to_rpt_ids as a dictionary mapping sub_id to rpt_id (replace {} with the actual data)
sub_id_to_rpt_ids = {}

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

# Loop through the TrdCaptRpt elements and parse the data
print("Processing the XML data...")
for trd_capt_rpt in root_trade.findall('.//fixml:TrdCaptRpt', ns):
    rpt_id = trd_capt_rpt.get('RptID')
    for rpt_side in trd_capt_rpt.findall('fixml:RptSide', ns):
        side = rpt_side.get('Side')
        for pty in rpt_side.findall('fixml:Pty', ns):
            pty_id = pty.get('ID')
            pty_r = pty.get('R')
            sub_id = pty.find('fixml:Sub', ns).get('ID') if pty.find('fixml:Sub', ns) is not None else None

            # Append the parsed data to the respective lists
            quantity_list.append(int(trd_capt_rpt.get('LastQty')))  # Convert quantity to integer
            side_list.append(side)
            pty_id_list.append(pty_id)
            pty_r_list.append(pty_r)
            sub_id_list.append(sub_id)
            rpt_id_list.append(rpt_id)

            # Determine the Ultimate Clearing Firm
            ultimate_clearing_firm = get_ultimate_clearing_firm(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids)
            ultimate_clearing_firm_list.append(ultimate_clearing_firm)

            # Determine the Entering Firm - Column 1
            entering_firm_col1 = get_entering_firm_col1(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids)
            entering_firm_col1_list.append(entering_firm_col1)

            # Determine the Entering Firm - Column 2
            entering_firm_col2 = get_entering_firm_col2(sub_id, pty_r, rpt_id, sub_id_to_rpt_ids)
            entering_firm_col2_list.append(entering_firm_col2)

# Create a DataFrame for the parsed data
trade_data_frame = pd.DataFrame({
    'Quantity': np.array(quantity_list),
    'Side': np.array(side_list),
    'Pty ID': np.array(pty_id_list),
    'Pty R': np.array(pty_r_list),
    'Sub ID': np.array(sub_id_list),
    'RptID': np.array(rpt_id_list),
    'Ultimate Clearing Firm': np.array(ultimate_clearing_firm_list),
    'Entering Firm - Column 1': np.array(entering_firm_col1_list),
    'Entering Firm - Column 2': np.array(entering_firm_col2_list)
})

# Filter rows where at least one of Ultimate Clearing Firm, Entering Firm - Column 1, or Entering Firm - Column 2 is not None
print("Filtering the DataFrame...")
filtered_trade_data_frame = trade_data_frame[
    trade_data_frame[['RptID', 'Quantity', 'Sub ID', 'Side', 'Ultimate Clearing Firm', 'Entering Firm - Column 1', 'Entering Firm - Column 2']].notna().any(axis=1)
]

# Group the filtered DataFrame and aggregate the values for Ultimate Clearing Firm, Entering Firm - Column 1, and Entering Firm - Column 2
print("Grouping the DataFrame...")
grouped_trade_data_frame = filtered_trade_data_frame.groupby(['Side', 'Sub ID', 'RptID'], as_index=False).agg({
    'Ultimate Clearing Firm': 'first',
    'Entering Firm - Column 1': 'first',
    'Entering Firm - Column 2': 'first',
    'Quantity': 'sum'
})

# Generate the timestamp for the file name up to minutes
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
output_file_name = f'trade_report_{timestamp}.xlsx'

with pd.ExcelWriter(output_file_name) as writer:
    grouped_trade_data_frame.to_excel(writer, sheet_name='Pivoted Trade Data', index=False)

print(f"Processing completed. Result saved to '{output_file_name}'.")
