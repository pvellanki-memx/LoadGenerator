import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('trades_81.db')

# Drop the 'grouped_trades_summary' table if it exists
conn.execute('DROP TABLE IF EXISTS grouped_trades_summary')

# Create a new table to store the summarized data
conn.execute('''CREATE TABLE IF NOT EXISTS grouped_trades_summary (
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
                    Total_Quantity INTEGER
                 )''')

# Query the data from the 'grouped_trades' table with grouping and summing the quantities
query_grouped = """
    INSERT INTO grouped_trades_summary (Side, Sub_ID, Ultimate_Clearing_Firm, Entering_Firm_Col1, EXCH, TRANS_TYPE,  BIZ_DT, CFI, PREVLY_RPTD, RPT_TYP,MTCH_STAT, Total_Quantity)
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
        SUM(Quantity) AS Total_Quantity
    FROM grouped_trades
    GROUP BY Side, Sub_ID, Ultimate_Clearing_Firm, Entering_Firm_Col1, EXCH, TRANS_TYPE, BIZ_DT, CFI, PREVLY_RPTD, RPT_TYP,MTCH_STAT
"""

# Execute the query to insert the data into the new table
conn.execute(query_grouped)

# Commit the changes and close the connection to the database
conn.commit()
conn.close()

print("Data has been successfully inserted into the 'grouped_trades_summary' table.")
