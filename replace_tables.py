import pandas as pd
import sqlite3

# Load Excel file into a DataFrame
excel_data = pd.read_excel(r"C:\Users\BRYCE\Documents\192-project\VoltageValues.xlsx")

# Connect to the SQLite database
conn = sqlite3.connect('serial_data.db')
cursor = conn.cursor()

# Clear the existing data from the table
cursor.execute('DELETE FROM VoltageLog;')
conn.commit()

# Insert new data from the DataFrame into the SQLite table
excel_data.to_sql('VoltageLog', conn, if_exists='append', index=False)
cursor.execute("SELECT * FROM VoltageLog WHERE Seconds > 50")
rows = cursor.fetchall()
df = pd.DataFrame(rows)
print(df)
# Close the database connection
conn.close()
