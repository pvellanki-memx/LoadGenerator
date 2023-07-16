import xml.etree.ElementTree as ET
import pandas as pd

# Function to determine Ultimate Clearing Firm
def get_ultimate_clearing_firm(sub_id, pty_r, rpt_id):
    if (sub_id == 'C' or sub_id == 'M' or sub_id == 'F') and pty_r == '14' and rpt_id in rpt_id_list:
        return pty_id_list[rpt_id_list.index(rpt_id)]
    elif (sub_id == 'C' or sub_id == 'M' or sub_id == 'F') and pty_r == '18' and rpt_id in rpt_id_list:
        return pty_id_list[rpt_id_list.index(rpt_id)]
    elif (sub_id == 'C' or sub_id == 'M' or sub_id == 'F') and pty_r == '1':
        return pty_id_list[rpt_id_list.index(rpt_id)]
    else:
        return None


# Function to determine Entering Firm - Buy
def get_entering_firm_buy(pty_r, pty_id,rpt_id):
    if pty_r in ['1', '18'] and rpt_id in rpt_id_list:
        return pty_id[:3] if pty_id else None
    else:
        return None

# Function to determine Entering Firm - Sell
def get_entering_firm_sell(pty_r, pty_id,rpt_id):
    if pty_r in ['2', '26'] and rpt_id in rpt_id_list:
        return pty_id[:4] if pty_id else None
    else:
        return None


# Parse the XML data from trade.xml
tree_trade = ET.parse('trade.xml')
root_trade = tree_trade.getroot()

# Create lists to store the parsed trade data
quantity_list = []
side_list = []
pty_id_list = []
pty_r_list = []
sub_id_list = []
rpt_id_list = []
ultimate_clearing_firm_list = []  # List to store Ultimate Clearing Firm
entering_firm_buy_list = []  # List to store Entering Firm - Buy
entering_firm_sell_list = []  # List to store Entering Firm - Sell

# Parse the XML data from trade.xml
for trd_capt_rpt in root_trade.findall('TrdCaptRpt'):
    rpt_id = trd_capt_rpt.get('RptID')
    side = trd_capt_rpt.find('RptSide').get('Side')

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

        # Determine the Entering Firm - Buy
        entering_firm_buy = get_entering_firm_buy(pty_r, pty_id,rpt_id)
        entering_firm_buy_list.append(entering_firm_buy)

        # Determine the Entering Firm - Sell
        entering_firm_sell = get_entering_firm_sell(pty_r,pty_id, rpt_id)
        entering_firm_sell_list.append(entering_firm_sell)

# Parse the XML data from postmove.xml
tree_postmove = ET.parse('postmove.xml')
root_postmove = tree_postmove.getroot()

# Parse the XML data from postmove.xml and append to the respective lists
for trd_capt_rpt in root_postmove.findall('TrdCaptRpt'):
    rpt_id = trd_capt_rpt.get('RptID')
    side = trd_capt_rpt.find('RptSide').get('Side')

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

        # Determine the Entering Firm - Buy
        entering_firm_buy = get_entering_firm_buy(pty_r,pty_id,rpt_id)
        entering_firm_buy_list.append(entering_firm_buy)

        # Determine the Entering Firm - Sell
        entering_firm_sell = get_entering_firm_sell(pty_r, pty_id,rpt_id)
        entering_firm_sell_list.append(entering_firm_sell)

# Create the DataFrame
trade_data_frame = pd.DataFrame({
    'Quantity': quantity_list,
    'Side': side_list,
    'Pty ID': pty_id_list,
    'Pty R': pty_r_list,
    'Sub ID': sub_id_list,
    'RptID': rpt_id_list,
    'Ultimate Clearing Firm': ultimate_clearing_firm_list,
    'Entering Firm - Buy': entering_firm_buy_list,
    'Entering Firm - Sell': entering_firm_sell_list
})

# Print the trade data DataFrame
print(trade_data_frame)

# Generate the timestamp for the file name
import datetime
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

# Write the DataFrame to an Excel file
output_file_name = f'trade_data_{timestamp}.xlsx'
trade_data_frame.to_excel(output_file_name, index=False)


# Parse the XML data from trade.xml
tree_trade = ET.parse('trade.xml')
root_trade = tree_trade.getroot()

# Create lists to store the parsed trade data
quantity_list = []
side_list = []
pty_id_list = []
pty_r_list = []
sub_id_list = []
rpt_id_list = []
ultimate_clearing_firm_list = []  # List to store Ultimate Clearing Firm
entering_firm_buy_list = []  # List to store Entering Firm - Buy
entering_firm_sell_list = []  # List to store Entering Firm - Sell

# Parse the XML data from trade.xml
for trd_capt_rpt in root_trade.findall('TrdCaptRpt'):
    rpt_id = trd_capt_rpt.get('RptID')
    side = trd_capt_rpt.find('RptSide').get('Side')

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

        # Determine the Entering Firm - Buy
        entering_firm_buy = get_entering_firm_buy(pty_r, pty_id,rpt_id)
        entering_firm_buy_list.append(entering_firm_buy)

        # Determine the Entering Firm - Sell
        entering_firm_sell = get_entering_firm_sell(pty_r, pty_id,rpt_id)
        entering_firm_sell_list.append(entering_firm_sell)

# Parse the XML data from postmove.xml
tree_postmove = ET.parse('postmove.xml')
root_postmove = tree_postmove.getroot()

# Parse the XML data from postmove.xml and append to the respective lists
for trd_capt_rpt in root_postmove.findall('TrdCaptRpt'):
    rpt_id = trd_capt_rpt.get('RptID')
    side = trd_capt_rpt.find('RptSide').get('Side')

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

        # Determine the Entering Firm - Buy
        entering_firm_buy = get_entering_firm_buy(pty_r, pty_id,rpt_id)
        entering_firm_buy_list.append(entering_firm_buy)

        # Determine the Entering Firm - Sell
        entering_firm_sell = get_entering_firm_sell(pty_r, pty_id,rpt_id)
        entering_firm_sell_list.append(entering_firm_sell)

# Create the DataFrame
trade_data_frame = pd.DataFrame({
    'Quantity': quantity_list,
    'Side': side_list,
    'Pty ID': pty_id_list,
    'Pty R': pty_r_list,
    'Sub ID': sub_id_list,
    'RptID': rpt_id_list,
    'Ultimate Clearing Firm': ultimate_clearing_firm_list,
    'Entering Firm - Buy': entering_firm_buy_list,
    'Entering Firm - Sell': entering_firm_sell_list
})

# Print the trade data DataFrame
print(trade_data_frame)

# Generate the timestamp for the file name
import datetime
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

# Write the DataFrame to an Excel file
output_file_name = f'trade_data_{timestamp}.xlsx'
trade_data_frame.to_excel(output_file_name, index=False)
