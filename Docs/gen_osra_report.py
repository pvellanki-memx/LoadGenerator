import pandas as pd
import datetime
import lxml.etree as ET

# Read the XML data from trade.xml and parse it into a DataFrame (replace 'trade.xml' with the actual file path)
tree_trade = ET.parse('trade_bak.xml')
root_trade = tree_trade.getroot()

# Lists to store parsed trade data
data = {
    'Quantity': [],
    'Side': [],
    'Pty ID': [],
    'Pty R': [],
    'Sub ID': [],
    'RptID': [],
    'Ultimate Clearing Firm': [],
    'Entering Firm - Column 1': [],
    'Entering Firm - Column 2': []
}

# Function to determine Ultimate Clearing Firm, Entering Firm - Column 1, and Entering Firm - Column 2
def get_party_info(rpt_side, rpt_id):
    ultimate_clearing_firm = None
    entering_firm_col1 = None
    entering_firm_col2 = None

    for pty in rpt_side.findall('Pty'):
        pty_id = pty.get('ID')
        pty_r = pty.get('R')
        sub_id = pty.find('Sub').get('ID') if pty.find('Sub') is not None else None

        if sub_id in ['C', 'M', 'F']:
            if pty_r == '14' and rpt_id == rpt_id:
                ultimate_clearing_firm = pty_id
            elif pty_r == '18' and rpt_id == rpt_id:
                entering_firm_col1 = pty_id
            elif pty_r == '2' and rpt_id == rpt_id:
                entering_firm_col2 = pty_id

    return ultimate_clearing_firm, entering_firm_col1, entering_firm_col2

# Parse the XML data from trade.xml
for trd_capt_rpt in root_trade.findall('TrdCaptRpt'):
    rpt_id = trd_capt_rpt.get('RptID')
    side = trd_capt_rpt.find('RptSide').get('Side')

    for rpt_side in trd_capt_rpt.findall('RptSide'):
        quantity = int(trd_capt_rpt.get('LastQty'))  # Convert quantity to integer
        side_value = side
        rpt_id_value = rpt_id

        ultimate_clearing_firm, entering_firm_col1, entering_firm_col2 = get_party_info(rpt_side, rpt_id)

        # Append data to lists
        data['Quantity'].append(quantity)
        data['Side'].append(side_value)
        data['Pty ID'].append(None)  # Replace with the actual pty_id if available
        data['Pty R'].append(None)  # Replace with the actual pty_r if available
        data['Sub ID'].append(None)  # Replace with the actual sub_id if available
        data['RptID'].append(rpt_id_value)
        data['Ultimate Clearing Firm'].append(ultimate_clearing_firm)
        data['Entering Firm - Column 1'].append(entering_firm_col1)
        data['Entering Firm - Column 2'].append(entering_firm_col2)

# Create the DataFrame
trade_data_frame = pd.DataFrame(data)

# Filter rows where at least one of Ultimate Clearing Firm, Entering Firm - Column 1, or Entering Firm - Column 2 is not None
filtered_trade_data_frame = trade_data_frame[
    trade_data_frame[
        ['RptID', 'Quantity', 'Sub ID', 'Side', 'Ultimate Clearing Firm', 'Entering Firm - Column 1', 'Entering Firm - Column 2']
    ].notna().any(axis=1)
]

# Group the filtered DataFrame and aggregate the values for Ultimate Clearing Firm, Entering Firm - Column 1, and Entering Firm - Column 2
grouped_trade_data_frame = filtered_trade_data_frame.groupby(['Side', 'Sub ID', 'RptID'], as_index=False).agg({
    'Ultimate Clearing Firm': 'first',
    'Entering Firm - Column 1': 'first',
    'Entering Firm - Column 2': 'first',
    'Quantity': 'sum'
})

print(grouped_trade_data_frame)

# Generate the timestamp for the file name up to minutes
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

# Write the grouped_trade_data_frame to an Excel file
output_file_name = f'grouped_trade_data_{timestamp}.xlsx'
grouped_trade_data_frame.to_excel(output_file_name, index=False)
