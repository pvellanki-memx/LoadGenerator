import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import datetime

def get_ultimate_clearing_firm(sub_id, pty_r, rpt_id):
    if sub_id in ['C', 'M', 'F']:
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '14' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None

# Function to determine Entering Firm - Column 1
def get_entering_firm_col1(sub_id, pty_r, rpt_id):
    if sub_id in ['C', 'M', 'F'] and rpt_id in rpt_id_list:
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '18' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '1' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None

# Function to determine Entering Firm - Column 2
def get_entering_firm_col2(sub_id, pty_r, rpt_id):
    if sub_id in ['C', 'M', 'F'] and rpt_id in rpt_id_list:
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '2' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
        for i in range(len(pty_r_list)):
            if pty_r_list[i] == '26' and rpt_id_list[i] == rpt_id:
                return pty_id_list[i] if pty_id_list[i] else None
    return None


# Initialize an empty DataFrame to store the parsed trade data
trade_data_frame = pd.DataFrame()

# Create lists to store the parsed trade data
batch_size = 10000
batch_data = []
processed_elements = 0


# Read the XML data from trade.xml and parse it into NumPy arrays (replace 'trade.xml' with the actual file path)
print("Parsing the XML data...")
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

# Loop through the TrdCaptRpt elements and parse the data
print("Processing the XML data...")
for trd_capt_rpt in root_trade.findall('.//TrdCaptRpt'):
    rpt_id = trd_capt_rpt.get('RptID')
    for rpt_side in trd_capt_rpt.findall('RptSide'):
        side = rpt_side.get('Side')
        for pty in rpt_side.findall('Pty'):
            pty_id = pty.get('ID')
            pty_r = pty.get('R')
            sub_id = pty.find('Sub').get('ID') if pty.find('Sub') is not None else None

            # Append the parsed data to the respective lists
            quantity_list.append(int(trd_capt_rpt.get('LastQty')))  # Convert quantity to integer
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

    # Process the data in batches (same as before)
    if len(quantity_list) >= batch_size:
        print(f"Processing batch {processed_elements // batch_size}")
        batch_df = process_batch({
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

        if processed_elements == 0:
            # Create the DataFrame for the first batch
            trade_data_frame = pd.DataFrame(batch_df)
        else:
            # Append to the DataFrame for subsequent batches
            trade_data_frame = trade_data_frame.append(pd.DataFrame(batch_df))

        # Clear the lists for the next batch
        quantity_list.clear()
        side_list.clear()
        pty_id_list.clear()
        pty_r_list.clear()
        sub_id_list.clear()
        rpt_id_list.clear()
        ultimate_clearing_firm_list.clear()
        entering_firm_col1_list.clear()
        entering_firm_col2_list.clear()

    # Process the data in batches
    if len(quantity_list) >= batch_size:
        # ... (The batch processing and DataFrame creation remain unchanged as before)

        # Clear the lists for the next batch
        quantity_list.clear()
        side_list.clear()
        pty_id_list.clear()
        pty_r_list.clear()
        sub_id_list.clear()
        rpt_id_list.clear()
        ultimate_clearing_firm_list.clear()
        entering_firm_col1_list.clear()
        entering_firm_col2_list.clear()

# Process the remaining data (if any)
if quantity_list:
    print(f"Processing the last batch {processed_elements // batch_size + 1}")
    batch_df = process_batch({
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

    if processed_elements == 0:
        # Create an empty DataFrame if no data is processed
        trade_data_frame = pd.DataFrame()
    else:
        # Append to the DataFrame for the last batch
        trade_data_frame = trade_data_frame.append(pd.DataFrame(batch_df))

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
