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
