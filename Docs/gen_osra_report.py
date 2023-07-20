import xml.etree.ElementTree as ET
import pandas as pd
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

# Create an empty DataFrame to store the parsed trade data
columns = ['Quantity', 'Side', 'Pty ID', 'Pty R', 'Sub ID', 'RptID']
trade_data_frame = pd.DataFrame(columns=columns)

# Replace 'your_large_file.xml' with the path to your actual large XML file.
file_path = 'orsa_trades_new.xml'
batch_size = 10000

# Start the XML file parsing in a streaming manner
context = ET.iterparse(file_path, events=('start', 'end'))
context = iter(context)
event, root = next(context)

for event, elem in context:
    if event == 'end' and elem.tag == 'TrdCaptRpt':
        # Process the element and extract relevant data
        rpt_id = elem.get('RptID')

        for rpt_side in elem.findall('RptSide'):
            side = rpt_side.get('Side')

            for pty in rpt_side.findall('Pty'):
                pty_id = pty.get('ID')
                pty_r = pty.get('R')
                sub_id = pty.find('Sub').get('ID') if pty.find('Sub') is not None else None

                # Append the parsed data to the DataFrame
                trade_data_frame = trade_data_frame.append({
                    'Quantity': int(elem.get('LastQty')),  # Convert quantity to integer
                    'Side': side,
                    'Pty ID': pty_id,
                    'Pty R': pty_r,
                    'Sub ID': sub_id,
                    'RptID': rpt_id,
                }, ignore_index=True)

                # Clear the element from memory to free up resources
                elem.clear()

    # As we process the batch, we'll also clear processed elements from memory
    # to prevent the script from consuming excessive memory.

    # If the batch size is reached, perform the data processing on the batch and clear elements
    if len(trade_data_frame) >= batch_size:
        # Determine the Ultimate Clearing Firm
        trade_data_frame['Ultimate Clearing Firm'] = trade_data_frame.apply(
            lambda x: get_ultimate_clearing_firm(x['Sub ID'], x['Pty R'], x['RptID']), axis=1
        )

        # Determine the Entering Firm - Column 1
        trade_data_frame['Entering Firm - Column 1'] = trade_data_frame.apply(
            lambda x: get_entering_firm_col1(x['Sub ID'], x['Pty R'], x['RptID']), axis=1
        )

        # Determine the Entering Firm - Column 2
        trade_data_frame['Entering Firm - Column 2'] = trade_data_frame.apply(
            lambda x: get_entering_firm_col2(x['Sub ID'], x['Pty R'], x['RptID']), axis=1
        )

        # Your additional data processing logic can be performed here if needed.

        # Reset the DataFrame for the next batch
        trade_data_frame = pd.DataFrame(columns=columns)

# Process the remaining records in the last batch (which may be smaller than the batch_size)
if not trade_data_frame.empty:
    # Determine the Ultimate Clearing Firm
    trade_data_frame['Ultimate Clearing Firm'] = trade_data_frame.apply(
        lambda x: get_ultimate_clearing_firm(x['Sub ID'], x['Pty R'], x['RptID']), axis=1
    )

    # Determine the Entering Firm - Column 1
    trade_data_frame['Entering Firm - Column 1'] = trade_data_frame.apply(
        lambda x: get_entering_firm_col1(x['Sub ID'], x['Pty R'], x['RptID']), axis=1
    )

    # Determine the Entering Firm - Column 2
    trade_data_frame['Entering Firm - Column 2'] = trade_data_frame.apply(
        lambda x: get_entering_firm_col2(x['Sub ID'], x['Pty R'], x['RptID']), axis=1
    )

    # Your additional data processing logic can be performed here if needed.

# After processing the entire XML file, continue with the remaining code.

# Replace 'None' with a placeholder value (e.g., 'Unknown')
# filtered_trade_data_frame = trade_data_frame.fillna('Unknown')

# Filter rows where at least one of Ultimate Clearing Firm, Entering Firm - Column 1, or Entering Firm - Column 2 is not None
filtered_trade_data_frame = trade_data_frame[
    trade_data_frame[['RptID', 'Quantity', 'Sub ID', 'Side', 'Ultimate Clearing Firm', 'Entering Firm - Column 1', 'Entering Firm - Column 2']].notna().any(axis=1)
]

# Group the filtered DataFrame and aggregate the values for Ultimate Clearing Firm, Entering Firm - Column 1, and Entering Firm - Column 2
grouped_trade_data_frame = filtered_trade_data_frame.groupby(['Side', 'Sub ID', 'RptID'], as_index=False).agg({
    'Ultimate Clearing Firm': 'first',
    'Entering Firm - Column 1': 'first',
    'Entering Firm - Column 2': 'first',
    'Quantity': 'sum'
})

# Generate the timestamp for the file name up to minutes
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

# Output file name
output_file_name = f'trade_data_{timestamp}.xlsx'

with pd.ExcelWriter(output_file_name) as writer:
    filtered_trade_data_frame.to_excel(writer, sheet_name='Grouped Trade Data', index=False)
    grouped_trade_data_frame.to_excel(writer, sheet_name='Pivoted Trade Data', index=False)
