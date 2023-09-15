
import sqlite3
import pandas as pd

# Define the SQLite database filename
db_filename = 'trades_new.db'

# Create an SQLite connection
conn = sqlite3.connect(db_filename)

# Query the data and load it into a DataFrame
query = '''
    SELECT Sub_ID, Ultimate_Clearing_Firm as OCC, TRANS_TYPE as transtype, EXCH, Side, Quantity as lastqty_sum
    FROM trades
'''
df = pd.read_sql_query(query, conn)
print(df)

# Create a pivot table
pivot_table = df.pivot_table(
    values='lastqty_sum',
    index=['Sub_ID', 'OCC', 'transtype'],
    columns=['EXCH', 'Side'],
    aggfunc='sum',
    fill_value=0
)

# Reset the index for a cleaner format
pivot_table = pivot_table.reset_index()

# Save the pivot table to a CSV file
pivot_table.to_csv('pivot_table.csv', index=False)

# Close the connection
conn.close()









import sqlite3
import xml.etree.ElementTree as ET
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import sys
import time

ns = {'fixml': 'http://www.fixprotocol.org/FIXML-4-4'}

# Function to determine Sub ID
def extract_sub_id(element):
    sub_id_element = element.find('.//fixml:Sub', ns)
    return sub_id_element.get('ID') if sub_id_element is not None else None

# Function to extract attribute values from the XML elements
def extract_attributes(element, attribute_names):
    attributes = [element.get(attr) for attr in attribute_names]
    return tuple(attributes) if len(attributes) == len(attribute_names) else (None,) * len(attribute_names)

def get_ultimate_clearing_firm(sub_id, pty_r, rpt_id, pty_id):
    if pty_r == '14':
        return pty_id
    elif pty_r == '18':
        return pty_id
    elif pty_r == '1':
        return pty_id
    return None



def create_table():
    conn = sqlite3.connect('trades_new.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS trades;")

    # Create the table for storing the trade data
    cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                        Quantity INTEGER,
                        Side TEXT,
                        Pty_ID TEXT,
                        Pty_R TEXT,
                        Sub_ID TEXT,
                        Rpt_ID TEXT,
                        Ultimate_Clearing_Firm TEXT,
                        EXCH,
                        TRANS_TYPE,
                        ORFInd TEXT
                     )''')

    conn.commit()
    conn.close()

# Function to process a batch of data and insert into the database


def process_batch(batch_data):
    conn = None
    cursor = None
    retries = 5

    while retries > 0:
        try:
            conn = sqlite3.connect('trades_new.db')
            cursor = conn.cursor()

            total_batches = len(batch_data)
            with tqdm(total=total_batches, desc='Inserting data') as pbar:

                # Insert the batch data into the database
                for data in batch_data:
                    quantity, side, rpt_id = data[0:3]
                    pty_id, pty_r, sub_id = data[3:6]  # Extract pty_id, pty_r, sub_id from the data tuple
                    trans_type, exch = data[6:8]
                    orfind = data[8]
                    ultimate_clearing_firm = get_ultimate_clearing_firm(sub_id, pty_r, rpt_id, pty_id)
                    
                    

                    cursor.execute('INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (quantity, side, pty_id, pty_r, sub_id, rpt_id,
                                    ultimate_clearing_firm,exch,trans_type,orfind ))
                    
                    #pbar.update(1)


            conn.commit()
            conn.close()
            break  # Success, break the loop
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                retries -= 1
                if retries > 0:
                    print("Database locked. Retrying in 1 second...")
                    time.sleep(2)
            else:
                # If the error is not related to locking, raise it.
                raise
        finally:
            if conn:
                conn.close()


# Function to fetch data in batches from the trades database
def fetch_data_in_batches(xml_file, batch_size):
    conn = sqlite3.connect('trades1.db')
    cursor = conn.cursor()

    create_table()

    # Parse the XML data and extract the required attributes
    print("Parsing the XML data...")
    tree_trade = ET.parse(xml_file)
    root_trade = tree_trade.getroot()

    # Initialize batch_data list
    batch_data = []

    # Loop through the TrdCaptRpt elements and extract the data
    print("Extracting data from the XML...")
    data_to_process = []
    for trd_capt_rpt in tqdm(root_trade.findall('.//fixml:TrdCaptRpt', ns)):
        rpt_id = trd_capt_rpt.get('RptID')
        trans_type = trd_capt_rpt.get('TransTyp')
        exch = trd_capt_rpt.find('fixml:Instrmt', ns).get('Exch')

        for rpt_side in trd_capt_rpt.findall('fixml:RptSide', ns):
            side = rpt_side.get('Side')
            orfind = rpt_side.get('ORFInd') or '' 

            for pty in rpt_side.findall('fixml:Pty', ns):
                pty_id = pty.get('ID')
                pty_r = pty.get('R')
                sub_element = pty.find('fixml:Sub', ns)
                sub_id = sub_element.get('ID') if sub_element is not None else None

                # Append the parsed data to the batch_data list
                batch_data.append((int(trd_capt_rpt.get('LastQty')), side, rpt_id, pty_id, pty_r, sub_id,trans_type,exch,orfind))

                if len(batch_data) >= batch_size:
                    data_to_process.append(batch_data)
                    batch_data = []

    # Insert the remaining batch data into the data_to_process
    if batch_data:
        data_to_process.append(batch_data)

    # Use multiprocessing to process the data
    with Pool(processes=cpu_count()) as pool:
        pool.map(process_batch, data_to_process)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print("Data has been successfully stored in the SQLite database.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python your_script.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]  # Get the XML file name from command-line arguments
    batch_size = 100  # Adjust the batch size as per your requirement
    fetch_data_in_batches(xml_file, batch_size)
