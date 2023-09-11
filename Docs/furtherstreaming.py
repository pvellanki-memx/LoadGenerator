import sqlite3
import sys

db_name = sys.argv[1]

# List of exchanges to summarize
exchanges_to_summarize = [
    'MEMX', 'EMLD', 'BATO', 'C2OX', 'EDGO', 'GMNI', 'MCRY', 'MPRL', 'XASE',
    'XBOX', 'XBXO', 'XCBO', 'XISX', 'XMIO', 'XNDQ', 'XPHO', 'XPSE'
]

# Connect to the SQLite database
conn = sqlite3.connect(db_name)

# Loop through the exchanges and create corresponding summaries
for exchange in exchanges_to_summarize:
    table_name = f'grouped_trades_{exchange}'
    summary_table_name = f'grouped_trades_summary_{exchange}'

    # Check if the table exists in the database
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    result = cursor.fetchone()
    cursor.close()

    if result:
        # The table exists, so create a summary for it
        conn.execute(f'DROP TABLE IF EXISTS {summary_table_name}')
        conn.execute(f'''CREATE TABLE IF NOT EXISTS {summary_table_name} (
                            Side TEXT,
                            Sub_ID TEXT,
                            Ultimate_Clearing_Firm TEXT,
                            Entering_Firm_Col1 TEXT,
                            EXCH TEXT,
                            TRANS_TYPE TEXT,
                            BIZ_DT TEXT,
                            CFI TEXT,
                            PREVLY_RPTD TEXT,
                            RPT_TYP TEXT,
                            MTCH_STAT TEXT,
                            TRD_SUB_TYPE TEXT,
                            TRD_DT TEXT,
                            Total_Quantity INTEGER
                         )''')

        # Query the data from the corresponding 'grouped_trades' table with grouping and summing the quantities
        query_grouped = f"""
            INSERT INTO {summary_table_name} (Side, Sub_ID, Ultimate_Clearing_Firm, Entering_Firm_Col1, EXCH, TRANS_TYPE, BIZ_DT, CFI, PREVLY_RPTD, RPT_TYP, MTCH_STAT, TRD_SUB_TYPE, TRD_DT, Total_Quantity)
            SELECT 
                Side,
                Sub_ID,
                Ultimate_Clearing_Firm,
                Entering_Firm_Col1,
                EXCH,
                TRANS_TYPE,
                BIZ_DT,
                CFI,
                PREVLY_RPTD,
                RPT_TYP,
                MTCH_STAT,
                TRD_SUB_TYPE,
                TRD_DT,
                SUM(Quantity) AS Total_Quantity
            FROM {table_name}
            GROUP BY Side, Sub_ID, Ultimate_Clearing_Firm, Entering_Firm_Col1, EXCH, TRANS_TYPE, BIZ_DT, CFI, PREVLY_RPTD, RPT_TYP, MTCH_STAT, TRD_SUB_TYPE, TRD_DT
        """

        # Execute the query to insert the data into the new summary table
        conn.execute(query_grouped)

# Commit the changes and close the connection to the database
conn.commit()
conn.close()

print("Data has been successfully inserted into the summary tables.")
