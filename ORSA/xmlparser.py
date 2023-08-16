import xml.etree.ElementTree as ET
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import sys
import time
import sqlite3

# ... (rest of the code)

def create_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # ... (rest of the code)

def process_batch(batch_data, db_name):
    conn = None
    cursor = None
    retries = 5

    while retries > 0:
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            # ... (rest of the code)

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

def fetch_data_in_batches(xml_file, batch_size, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # ... (rest of the code)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python your_script.py <xml_file> <db_name>")
        sys.exit(1)

    xml_file = sys.argv[1]  # Get the XML file name from command-line arguments
    db_name = sys.argv[2]   # Get the trade database name from command-line arguments
    batch_size = 100  # Adjust the batch size as per your requirement
    fetch_data_in_batches(xml_file, batch_size, db_name)
















#update split.py to below:

import xml.etree.ElementTree as ET

def split_xml_file(input_file_path, output_file_prefix, chunk_size=1):
    record_count = 0
    file_count = 1
    output_file_path = f"{output_file_prefix}_{file_count}.xml"
    output_file = open(output_file_path, 'w')

    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    # Strip the opening and closing tags from the original file
    if lines[0].strip() == '<FIXML r="20030618" s="20040109" v="4.4" xr="FIA" xv="1" xmlns="http://www.fixprotocol.org/FIXML-4-4">':
        lines.pop(0)
    if lines[-1].strip() == '</FIXML>':
        lines.pop(-1)
    if lines[0].strip() == '<Batch>':
        lines.pop(0)
    if lines[-1].strip() == '</Batch>':
        lines.pop(-1)

    # Write the opening tags to the first split file
    output_file.write('<FIXML r="20030618" s="20040109" v="4.4" xr="FIA" xv="1" xmlns="http://www.fixprotocol.org/FIXML-4-4">\n')
    output_file.write('<Batch>\n')

    for line in lines:
        if '<Batch>' in line:  # Check for the <Batch> tag
            if record_count == 0:
                output_file.write(line)

        if '<TrdCaptRpt' in line:
            record_count += 1

        output_file.write(line)

        if record_count >= chunk_size:
            record_count = 0
            output_file.write('</Batch>\n')  # Close the <Batch> tag
            output_file.write('</FIXML>\n')  # Close the <FIXML> tag

            file_count += 1
            output_file_path = f"{output_file_prefix}_{file_count}.xml"
            output_file = open(output_file_path, 'w')
            output_file.write('<FIXML r="20030618" s="20040109" v="4.4" xr="FIA" xv="1" xmlns="http://www.fixprotocol.org/FIXML-4-4">\n')
            output_file.write('<Batch>\n')

    output_file.write('</Batch>\n')  # Close the <Batch> tag for the last file
    output_file.write('</FIXML>\n')  # Write the closing </FIXML> tag for the last file
    output_file.close()
    print(f"Split into {file_count} files.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <input_xml_file> <output_file_prefix>")
        sys.exit(1)

    input_xml_file_path = sys.argv[1]
    output_file_prefix = sys.argv[2]
    
    split_xml_file(input_xml_file_path, output_file_prefix)

