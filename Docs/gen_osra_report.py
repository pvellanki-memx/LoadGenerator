import xml.etree.ElementTree as ET
import pandas as pd
import datetime

# Function to process each chunk and save it to an Excel file
def process_chunk(chunk_num, trade_data):
    # Filter rows where at least one of Ultimate Clearing Firm, Entering Firm - Column 1, or Entering Firm - Column 2 is not None
    filtered_trade_data_frame = trade_data[
        trade_data[['RptID', 'Quantity', 'Sub ID', 'Side', 'Ultimate Clearing Firm', 'Entering Firm - Column 1', 'Entering Firm - Column 2']].notna().any(axis=1)
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

    # Write the grouped_trade_data_frame to an Excel file
    output_file_name = f'grouped_trade_data_{chunk_num}_{timestamp}.xlsx'
    grouped_trade_data_frame.to_excel(output_file_name, index=False)

    return output_file_name

# Read the XML data from trade.xml and parse it into a DataFrame (replace 'trade.xml' with the actual file path)
tree_trade = ET.parse('trade_bak.xml')
root_trade = tree_trade.getroot()

# Create lists to store the parsed trade data
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

# Parse the XML data from trade.xml
for trd_capt_rpt in root_trade.findall('TrdCaptRpt'):
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

# Split the DataFrame into smaller chunks (adjust the chunk size as needed)
chunk_size = 10000
trade_data_chunks = [trade_data_frame[i:i+chunk_size] for i in range(0, len(trade_data_frame), chunk_size)]

# Process each chunk and append the output to a single Excel file
final_output_file_name = f'grouped_trade_data_final.xlsx'
with pd.ExcelWriter(final_output_file_name) as writer:
    for chunk_num, trade_data_chunk in enumerate(trade_data_chunks, 1):
        output_file_name = process_chunk(chunk_num, trade_data_chunk)
        df = pd.read_excel(output_file_name)
        df.to_excel(writer, sheet_name=f'Chunk_{chunk_num}', index=False)

print(f"Data has been written to {final_output_file_name}")
