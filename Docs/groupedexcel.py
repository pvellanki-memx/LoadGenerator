
    import sqlite3

# Connect to the original SQLite database
conn = sqlite3.connect('trades_81.db')

# Drop the 'grouped_trades' table if it exists
conn.execute('DROP TABLE IF EXISTS grouped_trades')

# Create a new table to store the query results
conn.execute('''CREATE TABLE grouped_trades (
                    Side TEXT,
                    Sub_ID TEXT,
                    Rpt_ID TEXT,
                    Ultimate_Clearing_Firm TEXT,
                    Entering_Firm_Col1 TEXT,
                    EXCH TEXT,
                    TRANS_TYPE TEXT,
                    EXCH TEXT,
                    TRANS_TYPE TEXT,
                    BIZ_DT TEXT,
                    CFI TEXT,
                    PREVLY_RPTD TEXT,
                    RPT_TYP TEXT,
                    MTCH_STAT TEXT,
                    Quantity INTEGER  -- Add the Quantity column
                 )''')

# Query the data from the original table with grouping and insertion into the new table
query = """
    INSERT INTO grouped_trades (Side, Sub_ID, Rpt_ID, Ultimate_Clearing_Firm, Entering_Firm_Col1, EXCH, TRANS_TYPE, BIZ_DT, CFI, PREVLY_RPTD, RPT_TYP, MTCH_STAT, Quantity)
    SELECT 
        t.Side,
        MAX(CASE WHEN t.Sub_ID != '' AND t.Sub_ID IS NOT NULL THEN t.Sub_ID END) AS Sub_ID,
        t.Rpt_ID,
        MAX(CASE WHEN t.Ultimate_Clearing_Firm != '' AND t.Ultimate_Clearing_Firm IS NOT NULL THEN t.Ultimate_Clearing_Firm END) AS Ultimate_Clearing_Firm,
        MAX(CASE WHEN t.Entering_Firm_Col1 != '' AND t.Entering_Firm_Col1 IS NOT NULL THEN t.Entering_Firm_Col1 END) AS Entering_Firm_Col1,
        t.EXCH,
        t.TRANS_TYPE,
        t.BIZ_DT,
        t.CFI,
        t.PREVLY_RPTD,
        t.RPT_TYP,
        t.MTCH_STAT,
        t.Quantity
    FROM trades t
    GROUP BY t.Rpt_ID, t.Side, t.Quantity
"""

# Execute the query to insert the data into the new table
conn.execute(query)

# Commit the changes and close the connection to the original database
conn.commit()
conn.close()

print("Data has been successfully inserted into the 'grouped_trades' table.")
