import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import datetime


# Function to determine Ultimate Clearing Firm
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


def process_batch(batch_data):
    quantity_list = []
    side_list = []
    pty_id_list = []
    pty_r_list = []
    sub_id_list = []
    rpt_id_list = []
    ultimate_clearing_firm_list = []
    entering_firm_col1_list = []
    entering_firm_col2_list = []

    for trd_capt_rpt in batch_data:
        rpt_id = trd_capt_rpt.get('RptID')
        for rpt_side in trd_capt_rpt.findall('RptSide'):
            side = rpt_side.get('Side')
            for pty in rpt_side.findall('Pty'):
                pty_id = pty.get('ID')
                pty_r = pty.get('R')
                sub_id = pty.find('Sub').get('ID') if pty.find('Sub') is not None else None

                quantity_list.append(int(trd_capt_rpt.get('LastQty')))
                side_list.append(side)
                pty_id_list.append(pty_id)
                pty_r_list.append(pty_r)
                sub_id_list.append(sub_id)
                rpt_id_list.append(rpt_id)

                ultimate_clearing_firm = get_ultimate_clearing_firm(sub_id, pty_r, rpt_id)
                ultimate_clearing_firm_list.append(ultimate_clearing_firm)

                entering_firm_col1 = get_entering_firm_col1(sub_id, pty_r, rpt_id)
                entering_firm_col1_list.append(entering_firm_col1)

                entering_firm_col2 = get_entering_firm_col2(sub_id, pty_r, rpt_id)
                entering_firm_col2_list.append(entering_firm_col2)

    batch_df = {
        'Quantity': quantity_list,
        'Side': side_list,
        'Pty ID': pty_id_list,
        'Pty R': pty_r_list,
        'Sub ID': sub_id_list,
        'RptID': rpt_id_list,
        'Ultimate Clearing Firm': ultimate_clearing_firm_list,
        'Entering Firm - Column 1': entering_firm_col1_list,
        'Entering Firm - Column 2': entering_firm_col2_list
    }

    return batch_df

# Read the XML data from trade.xml and parse it into NumPy arrays (replace 'trade.xml' with the actual file path)
print("Parsing the XML data...")
tree_trade = ET.iterparse('trade_bak.xml', events=('start', 'end'))
_, root_trade = next(tree_trade)  # Get the root element

# Initialize lists to store the parsed trade data
quantity_list = []
side_list = []
pty_id_list = []
pty_r_list = []
sub_id_list = []
rpt_id_list = []
ultimate_clearing_firm_list = []
entering_firm_col1_list = []
entering_firm_col2_list = []

batch_size = 10000
batch_data = []
processed_elements = 0

# Create lists to store the parsed trade data
batch_size = 10000
batch_data = []
processed_elements = 0

# Parse the XML data from trade.xml
for event, element in tree_trade:
    if event == 'end' and element.tag == 'TrdCaptRpt':
        batch_data.append(element)
        processed_elements += 1

        # Process a batch of data
        if processed_elements % batch_size == 0:
            print(f"Processing batch {processed_elements // batch_size}")
            batch_df = process_batch(batch_data)
            batch_data.clear()

            if processed_elements == batch_size:
                # Create the DataFrame with the first batch
                trade_data_frame = pd.DataFrame(batch_df)
            else:
                # Append to the DataFrame for subsequent batches
                trade_data_frame = trade_data_frame.append(pd.DataFrame(batch_df))

            # Clear memory by removing processed elements
            root_trade.clear()

# Process the remaining data (if any)
if batch_data:
    print(f"Processing the last batch {processed_elements // batch_size + 1}")
    batch_df = process_batch(batch_data)
    
    if processed_elements == 0:
        # Create the DataFrame if it's the first and only batch
        trade_data_frame = pd.DataFrame(batch_df)
    else:
        # Append to the DataFrame for the last batch
        if 'trade_data_frame' not in locals():
            trade_data_frame = pd.DataFrame()
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
